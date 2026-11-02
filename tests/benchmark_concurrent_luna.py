"""Exercise two real Luna streams against the same interview context.

Run with the project virtual environment. Prints timing and answer excerpts,
never credentials or source documents.
"""

import asyncio
import sys
import time

from core.provider_service import load_providers_config
from services.context_manager import PersistentContextManager
from services.llm_service import LLMManager


QUESTIONS = (
    "Tell me about your research experience.",
    "How does your experience relate to healthcare data and MIMIC-IV?",
)


async def main():
    config = next(p for p in load_providers_config() if p["name"] == "OpenAI")
    context = PersistentContextManager()
    context.initialize_persistent_context({"name": "Latency Test", "interviewType": "phd"})
    llm = LLMManager(
        provider_name="OpenAI",
        base_url=config["baseURL"],
        api_key=config["apiKeys"][0],
        api_keys=config["apiKeys"],
        model_name="gpt-6-luna",
        request_params={"reasoning_effort": "low"},
    )
    llm.set_context_manager(context)
    origin = time.perf_counter()
    results = {}

    async def ask(index, question):
        started = time.perf_counter()
        first = None
        chunks = 0

        async def on_chunk(chunk, chunk_type):
            nonlocal first, chunks
            if chunk:
                chunks += 1
                if first is None:
                    first = time.perf_counter()
                    print(f"request={index} first_chunk_at_s={first - origin:.3f}", flush=True)

        print(f"request={index} start_at_s={started - origin:.3f}", flush=True)
        answer, info = await llm.get_ai_answer(question, on_chunk)
        finished = time.perf_counter()
        results[index] = (started, first, finished, answer, info, chunks)
        print(f"request={index} complete_at_s={finished - origin:.3f} success={bool(info.get('success'))} words={len(answer.split())} chunks={chunks}", flush=True)
        print(f"request={index} answer_excerpt={answer[:450]!r}", flush=True)

    first_task = asyncio.create_task(ask(1, QUESTIONS[0]))
    await asyncio.sleep(0.5)
    second_task = asyncio.create_task(ask(2, QUESTIONS[1]))
    await asyncio.gather(first_task, second_task)
    first, second = results[1], results[2]
    print(f"requests_overlapped={second[0] < first[2]}")
    print(f"first_answer_attached_to_first_question={context.conversation_history[0]['ai_response'] == first[3]}")
    print(f"second_answer_attached_to_second_question={context.conversation_history[1]['ai_response'] == second[3]}")
    if not (second[0] < first[2] and all(result[4].get('success') for result in (first, second))):
        raise RuntimeError("Live concurrent Luna check failed")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main())
