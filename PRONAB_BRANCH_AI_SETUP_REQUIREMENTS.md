# Pronab Branch: Knowledge-Grounded Answers and AI Provider Setup

## Purpose

Improve the PhD interview preparation workflow on the `pronab` branch. Answers should use the local knowledge bank for personal and project facts, and use an external AI provider or permitted public sources when the bank does not contain enough information. This document covers preparation and practice sessions.

## Answering behavior

For each question, the system should:

1. Search the current knowledge bank for relevant passages.
2. Use those passages directly when they contain enough evidence to answer. For example, if the candidate's name is in the bank, answer from that source without introducing unrelated claims.
3. If the bank is incomplete, use the configured AI provider to help fill the gap. For project questions, this may include public information about a GitHub repository linked from the candidate's profile.
4. Keep source-backed facts separate from model-generated context. Identify externally sourced details where practical, and do not present unsupported claims as facts about the candidate.
5. Say when the available sources do not support a reliable answer instead of inventing personal details.

The knowledge bank remains the source of truth for candidate-specific facts. External information supplements it; it does not silently replace or rewrite it.

## Provider configuration

The application should support the following setup for the `pronab` branch:

- **Primary text provider:** OpenAI with the `gpt-6-luna` model, using the existing `OPENAI_API_KEYS` value in `.env` and low reasoning effort.
- **Secondary text provider:** Google Gemini, configured as a fallback when Luna is unavailable or a request fails.
- **Models:** Offer `gpt-6-luna` under OpenAI and Gemini Flash under Gemini. Populate the setup choices from provider configuration.
- **Fallback behavior:** Attempt the primary provider first. On a recoverable provider or request failure, try the configured secondary provider and report which provider produced the answer.
- **Configuration source:** Keep API keys in `.env`; do not expose key values in the UI, logs, generated answers, or committed files.

## AI Setup page

The AI Setup page should make it possible to:

- Choose OpenAI and `gpt-6-luna` as the primary text provider and model.
- Choose Gemini and a configured Gemini Flash model as the secondary provider.
- Change either provider or model during preparation and practice sessions.
- Clearly see which provider is primary and which is the fallback.
- Continue to configure vision providers separately from text-answer providers.

## Advanced Config page

The Advanced Config page should:

- List OpenAI alongside the other supported providers.
- Allow adding or updating the OpenAI API key, base URL, supported models, and default model through the existing provider configuration flow.
- Keep the API key masked after entry and avoid returning stored secrets to the frontend.
- Provide a connection check for OpenAI and Gemini.
- Preserve the existing Gemini configuration when OpenAI settings are changed, and vice versa.

## Environment configuration

Use the existing OpenAI API key for Luna and keep Gemini settings separate. Gemini model identifiers remain configurable so the Flash model can be updated without changing application code.

Example shape only; values are supplied locally and must not be committed:

```env
AI_PROVIDERS=OpenAI,Gemini
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEYS=<local OpenAI API key>
OPENAI_MODELS=gpt-6-luna
OPENAI_DEFAULT_MODEL=gpt-6-luna
GEMINI_BASE_URL=<configured Gemini endpoint>
GEMINI_API_KEYS=<local Gemini API key>
GEMINI_MODELS=<configured Gemini model identifiers>
GEMINI_DEFAULT_MODEL=<chosen Gemini Flash model>
```

Use the actual variable names supported by the current provider loader when implementing this requirement. Never put real keys in this document or in source control.

## Acceptance criteria

- A question whose answer is present in the knowledge bank can be answered from that evidence.
- A question with insufficient bank evidence can use the configured model and, where applicable, relevant public repository information.
- The answer distinguishes candidate-specific source evidence from external or model-generated context.
- OpenAI with `gpt-6-luna` can be selected as the primary text provider and Gemini as the secondary fallback in AI Setup.
- The existing OpenAI key and model configuration can be managed through Advanced Config and stored in `.env`.
- A failed OpenAI Luna request can fall back to Gemini, with the selected provider shown in answer metadata.
- Provider keys remain masked and are not exposed in responses or committed configuration.
- The feature is used for preparation and practice sessions.
