import json

f = open("static/test2.json", 'r')
data = json.load(f)


def getQuestionFromFile(questions, questionNumber):
    for question in questions["questions"]:
        # if the id of the current question is the same as the desired question
        if question.get("questionID") == questionNumber:
            question_id = question.get('questionID')
            question_text = question.get('questionText')
            question_type = question.get('questionType')
            answers = question.get("answers")
            print(question_text)
            return answers
            break

            # for answer in question["answers"]:
            #     #print(type(answer))
            #     answer_id = answer.get("answerID")
            #     answer_text = answer.get("answerText")
            #
            #     # for modifier in answer["modifiers"]:
            #     #     to_modify = modifier.get("modifier")
            #     #     modify_by = modifier.get("modifyBy")

    return answers


def getAnswerFromFile(answers, userAnswer):
    for answer in answers:
        if answer.get("answerText") == userAnswer:
            answer_id = answer.get("answerID")
            answer_text = answer.get("answerText")
            print(answer_id)
            print(answer_text)
            for modifier in answer["modifiers"]:
                toModify = modifier.get("modifier")
                modificationBy = modifier.get("modifyBy")
                print(type(toModify))
                print(toModify)
                print(type(modificationBy))
                print(modificationBy)

                return modifier

            return answer







questionNumber = int(input("What question would you like? "))
questionAnswers = getQuestionFromFile(data, questionNumber)
userAnswer = str(input("What is your answer? "))
getAnswerFromFile(questionAnswers, userAnswer)







# class Question:
#     def __init__(self, questionID, questionText, questionType, answers):
#         self.questionID = questionID
#         self.questionText = questionText
#         self.questionType = questionType
#         self.answers = answers
#
# class Answer:
#     def __init__(self, answerID, answerText, modifiers):
#         self.answerID = answerID
#         self.answerText = answerText
#         self.modifiers = modifiers
#
# class AnswerModifier:
#     def __init__(self, modifier, modifyBy):
#         self.modifier = modifier
#         self.modifyBy = modifyBy




















#questionNumber = int(input("What question would you like? "))
#questionAnswers = questionSeperator(data, questionNumber, 1)
#userAnswer = str(input("What is your answer? "))
#answerSeparator(questionAnswers, userAnswer, 1, 1)





#
# with open("static/test.json", 'r') as f:
#     data = json.load(f)
#     questionNum = 1
#
#     for question in data["questions"]:
#         test = question['questionText']
#         print(test)
#         print(f"\n----Question {questionNum}----\n")
#         question_id = question.get('questionID')
#         question_text = question.get('questionText')
#         print(f"id: {question_id} \n\
# it asks '{question_text}'")
#         questionNum += 1
#         answerNum = 1
#         for answer in question["answers"]:
#             print(f"\n----Answer {answerNum}----\n")
#             answer_id = answer.get('answerID')
#             answer_text = answer.get('answerText')
#             print(f"Answer ID: {answer_id} \n\
# Answer text is: {answer_text}")
#             answerNum = answerNum + 1
#             print("the answer is of type", type(answer))
#             for modifier in answer["modifiers"]:
#                 toModify = modifier.get("modifier")
#                 modificationBy = modifier.get("modifyBy")
#                 print(f"this answer will modify {toModify} by {modificationBy}")
#                 print("the modifier is of type", type(modifier))
#                 #print(modifier)
#                 # #modifierModifications = (modifier.values())
#                 # #print(type(toModify))
#                 # print(f"{toModify} will be modified by {modificationBy}")
#
#
#
#

# def answerSeparator(answerDict, desiredAnswer, currentQuestion, x):
#     if desiredAnswer == x:
#         for answer in answerDict["answers"]:
#             print(type(answer))
#             if answer.get("answerText") == desiredAnswer:
#                 answer_id = answer.get("answerID")
#                 print(answer_id)
#
#     else:
#         x += 1
#         answerSeparator(answerDict, desiredAnswer, x)


#
# def questionSeperator(questionDict, desiredQuestionNumber, x):
#     #print("Hello")
#     #print(questionDict)
#
#     # x is the recursive variable that will loop through the questions until it finds the desired question
#     # if the desired question is the same as the current loop of the function (x)
#     if desiredQuestionNumber == x:
#         # iterate through each question in the questions of the JSON file
#         for question in questionDict["questions"]:
#             # if the id of the current question is the same as the desired question
#             if question.get("questionID") == desiredQuestionNumber:
#                 question_id = question.get('questionID')
#                 question_text = question.get('questionText')
#                 print(question_text)
#                 answers = question["answers"]
#                 break
#                 # for answer in question["answers"]:
#                 #     #print(type(answer))
#                 #     answer_id = answer.get("answerID")
#                 #     answer_text = answer.get("answerText")
#                 #
#                 #     # for modifier in answer["modifiers"]:
#                 #     #     to_modify = modifier.get("modifier")
#                 #     #     modify_by = modifier.get("modifyBy")
#
#         print(type(answers))
#         print(answers)
#         return answers
#
#     else:
#         x += 1
#         questionSeperator(questionDict, desiredQuestionNumber, x)
#
#
#
#     # print(questionDict[(list(questionDict.keys())[0])])









# r = json.dumps(data)
# loaded_data = json.loads(r)





