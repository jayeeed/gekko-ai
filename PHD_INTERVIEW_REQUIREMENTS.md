# PhD interview preparation

## Goal

Support preparation for PhD interviews and conversations with prospective professors. The candidate provides files describing their own profile and separate files describing the professor and research. Gekko builds one knowledge bank from those sources and retrieves relevant information when interview questions arrive.

## Your Profile

Keep the existing **Your Profile** tab and add an **Interview type** dropdown with **General interview** and **PhD interview**.

In PhD mode, collapse the existing Candidate Profile, Interview Focus, and Job Description / Requirements sections. Their fields must not be required to continue. Show a simple PhD file input with one dropdown:

- **My profile**
- **Professor**

The candidate selects which profile the files belong to, then adds one or more files. Support Markdown (`.md`) and LaTeX (`.tex` and `.latex`) only. Do not add PDF, plain text, a manual repository input, professor website scraping, pasted text, research, or opportunity source options. The candidate prepares the files with the information to include. Professor details are supplied by the candidate in their files; the app does not scrape them. A GitHub repository URL included in a candidate profile file is a reference for project questions, not another source input method.

Show each file's name, selected profile, processing state, and any error. Allow removing individual files or clearing all files. To update a file, the candidate can remove and upload the updated version.

## Knowledge bank and answers

Extract readable text from each Markdown or LaTeX file and store it in the local knowledge bank. Generate and maintain `memory.md` with the source content and possible links between candidate and professor information. Label links as possible associations based on shared terms; do not present them as verified facts.

For every interview question, retrieve relevant passages from the current files and pass them to the selected AI model. Ground answers in those passages, do not invent candidate experience or professor details, and state when the files do not provide enough information. Removing a file must remove its information from the generated memory and later answer context.

When a project question refers to a GitHub URL found in the candidate's profile files, fetch current public repository metadata, its README, and a small number of relevant documentation or source files from GitHub's API. Use this live material for that answer when the profile files do not contain enough project detail. Fetch only repositories linked from candidate files, only for project questions, and only public repositories. Keep fetched content in the current request context; do not store it in the local knowledge bank. Label repository evidence and do not claim that the candidate authored work unless their profile supports that claim. If the repository is private, missing, rate-limited, or lacks readable details, acknowledge the gap rather than guessing.

Files and the generated memory are stored under the git-ignored `.phd_knowledge/` directory on the local device. Source content is sent to the selected AI provider when used to answer an interview question. Credentials must not be included in the knowledge bank or committed.

## Remaining onboarding flow

The existing AI Setup, Advanced Config, Commands & Tips, and Device Setup flow stays available in PhD mode. Gemini can be selected through the existing AI Setup.

## Acceptance criteria

- The dropdown selects general or PhD interview mode.
- In PhD mode, general profile, focus, and job description fields are collapsed and optional.
- The only PhD source dropdown choices are **My profile** and **Professor**.
- Multiple `.md`, `.tex`, and `.latex` files can be added for either choice; other file types and source input methods are rejected.
- The knowledge bank and subsequent answers reflect added and removed files.
- Project questions can use live details from public GitHub repositories linked in candidate profile files, while unrelated questions do not trigger GitHub lookups.
- AI Setup, Advanced Config, Commands & Tips, and Device Setup continue to work.
