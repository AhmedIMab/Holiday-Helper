import Api from "./api.js"

// Gets the element with the class of question text
// To later manipulate and display the current question's text
const questionTextP = $(".question-text")
const questionAnswerP = $("#answer-container")
const showBestCountries = $(".showSuggestions")
const waitMessage = document.querySelector("#pleaseWait");


const removeAllChildNodes = function (parent) {
    // When the parent has a child
    while (parent.firstChild) {
        // remove the child
        // removeAllChildNodes(parent.firstChild)
        parent.removeChild(parent.firstChild)
    }
}

function createElementX (type, attributes, children=[]) {
    // Creates an element of type (type)
    // e.g. div
    const element = document.createElement(type)
    // attributes will be an array
    // object.entries() returns an array of a given objects own (key, value) pairs
    // like a for loop which assigns the key to the first value in the array given
    // and the value to the 2nd value in the attributes parameter array given
    for (const [key, value] of Object.entries(attributes))
    {
        element.setAttribute(key, value)
        // Assign keys and values to object
        // could use element[key] = value
    }

    // For every child element in the list of children
    for (const child of children) {
        // adds the child to the element
        element.appendChild(child)
    }

    return element
}

const nextQuestion = function (travelID) {
    Api.getLatestQuestion(travelID)
        .then((_res) => {
            // If there is a Not Acceptable error (code: 406)
            if(_res.status === 406) {
                // Generates an error object which says the message "No more questions"
                // as this status code will only be returned by views.py when there are no more questions
                throw Error("No more questions");
            }
            return _res.json()
        }).then((question) => {
            // 'question' here is the same as _res.json
            // Removes all the old answers
            removeAllChildNodes(document.getElementById("answer-container"))
            removeAllChildNodes(document.getElementsByClassName("helper-text"))
            // Changes the questionTextP element's text to the current questions text
            questionTextP.text(question.questionText)
            const questionType = question.questionType
            const answers = question.answers
            if (questionType == "Multiple Choice") {
                multipleChoiceQuestion(question, answers, travelID)

            } else if (questionType == "Integer") {
                integerQuestion(question, answers, travelID)
            }
        }).catch((error) => {
            console.log("This is the error", error)
            if (error == "Error: No more questions") {
                // Wait message displayed while running the algorithm for ranking countries
                $(waitMessage).show();
                Api.userCountrySuggestions(travelID)
                // Gets the response from the userCountrySuggestions API function
                .then((_res) => {
                    // If there is a not found error (code: 404)
                    if(_res.status === 404) {
                        // Generates an error object which says the message "No travelID"
                        throw Error("No travelID");
                    }
                    return _res
                })
                .then((_res) => {
                    console.log("PASSED")
                    console.log(_res.json)
                    window.location.href = "/suggestions/" + travelID
                }).catch((error) => {
                    // If the error is the same as the error above (no travelID)
                    if (error == "Error: No travelID") {
                        console.log("Error")
                        // Sends the user to the no travel ID page which explains the problem
                        window.location.href = "/noTravel"
                    }
                })
            }
        })
}


const integerQuestion = function (question, answers, travelID) {
    const placeholder = question.answerPlaceholder

    const element = document.getElementById("answer-container")

    const elementButton =
        createElementX(
        // the second param takes a dictionary object
        "div",
        {
            "align":"center",
            "id": "submit-container",
            "class": "input-group"
        },
            [
            createElementX(
                "input",
                {
                    "placeholder": placeholder,
                    "id": "entryInput",
                    "class": "form-control",
                    "type": "number",
                }),
            createElementX(
                "button",
                {
                    "class":"btn btn-outline-primary submitButton",
                    "type": "button"
                },
                [
                    document.createTextNode("Submit")
                ])
            ])


    element.appendChild(elementButton)

    const submitButtonX = $(".submitButton");

    submitButtonX.click(function (event) {
        console.log("submit button clicked!")
        const answerValue = $("#entryInput").val();
        const questionID = question.questionID
        Api.sendUserResponse(questionID, answerValue, travelID).then(() => {
            nextQuestion(travelID)
        });

    })
}


const multipleChoiceQuestion = function (question, answers, travelID) {
    const element = document.getElementById("answer-container")
    const questionContainer = document.getElementById("question-container")

    const answer_buttons = createElementX(
            "section",
            {
                "class":"row"
            },[
                createElementX(
                    "div",
                    {
                        "id":"buttonsss",
                        "class": "col centerAButtons"
                    }
                )
            ])

    element.appendChild(answer_buttons)

    const helper = question.questionHelper

    if (helper == "") {
        // Do nothing
    }
    else {
        const question_helper = createElementX(
            "p",
            {
                "align": "center",
                "class": "pt-3 helper-text",
                "id": "q-helper"
            },
            [
                document.createTextNode(helper)
            ])
        answer_buttons.appendChild(question_helper)
    }

    for (let i = 0; i < answers.length; i++) {
        // Loops through the list of dictionaries of the answers
        // sets the answer
        const answer = answers[i]
        // retrieves the answer text of the answer
        const answerText = answer.answerText
        const centerAButtons = document.getElementById("buttonsss");

        // creates a new button element
        const answer_button = createElementX(
                "button",
                {
                    "class":"btn btn-outline-primary answerButtons",
                    "questionID": question.questionID,
                    "answerID": answer.answerID
                },
                [
                    // Adds the answer text
                    document.createTextNode(answerText)
                ])

        centerAButtons.appendChild(answer_button)
    }

    const answerButton = $(".answerButtons");

    answerButton.click(function (event) {
        const questionID = event.currentTarget.attributes["questionID"].value;
        const answerID = event.currentTarget.attributes["answerID"].value;
        Api.sendUserResponse(questionID, answerID, travelID).then(() => {
            // After it runs the sendUserResponse function in api.js
            // runs the nextQuestion function which displays the next question
            nextQuestion(travelID)
        });
    })
}

const travelElement = document.querySelector("#travelElement");
const travelID = travelElement.attributes["travelID"].value;
console.log(travelID);

// shows the next question the user should get
nextQuestion(travelID);






// Api.getLatestQuestion()
//     // _res is the response (can be named anything)
//     .then((_res) => {
//
//         // console.log(_res)
//         // change the body in a JSON string format to a JSON object
//         return _res.json()
//     }).then((question) => {
//     // console.log(question)
//     // Much simpler from JSON to js
//     // Manipulate the object to get the question text of the question
//     // .text is a js method to change the text of the element to whats in the bracket (question.questionText)
//     questionTextP.text(question.questionText)
//     const questionType = question.questionType
//     // console.log(questionType)
//     const answers = question.answers
//     // console.log(answers)
//
//     if (questionType == "Multiple Choice") {
//         console.log("THIS IS A MULTIPLE CHOICE QUESTION")
//         multipleChoiceQuestion(event, question, answers)
//
//     } else if (questionType == "Integer") {
//         console.log("THIS IS AN INTEGER QUESTION")
//         integerQuestion(event, question, answers)
//     }
// })
















// }).then(() => {
//     const answerButton = $(".answerButtons");
//     console.log(answerButton)
//
//     answerButton.click(function (event) {
//         // console.log("answerButton clicked!")
//         // const answerText = event.currentTarget.innerText;
//         const questionID = event.currentTarget.attributes["questionID"].value;
//         const answerID = event.currentTarget.attributes["answerID"].value;
//         console.log(questionID)
//         console.log(answerID)
//         Api.sendUserResponse(questionID, answerID).then(() => {
//             window.location.href = "/questions";
//         });
//         // console.log(answerText)
//     })
// })












