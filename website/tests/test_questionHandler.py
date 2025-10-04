import pytest
from website.questionHandler import getQuestion

def test_getQuestion():
    question = getQuestion(4)
    expected_question = {
      "questionID": 4,
      "mandatory": True,
      "user_type": [1,2],
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





