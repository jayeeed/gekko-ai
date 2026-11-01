"""Endpoints for managing locally stored PhD interview sources."""
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse

from services.phd_knowledge import MAX_FILE_BYTES, extract_file, knowledge_bank

router = APIRouter(prefix='/api/phd', tags=['phd'])


def public_source(source):
    return {key: value for key, value in source.items() if key != 'content'}


@router.get('/sources')
def list_sources():
    return {'sources': knowledge_bank.list()}


@router.post('/sources/file', status_code=201)
async def add_file(request: Request, filename: str = Query(min_length=1, max_length=200), category: str = Query(default='candidate')):
    data = bytearray()
    async for chunk in request.stream():
        data.extend(chunk)
        if len(data) > MAX_FILE_BYTES:
            raise HTTPException(413, 'Files must be 5 MB or smaller.')
    try:
        content = extract_file(filename, bytes(data))
        return public_source(knowledge_bank.add(filename, category, 'file', content, filename))
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc


@router.delete('/sources/{source_id}', status_code=204)
def delete_source(source_id: str):
    if not knowledge_bank.delete(source_id):
        raise HTTPException(404, 'Source not found.')


@router.delete('/sources', status_code=204)
def delete_all_sources():
    knowledge_bank.clear()


@router.get('/memory', response_class=PlainTextResponse)
def get_memory():
    # Rebuild from the database, the authoritative source, if the file was removed.
    with knowledge_bank.lock, knowledge_bank._connect() as db:
        knowledge_bank._write_memory(db)
    return PlainTextResponse((knowledge_bank.directory / 'memory.md').read_text(encoding='utf-8'), media_type='text/markdown')
