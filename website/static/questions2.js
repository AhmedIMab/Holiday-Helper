import Api from "./api.js"


// Gets the element with the class of question text
// tO later manipulate and display the current question's text
const questionTextP = $(".question-text")


const questionAnswerP = $("#answer-container")



const removeAllChildNodes = function (parent) {
    // When the parent has a child
    while (parent.firstChild) {
        // remove the child
        // removeAllChildNodes(parent.firstChild)
        parent.removeChild(parent.firstChild)
    }
}


const nextQuestion = function (event, questionID) {

    console.log("NEXT QUESTION FUNCTION")
    console.log(questionID)
    // const nextQ = parseInt(questionID) + 1
    Api.getLatestQuestion()
        .then((_res) => {
        return _res.json()
    }).then((question) => {
        removeAllChildNodes(document.getElementById("answer-container"))
        // Changes the questionTextP element's text to the current questions text
        questionTextP.text(question.questionText)
        const questionType = question.questionType
        const answers = question.answers
        if (questionType == "Multiple Choice") {
        console.log("THIS IS A MULTIPLE CHOICE QUESTION")
        multipleChoiceQuestion(event, question, answers)

        } else if (questionType == "Integer") {
            console.log("THIS IS AN INTEGER QUESTION")
            integerQuestion(event, question, answers)
        }
    })
}



function createElementX (type, attributes, children=[]) {
    // Creates an element of type (type)
    // e.g. div
    const element = document.createElement(type)
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries
    // https://javascript.info/destructuring-assignment
    // attributes will be an array
    // object.entries() returns an array of a given objects own (key, value) pairs
    // like a for loop which assigns the key to the first value in the array given
    // and the value to the 2 value in the attributes parameter array given
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



const integerQuestion = function (event, question, answers) {
    console.log(answers)
    const placeholder = question.answerPlaceholder
    console.log(placeholder)

    const element = document.getElementById("answer-container")

    const elementButton =
        createElementX(
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
                    "type": "text",
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



    // element.removeAttribute("class","container")
    // element.setAttribute("class", "input-group")
    // the second param takes an object
    // let answerEntry = createElementX("input", {"placeholder": placeholder,
    //                                                         "id": "entryInput",
    //                                                         "class": "form-control",
    //                                                         "type": "text",
    //                                                         })

    // element.appendChild(answerEntry)
    // let submitButton = createElementX("button", {"class":"btn btn-outline-primary submitButton",
    //                                                           "type": "button"})


    // const node = document.createTextNode("Submit")
    // elementButton.appendChild(submitButton)
    // submitButton.appendChild(node)

    element.appendChild(elementButton)

    const submitButtonX = $(".submitButton");

    submitButtonX.click(function (event) {
        console.log("submit button clicked!")
        const answerValue = $("#entryInput").val();
        console.log(answerValue)
        const questionID = question.questionID
        console.log(questionID)
        Api.sendUserResponse(questionID, answerValue).then(() => {
            // window.location.href = "/questions";
        }).then(() => {
            console.log("Moving onto next question?")
            nextQuestion(event, questionID)
        });

    })

    // const answerEntry = document.createElement("input")
    // answerEntry.setAttribute("placeholder", "Enter the number of people...")
    // answerEntry.setAttribute("class", "input-group input-group-lg")
    // answerEntry.setAttribute("id", "entryInput")
    // answerEntry.setAttribute("type", "text")
    // answerEntry.setAttribute("size", "30")
    // element.appendChild(answerEntry)
    // const submitButton = document.createElement("button")
    // submitButton.setAttribute("class", "bte btn-primary")
    //element.appendChild(submitButton)
}





const multipleChoiceQuestion = function (event, question, answers) {
    const element = document.getElementById("answer-container")
    const main = document.getElementById("main")
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

    // const centerAButtons = document.getElementsByClassName("centerAButtons")
    console.log("TEST")
    console.log(main)
    element.appendChild(answer_buttons)

    for (var i = 0; i < answers.length; i++) {
        // Loops through the list of dictionaries of the answers
        // sets the answer
        const answer = answers[i]
        // retrieves the answer text of the answer
        const answerText = answer.answerText
        // console.log(answer)
        // console.log(answerText)
        // creates a new button element
        const centerAButtons = document.getElementById("buttonsss");
        console.log(centerAButtons)

        const answer_button = createElementX(
                "button",
                {
                    "class":"btn btn-outline-primary answerButtons",
                    "questionID": question.questionID,
                    "answerID": answer.answerID
                },
                [
                    document.createTextNode(answerText)
                ])

        // const answer_button = document.createElement("button")
        // to add text to the button, a node is created with the answer's text
        // const node = document.createTextNode(answerText)
        // adds the node to the button element
        // answer_button.appendChild(node)
        // answer_button.classList.add('answerButtons')
        // answer_button.setAttribute("questionID", question.questionID)
        // answer_button.setAttribute("answerID", answer.answerID)
        // finds an existing div element
        // then adds the answer button (with it's text) to the element with the id "answers"
        centerAButtons.appendChild(answer_button)
    }

    const answerButton = $(".answerButtons");
    console.log(answerButton)

    answerButton.click(function (event) {
        // console.log("answerButton clicked!")
        // const answerText = event.currentTarget.innerText;
        const questionID = event.currentTarget.attributes["questionID"].value;
        const answerID = event.currentTarget.attributes["answerID"].value;
        console.log(questionID)
        console.log(answerID)
        Api.sendUserResponse(questionID, answerID).then(() => {
            // window.location.href = "/questions";
        }).then(() => {
            nextQuestion(event, questionID)
        });
        // console.log(answerText)
    })
}




Api.getLatestQuestion()
    // _res is the response (can be named anything)
    .then((_res) => {
        // console.log(_res)
        // change the body in a JSON string format to a JSON object
        return _res.json()
    }).then((question) => {
    // console.log(question)
    // Much simpler from JSON to js
    // Manipulate the object to get the question text of the question
    // .text is a js method to change the text of the element to whats in the bracket (question.questionText)
    questionTextP.text(question.questionText)
    const questionType = question.questionType
    // console.log(questionType)
    const answers = question.answers
    // console.log(answers)

    if (questionType == "Multiple Choice") {
        console.log("THIS IS A MULTIPLE CHOICE QUESTION")
        multipleChoiceQuestion(event, question, answers)

    } else if (questionType == "Integer") {
        console.log("THIS IS AN INTEGER QUESTION")
        integerQuestion(event, question, answers)
    }
})
















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












