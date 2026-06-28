# Recall

Recall is a local-first desktop study app that turns text notes into active recall exams and review sessions.

The first version reads a local `.txt` or `.md` file, splits it into source chunks, generates deterministic multiple-choice questions, lets you take an exam, scores it, and shows a review with explanations and source excerpts.

## Why Local Desktop First

Recall is a personal study tool for desktop/laptop use. It starts as a Python + PySide6 app so study material stays local and the core workflow works without accounts, hosting, sync, or internet access.

## Run On Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
recall
```

You can also run it directly:

```bash
python3 -m recall.app.main
```

## Test

```bash
pytest
```

## Current Capabilities

- Load local `.txt` and `.md` study files.
- Split content by Markdown headings or paragraph-sized chunks.
- Generate deterministic multiple-choice questions without an LLM.
- Take an exam one question at a time.
- Score answers deterministically.
- Review selected answers, correct answers, explanations, and source excerpts.
- Save sources, exams, questions, attempts, and answers in local SQLite.

## Current Limitations

- Only `.txt` and `.md` files are supported.
- Questions come from a fake deterministic generator, not a real model.
- Question quality is intentionally basic until a local AI provider is added.
- No PDF, DOCX, EPUB, cloud sync, accounts, or hosted service.

## Development Milestones

1. Skeleton desktop app.
2. File loading for `.txt` and `.md`.
3. Source chunking.
4. Fake deterministic multiple-choice generation.
5. Exam taking flow.
6. Review flow.
7. SQLite persistence.
8. Real AI provider behind the existing generator interface.
