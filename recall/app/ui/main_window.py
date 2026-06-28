from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QButtonGroup,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from recall.app.adapters.ai.fake import FakeQuestionGenerator
from recall.app.adapters.files.text_loader import TextLoader
from recall.app.adapters.storage.sqlite import SQLiteStore
from recall.app.domain.attempt import Attempt
from recall.app.domain.exam import Exam
from recall.app.domain.question import Question
from recall.app.domain.source import Source, SourceChunk
from recall.app.services.scoring import ScoringService
from recall.app.services.source_chunker import SourceChunker


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Recall")
        self.resize(940, 680)

        self.loader = TextLoader()
        self.chunker = SourceChunker()
        self.generator = FakeQuestionGenerator()
        self.scoring = ScoringService()
        self.store = SQLiteStore()

        self.source: Source | None = None
        self.chunks: list[SourceChunk] = []
        self.questions: list[Question] = []
        self.exam: Exam | None = None
        self.selections: dict[str, int | None] = {}
        self.current_index = 0
        self.attempt: Attempt | None = None

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_screen = HomeScreen(self)
        self.exam_screen = ExamScreen(self)
        self.score_screen = ScoreScreen(self)
        self.review_screen = ReviewScreen(self)

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.exam_screen)
        self.stack.addWidget(self.score_screen)
        self.stack.addWidget(self.review_screen)

    def pick_source(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open study file",
            str(Path.home()),
            "Study files (*.txt *.md)",
        )
        if not file_name:
            return

        try:
            source = self.loader.load(file_name)
            chunks = self.chunker.chunk(source)
            if not chunks:
                raise ValueError("Recall could not find enough text to study in this file.")
        except Exception as exc:
            QMessageBox.warning(self, "Could not load source", str(exc))
            return

        self.source = source
        self.chunks = chunks
        self.questions = []
        self.exam = None
        self.selections = {}
        self.current_index = 0
        self.attempt = None
        self.store.save_source(source, chunks)
        self.home_screen.refresh()

    def generate_exam(self) -> None:
        if not self.source:
            QMessageBox.information(self, "Choose a source", "Select a .txt or .md study file first.")
            return

        count = self.home_screen.question_count.value()
        questions = self.generator.generate_questions(self.chunks, count)
        if not questions:
            QMessageBox.warning(self, "Not enough content", "Recall could not generate grounded questions from this source.")
            return

        self.questions = questions
        self.exam = Exam(
            source_id=self.source.id,
            title=f"{self.source.title} exam",
            question_ids=tuple(question.id for question in questions),
        )
        self.selections = {question.id: None for question in questions}
        self.current_index = 0
        self.attempt = None
        self.store.save_questions(questions)
        self.store.save_exam(self.exam)
        self.exam_screen.refresh()
        self.stack.setCurrentWidget(self.exam_screen)

    def submit_exam(self) -> None:
        if not self.exam:
            return
        unanswered = sum(1 for selected in self.selections.values() if selected is None)
        if unanswered:
            response = QMessageBox.question(
                self,
                "Submit with unanswered questions?",
                f"{unanswered} question(s) are unanswered. They will be marked incorrect.",
            )
            if response != QMessageBox.StandardButton.Yes:
                return

        score, answers = self.scoring.score(self.questions, self.selections)
        self.attempt = Attempt(exam_id=self.exam.id, answers=answers, score=score.percent)
        self.store.save_attempt(self.attempt)
        self.score_screen.refresh()
        self.stack.setCurrentWidget(self.score_screen)

    def go_home(self) -> None:
        self.home_screen.refresh()
        self.stack.setCurrentWidget(self.home_screen)

    def show_review(self) -> None:
        self.current_index = 0
        self.review_screen.refresh()
        self.stack.setCurrentWidget(self.review_screen)


class HomeScreen(QWidget):
    def __init__(self, window: MainWindow) -> None:
        super().__init__()
        self.window = window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 34, 34, 34)
        layout.setSpacing(18)

        title = QLabel("Recall")
        title.setObjectName("Title")
        subtitle = QLabel("Turn local notes into active recall exams and review sessions.")
        subtitle.setObjectName("Subtitle")

        self.source_label = QLabel("No source loaded.")
        self.source_label.setWordWrap(True)

        self.chunk_label = QLabel("")
        self.chunk_label.setObjectName("Muted")

        select_button = QPushButton("Open .txt or .md file")
        select_button.clicked.connect(window.pick_source)

        self.question_count = QSpinBox()
        self.question_count.setRange(1, 30)
        self.question_count.setValue(8)

        generate_button = QPushButton("Generate exam")
        generate_button.setObjectName("Primary")
        generate_button.clicked.connect(window.generate_exam)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Questions"))
        controls.addWidget(self.question_count)
        controls.addStretch()
        controls.addWidget(generate_button)

        self.attempts_label = QLabel("Previous attempts appear here after completion.")
        self.attempts_label.setObjectName("Muted")
        self.attempts_label.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(12)
        layout.addWidget(card(self.source_label))
        layout.addWidget(self.chunk_label)
        layout.addWidget(select_button)
        layout.addLayout(controls)
        layout.addSpacing(8)
        layout.addWidget(QLabel("Attempts"))
        layout.addWidget(self.attempts_label)
        layout.addStretch()

    def refresh(self) -> None:
        source = self.window.source
        if not source:
            self.source_label.setText("No source loaded.")
            self.chunk_label.setText("")
            self.attempts_label.setText("Previous attempts appear here after completion.")
            return

        self.source_label.setText(f"{source.title}\n{source.file_path}")
        self.chunk_label.setText(f"{len(self.window.chunks)} source chunk(s) ready for question generation.")
        attempts = self.window.store.attempts_for_source(source.id)
        if not attempts:
            self.attempts_label.setText("No attempts yet for this source.")
            return
        self.attempts_label.setText("\n".join(f"{attempt.finished_at}: {attempt.score:.0f}%" for attempt in attempts[:5]))


class ExamScreen(QWidget):
    def __init__(self, window: MainWindow) -> None:
        super().__init__()
        self.window = window
        self.group = QButtonGroup(self)
        self.group.setExclusive(True)
        self.choice_buttons: list[QRadioButton] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 34, 34, 34)
        layout.setSpacing(16)

        self.progress = QLabel()
        self.prompt = QLabel()
        self.prompt.setObjectName("Question")
        self.prompt.setWordWrap(True)
        layout.addWidget(self.progress)
        layout.addWidget(self.prompt)

        for index in range(4):
            button = ChoiceButton()
            self.group.addButton(button, index)
            self.choice_buttons.append(button)
            layout.addWidget(button)
        self.group.idClicked.connect(self.record_selection)

        nav = QHBoxLayout()
        previous = QPushButton("Previous")
        previous.clicked.connect(self.previous_question)
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_question)
        submit = QPushButton("Submit exam")
        submit.setObjectName("Primary")
        submit.clicked.connect(window.submit_exam)
        nav.addWidget(previous)
        nav.addWidget(next_button)
        nav.addStretch()
        nav.addWidget(submit)
        layout.addStretch()
        layout.addLayout(nav)

    def record_selection(self, choice_index: int) -> None:
        question = self.window.questions[self.window.current_index]
        self.window.selections[question.id] = choice_index

    def previous_question(self) -> None:
        self.window.current_index = max(0, self.window.current_index - 1)
        self.refresh()

    def next_question(self) -> None:
        self.window.current_index = min(len(self.window.questions) - 1, self.window.current_index + 1)
        self.refresh()

    def refresh(self) -> None:
        question = self.window.questions[self.window.current_index]
        self.progress.setText(f"Question {self.window.current_index + 1} of {len(self.window.questions)}")
        self.prompt.setText(question.prompt)
        self.group.blockSignals(True)
        self.group.setExclusive(False)
        for button in self.choice_buttons:
            button.setChecked(False)
        self.group.setExclusive(True)
        for index, button in enumerate(self.choice_buttons):
            button.setText(question.choices[index])
            button.setChecked(self.window.selections.get(question.id) == index)
        self.group.blockSignals(False)


class ScoreScreen(QWidget):
    def __init__(self, window: MainWindow) -> None:
        super().__init__()
        self.window = window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 34, 34, 34)
        layout.setSpacing(16)

        self.score_label = QLabel()
        self.score_label.setObjectName("Title")
        self.detail_label = QLabel()

        review = QPushButton("Review answers")
        review.setObjectName("Primary")
        review.clicked.connect(window.show_review)
        home = QPushButton("Back to source")
        home.clicked.connect(window.go_home)

        layout.addWidget(self.score_label)
        layout.addWidget(self.detail_label)
        layout.addSpacing(20)
        layout.addWidget(review)
        layout.addWidget(home)
        layout.addStretch()

    def refresh(self) -> None:
        if not self.window.attempt:
            return
        correct = sum(1 for answer in self.window.attempt.answers if answer.is_correct)
        total = len(self.window.attempt.answers)
        self.score_label.setText(f"{self.window.attempt.score:.0f}%")
        self.detail_label.setText(f"{correct} correct, {total - correct} incorrect, {total} total.")


class ReviewScreen(QWidget):
    def __init__(self, window: MainWindow) -> None:
        super().__init__()
        self.window = window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(34, 34, 34, 34)
        layout.setSpacing(14)

        self.progress = QLabel()
        self.prompt = QLabel()
        self.prompt.setObjectName("Question")
        self.prompt.setWordWrap(True)
        self.result = QLabel()
        self.result.setWordWrap(True)
        self.explanation = QLabel()
        self.explanation.setWordWrap(True)
        self.excerpt = QLabel()
        self.excerpt.setObjectName("Excerpt")
        self.excerpt.setWordWrap(True)

        nav = QHBoxLayout()
        previous = QPushButton("Previous")
        previous.clicked.connect(self.previous_question)
        next_button = QPushButton("Next")
        next_button.clicked.connect(self.next_question)
        done = QPushButton("Done")
        done.clicked.connect(window.go_home)
        nav.addWidget(previous)
        nav.addWidget(next_button)
        nav.addStretch()
        nav.addWidget(done)

        layout.addWidget(self.progress)
        layout.addWidget(self.prompt)
        layout.addWidget(self.result)
        layout.addWidget(QLabel("Explanation"))
        layout.addWidget(self.explanation)
        layout.addWidget(QLabel("Source excerpt"))
        layout.addWidget(self.excerpt)
        layout.addStretch()
        layout.addLayout(nav)

    def previous_question(self) -> None:
        self.window.current_index = max(0, self.window.current_index - 1)
        self.refresh()

    def next_question(self) -> None:
        self.window.current_index = min(len(self.window.questions) - 1, self.window.current_index + 1)
        self.refresh()

    def refresh(self) -> None:
        if not self.window.attempt:
            return
        question = self.window.questions[self.window.current_index]
        answer = self.window.attempt.answers[self.window.current_index]
        selected = "Unanswered"
        if answer.selected_choice_index is not None:
            selected = question.choices[answer.selected_choice_index]
        correct = question.choices[question.correct_choice_index]
        verdict = "Correct" if answer.is_correct else "Incorrect"

        self.progress.setText(f"Review {self.window.current_index + 1} of {len(self.window.questions)}")
        self.prompt.setText(question.prompt)
        self.result.setText(f"{verdict}\n\nSelected: {selected}\n\nCorrect: {correct}")
        self.result.setProperty("correct", answer.is_correct)
        self.result.style().unpolish(self.result)
        self.result.style().polish(self.result)
        self.explanation.setText(question.explanation)
        self.excerpt.setText(question.source_excerpt)


def card(widget: QWidget) -> QFrame:
    frame = QFrame()
    frame.setObjectName("Card")
    layout = QVBoxLayout(frame)
    layout.addWidget(widget)
    return frame


class ChoiceButton(QRadioButton):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("text-align: left;")

    def setText(self, text: str) -> None:
        super().setText(self._wrap_text(text))

    def _wrap_text(self, text: str, width: int = 92) -> str:
        words = text.split()
        lines: list[str] = []
        current: list[str] = []
        current_len = 0
        for word in words:
            next_len = current_len + len(word) + (1 if current else 0)
            if current and next_len > width:
                lines.append(" ".join(current))
                current = [word]
                current_len = len(word)
            else:
                current.append(word)
                current_len = next_len
        if current:
            lines.append(" ".join(current))
        return "\n".join(lines)
