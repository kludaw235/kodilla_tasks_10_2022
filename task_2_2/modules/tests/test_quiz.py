from task_2_2.modules.quiz import Quiz


def test_quiz():
    quiz_id = 1
    topic = "Chemistry"
    difficulty = "Medium"
    quiz = Quiz(id=quiz_id, topic=topic, difficulty=difficulty)
    assert quiz.id == quiz_id
    assert quiz.topic == topic
    assert quiz.difficulty == difficulty
