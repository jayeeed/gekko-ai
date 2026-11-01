"""Fetch bounded public GitHub context referenced by candidate profile files."""
import base64
import asyncio
from datetime import datetime, timedelta, timezone
import re
from urllib.parse import quote, urlsplit

import httpx

from services.phd_knowledge import clean_text, knowledge_bank, terms

PROJECT_QUESTION = re.compile(r'\b(project|repository|repo|codebase|code|github|built|build|developed|implemented|implementation|software|tool|system|prototype|application|app|thesis|experiment)\b', re.I)
MARKDOWN_LINK = re.compile(r'\[([^\]]{1,200})\]\((https://(?:www\.)?github\.com/[^)\s]+)\)', re.I)
GITHUB_URL = re.compile(r'https://(?:www\.)?github\.com/[^\s<>"\']+', re.I)
CACHE_TTL = timedelta(minutes=15)
MAX_REPOSITORIES = 3
MAX_FILES_PER_QUESTION = 2
MAX_TREE_BYTES = 2 * 1024 * 1024
MAX_FILE_BYTES = 40_000
MAX_README_CHARS = 16_000
MAX_SOURCE_CHARS = 6_000
TEXT_SUFFIXES = {'.md', '.rst', '.txt', '.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.go', '.rs', '.cpp', '.h', '.c', '.cs', '.ipynb', '.yaml', '.yml', '.toml'}
SKIP_PATH_PARTS = {'node_modules', 'vendor', '.git', 'dist', 'build', 'coverage', '__pycache__'}

# Cache is memory-only. Removing a Markdown file removes its repository URL from
# subsequent lookups immediately; scraped repository text is never persisted.
_cache = {}


def _repo_from_url(value):
    try:
        parsed = urlsplit(value.rstrip('.,!?;:'))
        if parsed.scheme != 'https' or parsed.hostname not in {'github.com', 'www.github.com'} or parsed.username or parsed.password:
            return None
        segments = [part for part in parsed.path.split('/') if part]
        if len(segments) < 2:
            return None
        owner, repo = segments[:2]
        if repo.endswith('.git'):
            repo = repo[:-4]
        if not re.fullmatch(r'[A-Za-z0-9-]{1,39}', owner) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,100}', repo) or repo in {'.', '..'}:
            return None
        return {'owner': owner, 'repo': repo, 'url': f'https://github.com/{owner}/{repo}'}
    except (ValueError, AttributeError):
        return None


def candidate_repositories():
    """Find only GitHub repository links included in the candidate's own files."""
    refs = {}
    for source in knowledge_bank._all():
        if source.get('category') != 'candidate':
            continue
        content = source.get('content', '')
        matches = [(match.start(2), match.end(2), match.group(1), match.group(2)) for match in MARKDOWN_LINK.finditer(content)]
        linked_spans = {(start, end) for start, end, _, _ in matches}
        matches.extend((match.start(), match.end(), '', match.group(0)) for match in GITHUB_URL.finditer(content) if not any(start <= match.start() < end for start, end in linked_spans))
        for start, end, label, raw_url in matches:
            repo = _repo_from_url(raw_url)
            if not repo:
                continue
            nearby = content[max(0, start - 160):min(len(content), end + 160)]
            repo['label'] = clean_text(label)
            repo['context'] = clean_text(nearby)
            repo['candidate_source'] = source['title']
            refs.setdefault(repo['url'].lower(), repo)
            if len(refs) >= 10:
                return list(refs.values())
    return list(refs.values())


def _rank_repositories(question, refs):
    question_terms = terms(question)
    project_question = bool(PROJECT_QUESTION.search(question))
    ranked = []
    for index, ref in enumerate(refs):
        repo_terms = terms(ref['repo'].replace('-', ' ').replace('_', ' ') + ' ' + ref.get('label', ''))
        overlap = len(question_terms & repo_terms)
        if overlap or project_question:
            ranked.append((overlap, -index, ref))
    ranked.sort(reverse=True, key=lambda row: (row[0], row[1]))
    return [ref for _, _, ref in ranked[:MAX_REPOSITORIES]]


def _prune_cache(now):
    expired = [key for key, value in _cache.items() if value['expires'] <= now]
    for key in expired:
        del _cache[key]
    while len(_cache) > 50:
        oldest = min(_cache, key=lambda key: _cache[key]['expires'])
        del _cache[oldest]


async def _read_repo(client, ref, question):
    now = datetime.now(timezone.utc)
    cached = _cache.get(ref['url'].lower())
    if cached and cached['expires'] > now:
        repo_data = cached['data']
    else:
        repo_data = await _fetch_repo(client, ref)
        _cache[ref['url'].lower()] = {'expires': now + CACHE_TTL, 'data': repo_data}
    if not repo_data.get('ok'):
        return f"[GitHub source unavailable: {ref['url']}] {repo_data.get('error', 'The public repository could not be read.')}. Do not infer its contents."

    files = []
    file_cache = repo_data.setdefault('files', {})
    for path in _select_files(repo_data.get('tree', []), question)[:MAX_FILES_PER_QUESTION]:
        if path not in file_cache:
            file_cache[path] = await _fetch_file(client, ref, repo_data['branch'], path)
        text = file_cache[path]
        if text:
            files.append(f"[GitHub file: {path}]\n{text}")
    parts = [
        f"[Public GitHub repository: {repo_data['full_name']} | {ref['url']}]",
        f"Description: {repo_data.get('description') or 'Not provided'}",
        f"Primary language: {repo_data.get('language') or 'Not provided'}",
        f"Topics: {', '.join(repo_data.get('topics') or []) or 'Not provided'}",
    ]
    if repo_data.get('readme'):
        parts.append('[GitHub README]\n' + repo_data['readme'])
    parts.extend(files)
    if not repo_data.get('readme') and not files:
        parts.append('No readable README or relevant source files were found.')
    return '\n\n'.join(parts)


async def _fetch_repo(client, ref):
    base = f"https://api.github.com/repos/{quote(ref['owner'], safe='')}/{quote(ref['repo'], safe='')}"
    metadata = await _get_json(client, base)
    if metadata.get('error'):
        return {'ok': False, 'error': metadata['error']}
    if metadata.get('private') or metadata.get('visibility') == 'private':
        return {'ok': False, 'error': 'Only public GitHub repositories can be read'}
    full_name = metadata.get('full_name', f"{ref['owner']}/{ref['repo']}")
    readme_response = await _get_json(client, base + '/readme')
    readme = ''
    if readme_response.get('content') and readme_response.get('encoding') == 'base64' and readme_response.get('size', 0) <= MAX_FILE_BYTES:
        try:
            readme = clean_text(base64.b64decode(readme_response['content'], validate=False).decode('utf-8', errors='replace'))[:MAX_README_CHARS]
        except (ValueError, TypeError):
            readme = ''
    tree = await _get_tree(client, base, metadata.get('default_branch', ''))
    return {
        'ok': True,
        'full_name': full_name,
        'description': clean_text(metadata.get('description') or ''),
        'language': clean_text(metadata.get('language') or ''),
        'topics': [clean_text(item) for item in metadata.get('topics', [])[:20]],
        'readme': readme,
        'branch': metadata.get('default_branch', ''),
        'tree': tree,
        'files': {},
    }


async def _get_json(client, url):
    try:
        response = await client.get(url, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'Gekko-PhD-Interview'})
    except httpx.HTTPError:
        return {'error': 'GitHub could not be reached'}
    if response.status_code == 404:
        return {'error': 'The repository or file was not found; it may be private or the link may be stale'}
    if response.status_code == 403:
        return {'error': 'GitHub rate limit or access limit was reached'}
    if response.status_code != 200:
        return {'error': f'GitHub returned HTTP {response.status_code}'}
    try:
        return response.json()
    except (ValueError, TypeError):
        return {'error': 'GitHub returned unreadable data'}


async def _get_tree(client, base, branch):
    if not branch:
        return []
    url = f"{base}/git/trees/{quote(branch, safe='')}?recursive=1"
    try:
        async with client.stream('GET', url, headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'Gekko-PhD-Interview'}) as response:
            if response.status_code != 200:
                return []
            body = bytearray()
            async for chunk in response.aiter_bytes():
                body.extend(chunk)
                if len(body) > MAX_TREE_BYTES:
                    return []
        import json
        payload = json.loads(body)
        return [entry['path'] for entry in payload.get('tree', []) if entry.get('type') == 'blob' and isinstance(entry.get('path'), str) and entry.get('size', MAX_FILE_BYTES + 1) <= MAX_FILE_BYTES and _safe_text_path(entry['path'])]
    except (httpx.HTTPError, ValueError, TypeError):
        return []


def _safe_text_path(path):
    parts = path.replace('\\', '/').split('/')
    if any(part.lower() in SKIP_PATH_PARTS or part.lower().startswith('.env') for part in parts):
        return False
    if any(re.search(r'(secret|credential|token|password|\.pem$|\.key$)', part, re.I) for part in parts):
        return False
    return any(path.lower().endswith(suffix) for suffix in TEXT_SUFFIXES)


def _select_files(paths, question):
    words = terms(question)
    scored = []
    for index, path in enumerate(paths):
        name_terms = terms(path.replace('/', ' ').replace('_', ' ').replace('-', ' '))
        suffix = path.lower().rsplit('.', 1)[-1] if '.' in path else ''
        docs = suffix in {'md', 'rst', 'txt'}
        root_readme = path.lower().endswith('readme.md')
        score = len(words & name_terms) * 10 + (5 if docs else 0) + (4 if '/' not in path else 0) + (3 if path.lower().startswith(('src/', 'app/')) else 0) - (20 if root_readme else 0)
        scored.append((score, -index, path))
    scored.sort(reverse=True)
    return [path for _, _, path in scored]


async def _fetch_file(client, ref, branch, path):
    base = f"https://api.github.com/repos/{quote(ref['owner'], safe='')}/{quote(ref['repo'], safe='')}/contents/{quote(path, safe='/')}?ref={quote(branch, safe='')}"
    data = await _get_json(client, base)
    if data.get('encoding') != 'base64' or data.get('size', MAX_FILE_BYTES + 1) > MAX_FILE_BYTES or not data.get('content'):
        return ''
    try:
        raw = base64.b64decode(data['content'], validate=False)
        return clean_text(raw.decode('utf-8', errors='replace'))[:MAX_SOURCE_CHARS]
    except (ValueError, TypeError):
        return ''


async def fetch_project_evidence(question):
    """Fetch current public repository details linked from candidate Markdown/LaTeX files for project questions."""
    refs = _rank_repositories(question, candidate_repositories())
    if not refs:
        return ''
    _prune_cache(datetime.now(timezone.utc))
    async with httpx.AsyncClient(timeout=12, follow_redirects=False) as client:
        results = await asyncio.gather(*(_read_repo(client, ref, question) for ref in refs))
    return '\n\n'.join(result for result in results if result)
