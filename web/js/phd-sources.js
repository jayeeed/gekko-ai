const $ = id => document.getElementById(id);
const categories = { candidate: 'My profile', professor: 'Professor' };
let pending = 0;

function status(message, error = false) {
    const el = $('phd-status');
    el.textContent = message;
    el.classList.toggle('error', error);
}

async function request(url, options = {}) {
    const response = await fetch(url, options);
    if (!response.ok) {
        let message = `Request failed (HTTP ${response.status}).`;
        try { const body = await response.json(); if (typeof body.detail === 'string') message = body.detail; } catch (_) { /* Keep the HTTP error. */ }
        throw new Error(message);
    }
    return response.status === 204 ? null : response.json();
}

function setBusy(busy) {
    pending += busy ? 1 : -1;
    window.phdSourcesBusy = pending > 0;
    for (const id of ['phd-upload', 'phd-clear']) $(id).disabled = pending > 0;
}

async function refresh() {
    const { sources } = await request('/api/phd/sources');
    const list = $('phd-source-list');
    list.replaceChildren();
    $('phd-clear').hidden = sources.length === 0;
    if (!sources.length) {
        const empty = document.createElement('li');
        empty.textContent = 'No files added yet. Choose My profile or Professor and select Markdown or LaTeX files.';
        empty.className = 'phd-empty';
        list.append(empty);
        return;
    }
    for (const source of sources) {
        const li = document.createElement('li');
        const description = document.createElement('div');
        const title = document.createElement('strong');
        title.textContent = source.title;
        const meta = document.createElement('small');
        meta.textContent = `${categories[source.category] || source.category} · ${source.title.toLowerCase().endsWith('.md') ? 'Markdown' : 'LaTeX'} · Ready`;
        description.append(title, meta);
        const remove = document.createElement('button');
        remove.type = 'button'; remove.className = 'phd-link'; remove.textContent = 'Remove';
        remove.setAttribute('aria-label', `Remove ${source.title}`);
        remove.addEventListener('click', async () => {
            if (!window.confirm(`Remove “${source.title}” from the knowledge bank?`)) return;
            setBusy(true);
            try {
                await request(`/api/phd/sources/${encodeURIComponent(source.id)}`, { method: 'DELETE' });
                await refresh(); status('File removed from the knowledge bank.');
            } catch (error) { status(error.message, true); }
            finally { setBusy(false); }
        });
        li.append(description, remove); list.append(li);
    }
}

export function setupPhdSources() {
    const type = $('interview-type');
    const applyType = () => {
        const phd = type.value === 'phd';
        $('phd-section').hidden = !phd;
        $('general-profile').open = !phd;
    };
    type.addEventListener('change', applyType);
    applyType();
    refresh().catch(error => status(`Could not load files: ${error.message}`, true));
    $('phd-upload').addEventListener('click', async () => {
        const files = [...$('phd-file').files];
        if (!files.length) return status('Choose one or more Markdown or LaTeX files.', true);
        setBusy(true);
        const failures = [];
        let added = 0;
        try {
            for (const file of files) {
                status(`Reading ${file.name}…`);
                try {
                    await request(`/api/phd/sources/file?filename=${encodeURIComponent(file.name)}&category=${encodeURIComponent($('phd-category').value)}`, { method: 'POST', headers: { 'Content-Type': 'application/octet-stream' }, body: file });
                    added++;
                } catch (error) { failures.push(`${file.name}: ${error.message}`); }
            }
            $('phd-file').value = '';
            await refresh();
            status(failures.length ? `${added} added. ${failures.join(' ')}` : `${added} file${added === 1 ? '' : 's'} added to the knowledge bank.`, failures.length > 0);
        } catch (error) { status(error.message, true); }
        finally { setBusy(false); }
    });
    $('phd-clear').addEventListener('click', async () => {
        if (!window.confirm('Remove all PhD profile files from this device?')) return;
        setBusy(true);
        try { await request('/api/phd/sources', { method: 'DELETE' }); await refresh(); status('All files removed from the knowledge bank.'); }
        catch (error) { status(error.message, true); }
        finally { setBusy(false); }
    });
}
