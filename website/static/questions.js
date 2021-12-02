import Api from "./api.js"

const questionTextP = $(".question-text")

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
    console.log(questionType)
    const answers = question.answers
    console.log(answers)

    if (questionType == "Multiple Choice") {
        console.log("THIS IS A MULTIPLE CHOICE QUESTION")
    }

    else if (questionType == "Integer") {
        console.log("THIS IS AN INTEGER QUESTION")
    }

    for (var i = 0; i < answers.length; i++) {
        // Loops through the list of dictionaries of the answers
        // sets the answer
        const answer = answers[i]
        // retrieves the answer text of the answer
        const answerText = answer.answerText
        // console.log(answer)
        // console.log(answerText)
        // creates a new button element
        const answer_button = document.createElement("button")
        // to add text to the button, a node is created with the answer's text
        const node = document.createTextNode(answerText)
        // adds the node to the button element
        answer_button.appendChild(node)
        answer_button.classList.add('answerButtons')
        answer_button.setAttribute("questionID", question.questionID)
        answer_button.setAttribute("answerID", answer.answerID)
        // finds an existing div element
        const element = document.getElementById("answer-container")
        // then adds the answer button (with it's text) to the element with the id "answers"
        element.appendChild(answer_button)
        // console.log(answers)
    }

}).then(() => {
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
            window.location.href = "/questions";
        });
        // console.log(answerText)
    })
})












