import pytest

from website import create_app
from website.questionHandler import getQuestion


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app


def test_getQuestion(app):
    with app.app_context():
        question = getQuestion(4)

    expected_question = {
        "questionID": 4,
        "mandatory": True,
        "user_type": [1, 2],
        "questionText": "Would you like to go to previous countries?",
        "questionHelper": "",
        "questionType": "Multiple Choice",
        "ToNote": "Boolean",
        "answers": [
            {
                "answerID": 400,
                "answerText": "Yes",
                "modifiers": [
                    {
                        "modifier": "prev_countries",
                        "value": True
                    }
                ]
            },
            {
                "answerID": 401,
                "answerText": "No",
                "modifiers": [
                    {
                        "modifier": "prev_countries",
                        "value": False
                    }
                ]
            }
        ]
    }

    assert question == expected_question
