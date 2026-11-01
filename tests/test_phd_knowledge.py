from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

import api.phd_knowledge as api
import services.phd_knowledge as knowledge
from core.prompts import get_interview_answer_prompt
from services.context_manager import PersistentContextManager


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.bank = knowledge.KnowledgeBank(self.temp.name)
        self.patch_bank = patch.object(api, 'knowledge_bank', self.bank)
        self.patch_bank.start()
        self.patch_prompt_bank = patch.object(knowledge, 'knowledge_bank', self.bank)
        self.patch_prompt_bank.start()
        app = FastAPI(); app.include_router(api.router)
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close(); self.patch_prompt_bank.stop(); self.patch_bank.stop(); self.temp.cleanup()

    def upload(self, name, category, text):
        return self.client.post('/api/phd/sources/file', params={'filename': name, 'category': category}, content=text.encode())

    def test_only_markdown_and_latex_files_are_accepted(self):
        self.assertIn(self.client.post('/api/phd/sources/github', json={'url':'https://github.com/user/repo'}).status_code, (404, 405))
        self.assertIn(self.client.post('/api/phd/sources/text', json={'title':'Notes', 'category':'candidate', 'content':'text'}).status_code, (404, 405))
        for filename, text in [('cv.md', '# Candidate\nBuilt optical sensors'), ('work.tex', r'\section{Research}' + '\nOptical materials'), ('profile.latex', r'\textbf{Professor}' + '\nQuantum optics')]:
            result = self.upload(filename, 'candidate' if filename == 'cv.md' else 'professor', text)
            self.assertEqual(result.status_code, 201, result.text)
        for filename in ('cv.pdf', 'notes.txt', 'cv.docx'):
            self.assertEqual(self.upload(filename, 'candidate', 'content').status_code, 400)
        self.assertEqual(self.upload('bad.tex', 'candidate', r'\input{other}').status_code, 400)
        self.assertEqual(self.upload('bad.md', 'research', 'text').status_code, 400)

    def test_files_persist_retrieve_and_remove_from_knowledge_bank(self):
        candidate = self.upload('Candidate profile.md', 'candidate', '# Background\nI built optical quantum sensors for precision measurement.').json()
        professor = self.upload('Professor profile.md', 'professor', '# Research\nProfessor Lee studies optical quantum sensors at Yale.').json()
        self.assertNotIn('content', candidate)
        self.assertEqual(len(knowledge.KnowledgeBank(self.temp.name).list()), 2)
        context = PersistentContextManager(); context.initialize_persistent_context({'interviewType':'phd'})
        self.assertTrue(context.ensure_context_available())
        prompt = get_interview_answer_prompt('How does my quantum sensor work fit the professor?', context)
        self.assertIn('precision measurement', prompt)
        self.assertIn('Professor Lee', prompt)
        self.assertIn('Possible connection', prompt)
        self.assertIn('precision measurement', get_interview_answer_prompt('Tell me about yourself', context))
        memory = self.client.get('/api/phd/memory').text
        self.assertIn(candidate['id'], memory)
        self.assertEqual(self.client.delete('/api/phd/sources/' + professor['id']).status_code, 204)
        prompt = get_interview_answer_prompt('Tell me about Professor Lee and quantum optics', context)
        self.assertNotIn('Professor Lee studies', prompt)
        self.assertNotIn('Professor Lee', self.client.get('/api/phd/memory').text)
        self.assertEqual(self.client.delete('/api/phd/sources').status_code, 204)
        self.assertEqual(self.bank.list(), [])
        self.assertIn('No PhD sources', get_interview_answer_prompt('What is my background?', context))

    def test_configured_secret_is_redacted_and_bad_category_rejected(self):
        with patch.object(knowledge, 'dotenv_values', return_value={'GEMINI_API_KEYS': 'unlabelled-secret-12345'}):
            source = self.bank.add('Profile.md', 'candidate', 'file', 'unlabelled-secret-12345 was pasted here')
        self.assertNotIn('unlabelled-secret-12345', source['content'])
        self.assertNotIn('unlabelled-secret-12345', Path(self.temp.name, 'memory.md').read_text())
        self.assertEqual(self.upload('bad.md', 'invalid', 'text').status_code, 400)


if __name__ == '__main__':
    unittest.main()
