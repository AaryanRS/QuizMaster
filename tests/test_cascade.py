from app import db
from app.models import Attempt, Question, Quiz


def test_quiz_delete_cascades_questions_and_attempts(app):
    with app.app_context():
        # 1. Create two quizzes
        quiz1 = Quiz(title="Quiz One", category="Science", difficulty="easy")
        quiz2 = Quiz(title="Quiz Two", category="History", difficulty="medium")
        db.session.add_all([quiz1, quiz2])
        db.session.commit()

        quiz1_id = quiz1.id
        quiz2_id = quiz2.id

        # 2. Create at least one Question and one Attempt for each quiz
        q1 = Question(
            quiz_id=quiz1_id,
            text="Question 1 for Quiz 1",
            option_a="A",
            option_b="B",
            option_c="C",
            option_d="D",
            correct_option="A",
        )
        q1_extra = Question(
            quiz_id=quiz1_id,
            text="Question 2 for Quiz 1",
            option_a="A",
            option_b="B",
            option_c="C",
            option_d="D",
            correct_option="C",
        )
        a1 = Attempt(
            quiz_id=quiz1_id,
            player_name="Player 1",
            score=1,
            total_questions=2,
            time_taken_seconds=30,
        )
        a1_extra = Attempt(
            quiz_id=quiz1_id,
            player_name="Player 1 Retest",
            score=2,
            total_questions=2,
            time_taken_seconds=25,
        )

        q2 = Question(
            quiz_id=quiz2_id,
            text="Question 1 for Quiz 2",
            option_a="A",
            option_b="B",
            option_c="C",
            option_d="D",
            correct_option="B",
        )
        a2 = Attempt(
            quiz_id=quiz2_id,
            player_name="Player 2",
            score=1,
            total_questions=1,
            time_taken_seconds=45,
        )

        db.session.add_all([q1, q1_extra, a1, a1_extra, q2, a2])

        # 3. Commit the records
        db.session.commit()

        # 4. Delete the first quiz using db.session.delete(quiz)
        db.session.delete(quiz1)

        # 5. Commit the transaction
        db.session.commit()

        # 6. Expire or refresh session state before verifying persisted database results
        db.session.expire_all()

        # 7. Assert the deleted quiz no longer exists
        assert db.session.get(Quiz, quiz1_id) is None

        # 8. Assert its Questions and Attempts no longer exist
        assert Question.query.filter_by(quiz_id=quiz1_id).all() == []
        assert Attempt.query.filter_by(quiz_id=quiz1_id).all() == []

        # 9. Assert the second quiz remains
        persisted_quiz2 = db.session.get(Quiz, quiz2_id)
        assert persisted_quiz2 is not None
        assert persisted_quiz2.title == "Quiz Two"

        # 10. Assert the second quiz's Questions and Attempts remain unchanged
        quiz2_questions = Question.query.filter_by(quiz_id=quiz2_id).all()
        assert len(quiz2_questions) == 1
        assert quiz2_questions[0].text == "Question 1 for Quiz 2"

        quiz2_attempts = Attempt.query.filter_by(quiz_id=quiz2_id).all()
        assert len(quiz2_attempts) == 1
        assert quiz2_attempts[0].player_name == "Player 2"
