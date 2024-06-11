import Api from "./api.js"

// Gets the element with the class of question text
// To later manipulate and display the current question's text
const questionTextP = $(".question-text")
const questionAnswerP = $("#answer-container")
const showBestCountries = $(".showSuggestions")
const waitMessage = document.querySelector("#pleaseWait");
const invalidInteger = document.querySelector("#invalidInteger");

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
            // _res is the variable name of the response
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
            // document.getElementsByClassName("question-text").style.display = "none" does not work as...
            // document.getElementsByClassName delivers a nodeList
            // Could use jquery: $(".question-text").css("display", "none")
            // document.getElementsByClassName("question-text")[0].style.display = "none"
            // Changes the questionTextP element's text to the current questions text
            questionTextP.text(question.questionText)
            const questionType = question.questionType
            const answers = question.answers
            if (questionType == "Multiple Choice") {
                multipleChoiceQuestion(question, answers, travelID)
            } else if (questionType == "Integer") {
                integerQuestion(question, answers, travelID)
            } else if (questionType == "Range") {
                rangeQuestion(question, answers, travelID)
            } else {
                console.log("Unknown question")
            }
        }).catch((error) => {
            console.log("This is the error", error)
            if (error == "Error: No more questions") {
                // Wait message displayed while running the algorithm for ranking countries
                // All options are removed so that further unnecessary requests cannot be made
                removeAllChildNodes(document.getElementById("answer-container"));
                questionTextP.text("");
                $(waitMessage).show();
                Api.validateTravelID(travelID)
                    .then((_res) => {
                        if (_res.status === 404 || _res.status === 500) {
                            throw Error("No travelID/Unexpected, code:" + _res.status);
                        }
                        return _res.json(); // Returns the response further
                    })
                    .then((response_data) => {
                        // console.log("RESPONSE DATA: " + JSON.stringify(response_data));
                        if (response_data.valid === true) {
                            // When it's found a valid travel ID, redirects to the suggestions page
                            window.location.href = "/suggestions/" + travelID
                        } else {
                            console.log("Being thrown here!");
                            throw Error(response_data.message);
                        }
                    }).catch((error) => {
                        console.log("Error: " + error.message);
                        window.location.href = "/noTravel"
                })
            }
        })
}

const rangeQuestion = function (question, answers, travelID) {
    const element = document.getElementById("answer-container")
    const min_value = question.minValue
    console.log("Min Value", min_value)
    const max_value = question.maxValue
    console.log("Max Value", max_value)
    const increment = question.increment
    let middle_value = (min_value + max_value) / 2
    console.log("Middle value", middle_value)

    const slider =
        createElementX(
            "div",
            {
                "class": "rangeContainer"
            },
            [
            createElementX(
                "div",
                {
                    "class": "range"
                },
                [
                    createElementX(
                        "div",
                        {
                            "class": "sliderValue"
                        },
                        [
                            createElementX(
                                "span",
                                {
                                    "id": "slideV"
                                },
                                [
                                   document.createTextNode(middle_value)
                                ]
                            )
                        ]
                    ),
                    createElementX(
                        "div",
                        {
                            "class": "field"
                        },
                        [
                            createElementX(
                                "div",
                                {
                                    "class": "value left"
                                },
                                [
                                    document.createTextNode(min_value)
                                ]
                            ),
                            createElementX(
                                "input",
                                {
                                    "id": "slideI",
                                    "type": "range",
                                    "min": min_value,
                                    "max": max_value,
                                    "value": min_value,
                                    "step": increment
                                }
                            ),
                            createElementX(
                                "div",
                                {
                                    "class": "value right"
                                },
                                [
                                    document.createTextNode(max_value)
                                ]
                            )
                        ]
                    )
                ]
            ),
            createElementX(
                "button",
                {
                    "class": "btn btn-outline-primary submitButton",
                    "style": "text-align: center",
                    "type": "button"
                },
                [
                    document.createTextNode("Submit")
                ]
            )]
        )


    element.appendChild(slider)

    const slideValue = document.getElementById("slideV")
    const inputSlider = document.getElementById("slideI")
    let total_value = Math.abs(min_value) + Math.abs(max_value)
    var inputSliderOnInput = (() => {
        // Use of let as it's a constantly changing value, const more appropriate for a set value
        let value = inputSlider.value;
        slideValue.textContent = value;
        // Moves the value pointer as the slider is moved
        slideValue.style.left = ((value - min_value)/(max_value - min_value)) * 100 + "%"
    })


    // When the slider is moved...
    inputSlider.oninput = inputSliderOnInput
    inputSliderOnInput()


    const submitButtonX = $(".submitButton");


    submitButtonX.click(function (event) {
        console.log("submit button clicked!")
        const answerValue = inputSlider.value;
        console.log(answerValue)
        const questionID = question.questionID
        Api.sendUserResponse(questionID, answerValue, travelID).then(() => {
             nextQuestion(travelID)
        });

    })

}

const integerQuestion = function (question, answers, travelID) {
    const placeholder = question.answerPlaceholder
    const minimumValue = question.minimumValue

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
                    "min": question.minimumValue
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
        const invalidInteger = $("#invalidInteger")
        if (answerValue < minimumValue) {
            console.log("This is min", minimumValue)
            $(invalidInteger).show();
            let str_minimum_value = toString(minimumValue)
            invalidInteger.text("Please input an integer greater than or equal to " + minimumValue);
            console.log("dfgsefs")
        } else {
            $(invalidInteger).hide();
            Api.sendUserResponse(questionID, answerValue, travelID).then(() => {
                nextQuestion(travelID)
            });
        }
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
                    "class":"btn btn-outline-primary mt-3 answerButtons",
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












