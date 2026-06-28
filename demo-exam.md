# Recall Demo Exam

This is a small demonstration exam showing the first-version Recall flow:

1. Read source material.
2. Answer multiple-choice questions.
3. Check the score.
4. Review each answer with the explanation and source excerpt.

## Source Summary

Recall is a local-first desktop study app. It turns `.txt` and `.md` notes into active recall exams. The first version uses deterministic multiple-choice questions so scoring is simple and review behavior is easy to verify. Recall stores sources, generated questions, exams, attempts, and answers in local SQLite. The first implementation uses a fake offline question generator while keeping the architecture ready for future providers such as Ollama or OpenAI.

## Questions

### 1. What is Recall's main purpose?

- A. Turn local study notes into active recall exams and review sessions.
- B. Host public classrooms for many users.
- C. Sync study files across cloud accounts.
- D. Convert PDFs into spaced-repetition cards.

**Correct answer:** A

**Explanation:** Recall focuses on transforming local notes into active recall practice, scoring, and review.

**Source excerpt:** "Recall is a local-first desktop study app. It turns `.txt` and `.md` notes into active recall exams."

### 2. Why does the first version use multiple-choice questions?

- A. They require internet access.
- B. They make deterministic scoring and review easier to validate.
- C. They allow free-text AI grading.
- D. They replace the need for source excerpts.

**Correct answer:** B

**Explanation:** Multiple-choice questions keep scoring deterministic and make the review flow straightforward.

**Source excerpt:** "The first version uses deterministic multiple-choice questions so scoring is simple and review behavior is easy to verify."

### 3. Where does Recall store first-version app data?

- A. In a hosted Postgres database.
- B. In browser local storage.
- C. In local SQLite.
- D. In a shared classroom workspace.

**Correct answer:** C

**Explanation:** Recall is local-first and persists its basic records in SQLite on the user's machine.

**Source excerpt:** "Recall stores sources, generated questions, exams, attempts, and answers in local SQLite."

### 4. What does the fake question generator enable?

- A. Offline UI development and deterministic tests.
- B. PDF parsing.
- C. Mobile push notifications.
- D. Cloud-hosted model fine-tuning.

**Correct answer:** A

**Explanation:** The fake provider lets the app generate predictable questions without relying on an external model.

**Source excerpt:** "The first implementation uses a fake offline question generator while keeping the architecture ready for future providers such as Ollama or OpenAI."

## Review Template

Use this format after taking an exam:

| Question | Selected | Correct | Result |
| --- | --- | --- | --- |
| 1 |  | A |  |
| 2 |  | B |  |
| 3 |  | C |  |
| 4 |  | A |  |
