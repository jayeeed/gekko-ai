import asyncio
import base64
import json
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import services.github_research as github
import services.phd_knowledge as knowledge
from core.prompts import get_interview_answer_prompt
from services.context_manager import PersistentContextManager


class FakeResponse:
    def __init__(self, payload, status=200):
        self.payload = payload
        self.status_code = status

    def json(self):
        return self.payload


class FakeStreamResponse:
    status_code = 200

    def __init__(self, payload): self.payload = json.dumps(payload).encode()
    async def __aenter__(self): return self
    async def __aexit__(self, *args): pass
    async def aiter_bytes(self): yield self.payload


class GithubResearchTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory(prefix='gekko-github-tests-')
        self.addCleanup(self.directory.cleanup)
        self.temp = knowledge.KnowledgeBank(self.directory.name)
        self.temp.clear()
        self.bank_patch = patch.object(github, 'knowledge_bank', self.temp)
        self.bank_patch.start()
        github._cache.clear()
        self.addCleanup(self.bank_patch.stop)
        self.addCleanup(github._cache.clear)
        self.addCleanup(self.temp.clear)

    def test_project_question_reads_only_candidate_linked_public_repo_details(self):
        self.temp.add('CV.md', 'candidate', 'file', '[Sensor Toolkit](https://github.com/octocat/sensor-toolkit)\nI contributed to sensor calibration tests.')
        self.temp.add('Professor.md', 'professor', 'file', '[Private project](https://github.com/example/not-for-candidate-file)')

        calls = []
        class FakeClient:
            def __init__(self, **kwargs): pass
            async def __aenter__(self): return self
            async def __aexit__(self, *args): pass
            async def get(self, url, **kwargs):
                calls.append(url)
                if url.endswith('/readme'):
                    return FakeResponse({'encoding':'base64','size':45,'content':base64.b64encode(b'Calibration toolkit for optical sensors').decode()})
                if '/contents/docs/calibration.md?' in url:
                    content = '# Calibration\nUses a two-stage reference sweep.'
                    return FakeResponse({'encoding':'base64','size':len(content),'content':base64.b64encode(content.encode()).decode()})
                if '/contents/src/sensor.py?' in url:
                    content = 'def calibrate(): return reference_sweep()'
                    return FakeResponse({'encoding':'base64','size':len(content),'content':base64.b64encode(content.encode()).decode()})
                return FakeResponse({'full_name':'octocat/sensor-toolkit','private':False,'description':'Optical sensor calibration tools','language':'Python','topics':['optics'],'default_branch':'main'})
            def stream(self, method, url, **kwargs):
                calls.append(url)
                payload={'tree':[
                    {'path':'docs/calibration.md','type':'blob','size':100},
                    {'path':'src/sensor.py','type':'blob','size':100},
                    {'path':'.env','type':'blob','size':100},
                    {'path':'secrets/token.txt','type':'blob','size':100},
                ]}
                return FakeStreamResponse(payload)
        self.patch_client = patch.object(github.httpx, 'AsyncClient', FakeClient)
        self.patch_client.start()
        self.addCleanup(self.patch_client.stop)

        evidence = asyncio.run(github.fetch_project_evidence('Explain the sensor calibration project implementation'))
        self.assertIn('Optical sensor calibration tools', evidence)
        self.assertIn('two-stage reference sweep', evidence)
        self.assertIn('reference_sweep()', evidence)
        self.assertNotIn('.env', evidence)
        self.assertNotIn('not-for-candidate-file', evidence)
        self.assertTrue(calls)
        self.assertTrue(all(url.startswith('https://api.github.com/') for url in calls))
        context=PersistentContextManager(); context.initialize_persistent_context({'interviewType':'phd'})
        prompt=get_interview_answer_prompt('Explain the sensor calibration project implementation',context,evidence)
        self.assertIn('two-stage reference sweep',prompt)
        self.assertIn('never turn a broad claim',prompt)

    def test_unrelated_question_does_not_fetch_and_candidate_link_removal_stops_future_fetches(self):
        self.temp.add('CV.md','candidate','file','Sensor work: https://github.com/octocat/sensor-toolkit')
        class ForbiddenClient:
            def __init__(self, **kwargs): raise AssertionError('Non-project question must not access GitHub')
        with patch.object(github.httpx,'AsyncClient',ForbiddenClient):
            self.assertEqual(asyncio.run(github.fetch_project_evidence('Why do I want to work with this professor?')), '')
        source=self.temp.list()[0]
        self.temp.delete(source['id'])
        self.assertEqual(asyncio.run(github.fetch_project_evidence('Tell me about my project implementation')), '')

    def test_non_github_urls_are_ignored(self):
        self.temp.add('CV.md','candidate','file','Project: https://evil.example.com/octocat/sensor-toolkit')
        self.assertEqual(github.candidate_repositories(), [])


if __name__ == '__main__':
    unittest.main()
