import { devLog } from './config.js';

export class ConfigManager {
    constructor(stateManager) {
        this.stateManager = stateManager;
        this.providers = [];
        this.elements = {
            providersList: document.getElementById('adv-providers-list'),
            deepgramKey: document.getElementById('adv-deepgram-key'),
            saveDeepgramBtn: document.getElementById('save-deepgram-btn'),
            saveProvidersBtn: document.getElementById('save-all-providers-btn')
        };

        this.init();
    }

    async init() {
        if (!this.elements.providersList) return;

        await this.loadInitialData();
        this.setupEventListeners();
    }

    async loadInitialData() {
        try {
            // Load full providers with keys
            const pResp = await fetch('/api/ai-providers/full');
            this.providers = await pResp.json();

            // Load Deepgram key
            const dResp = await fetch('/api/deepgram-key');
            const dData = await dResp.json();
            if (this.elements.deepgramKey) {
                this.elements.deepgramKey.value = '';
                this.elements.deepgramKey.placeholder = dData.configured ? 'Key saved - enter a new key to replace it' : 'DEEPGRAM_API_KEY';
            }

            this.renderProviders();
        } catch (error) {
            console.error('Failed to load advanced config data:', error);
        }
    }

    setupEventListeners() {
        if (this.elements.saveDeepgramBtn) {
            this.elements.saveDeepgramBtn.addEventListener('click', () => this.saveDeepgramKey());
        }

        if (this.elements.saveProvidersBtn) {
            this.elements.saveProvidersBtn.addEventListener('click', () => this.saveProviders());
        }
    }

    renderProviders() {
        if (!this.elements.providersList) return;

        this.elements.providersList.innerHTML = '';

        this.providers.forEach((provider, pIndex) => {
            const tr = document.createElement('tr');

            // Name Cell
            const nameTd = document.createElement('td');
            const title = document.createElement('strong');
            title.textContent = provider.name;
            nameTd.appendChild(title);
            for (const [label, field, value] of [
                ['Base URL', 'baseURL', provider.baseURL || ''],
                ['Text models (comma separated)', 'models', (provider.models || []).map(m => m.modelName || m).join(',')],
                ['Default text model', 'defaultModel', provider.defaultModel || '']
            ]) {
                const caption = document.createElement('label');
                caption.textContent = label;
                caption.style.display = 'block';
                const input = document.createElement('input');
                input.type = 'text';
                input.value = value;
                input.placeholder = label;
                input.addEventListener('input', () => {
                    provider[field] = field === 'models'
                        ? input.value.split(',').map(item => item.trim()).filter(Boolean)
                        : input.value.trim();
                });
                caption.appendChild(input);
                nameTd.appendChild(caption);
            }
            for (const [label, field] of [['Primary text default', 'defaultPrimary'], ['Secondary text default', 'defaultSecondary']]) {
                const caption = document.createElement('label');
                caption.style.display = 'block';
                const radio = document.createElement('input');
                radio.type = 'radio';
                radio.name = field;
                radio.checked = Boolean(provider[field]);
                radio.addEventListener('change', () => {
                    this.providers.forEach(item => { item[field] = item === provider; });
                });
                caption.appendChild(radio);
                caption.appendChild(document.createTextNode(label));
                nameTd.appendChild(caption);
            }
            tr.appendChild(nameTd);

            // Keys Cell
            const keysTd = document.createElement('td');
            const keyListDiv = document.createElement('div');
            keyListDiv.className = 'key-list';

            const savedCount = document.createElement('small');
            savedCount.textContent = provider.keyCount ? `${provider.keyCount} key(s) saved` : 'No key saved';
            keyListDiv.appendChild(savedCount);
            const input = document.createElement('input');
            input.type = 'password';
            input.autocomplete = 'new-password';
            input.placeholder = 'New API key(s), comma separated';
            input.addEventListener('input', () => {
                provider.apiKeys = input.value.split(',').map(key => key.trim()).filter(Boolean);
            });
            keyListDiv.appendChild(input);
            keysTd.appendChild(keyListDiv);
            tr.appendChild(keysTd);

            // Actions Cell
            const actionsTd = document.createElement('td');
            const testBtn = document.createElement('button');
            testBtn.className = 'save-small';
            testBtn.textContent = 'Test Connection';
            testBtn.onclick = () => this.testProviderConnection(provider, testBtn);
            actionsTd.appendChild(testBtn);
            tr.appendChild(actionsTd);

            this.elements.providersList.appendChild(tr);
        });
    }

    async testProviderConnection(provider, btn) {
        const originalText = btn.textContent;
        btn.textContent = 'Testing...';
        btn.disabled = true;

        try {
            if (provider.apiKeys?.length) {
                alert('Save the new API key before testing the connection.');
                return;
            }
            const testKey = provider.keyCount;
            const testModel = provider.defaultModel || (provider.models[0]?.modelName || provider.models[0]);

            if (!testKey || !provider.baseURL || !testModel) {
                alert('Save an API key, base URL, and default model before testing.');
                return;
            }

            const response = await fetch('/api/verify-provider', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: provider.name,
                    model: testModel
                }),
            });

            const result = await response.json();

            if (result.success) {
                btn.textContent = '✅ Success';
                btn.style.borderColor = 'var(--accent-success)';
            } else {
                btn.textContent = '❌ Failed';
                btn.style.borderColor = 'var(--accent-warning)';
            }

            setTimeout(() => {
                btn.textContent = originalText;
                btn.disabled = false;
                btn.style.borderColor = '';
            }, 3000);

        } catch (error) {
            console.error('Test failed:', error);
            btn.textContent = 'Error';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.disabled = false;
            }, 3000);
        } finally {
            btn.disabled = false;
            if (btn.textContent === 'Testing...') btn.textContent = originalText;
        }
    }

    async saveDeepgramKey() {
        const key = this.elements.deepgramKey.value;
        if (!key) return;
        const btn = this.elements.saveDeepgramBtn;
        const originalText = btn.textContent;

        btn.textContent = 'Saving...';
        btn.disabled = true;

        try {
            const resp = await fetch('/api/save-deepgram-key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key })
            });

            if (resp.ok) {
                btn.textContent = '✅ Saved';
                this.elements.deepgramKey.value = '';
                this.elements.deepgramKey.placeholder = 'Key saved - enter a new key to replace it';
                devLog('Deepgram key saved successfully');
            } else {
                btn.textContent = '❌ Failed';
            }

            setTimeout(() => {
                btn.textContent = originalText;
                btn.disabled = false;
            }, 2000);
        } catch (error) {
            console.error('Save failed:', error);
            btn.textContent = 'Error';
            btn.disabled = false;
        }
    }

    async saveProviders() {
        const btn = this.elements.saveProvidersBtn;
        const originalText = btn.textContent;

        btn.textContent = 'Saving Configuration...';
        btn.disabled = true;

        try {
            const resp = await fetch('/api/save-ai-providers', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ providers: this.providers })
            });

            if (resp.ok) {
                btn.textContent = '✅ All Changes Saved';
                devLog('AI Providers saved successfully');
                await this.loadInitialData();

                // Trigger reload in provider manager if available
                if (window.providerManager) {
                    await window.providerManager.loadAiProviders();
                }
            } else {
                btn.textContent = '❌ Save Failed';
            }

            setTimeout(() => {
                btn.textContent = originalText;
                btn.disabled = false;
            }, 3000);
        } catch (error) {
            console.error('Save failed:', error);
            btn.textContent = 'Error';
            btn.disabled = false;
        }
    }
}
