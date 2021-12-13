// import $ from jQuery

class Api {
    deleteNote(noteId) {
        // fetch will send a request to the 'delete-note' endpoint
        return fetch("/notes", {
            method: "DELETE",
            // Takes JS object and turns to a string
            // Serialises the js object into JSON
            body: JSON.stringify({ noteId: noteId }),
        // after getting a response then it will.....
        });
    }


    addNote(noteValue) {
        return fetch("/notes", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({noteValue: noteValue})
        })
    }


    addCountry(countryCode) {
        return fetch("/usercountries", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({countryCode: countryCode})
        })
    }

    deleteCountry(countryCode) {
        return fetch("/usercountries", {
            method: "DELETE",
            body: JSON.stringify({countryCode: countryCode})
        })
    }


    // getQuestion(questionNumber) {
    //     return fetch("/api/questions/" + questionNumber, {
    //         method: "GET"
    //     })
    // }

    getLatestQuestion() {
        return fetch("/api/questions/nextQuestion", {
            method: "GET"
        })
    }

    // Gives travelID a default value if none is entered
    sendUserResponse(questionID, answerID, travelID = 1) {
        return fetch("userQuestionAnswer", {
            method: "POST",
            // sends the answer to the views.py function UserAnswerQuestion
            body: JSON.stringify({questionID: questionID, answerID: answerID, travelID: travelID})
        })
    }

    UserCountrySuggestions(travelID) {
        return fetch("/suggestions/" + travelID, {
            method: "GET"
        })
    }

    // getSuggestedCountries(travelID) {
    //     return fetch("/countrySuggestions", {
    //         method: "POST",
    //         body: JSON.stringify({travelID: travelID})
    //     })
    // }

}

export default new Api();

























    // addNote(noteValue) {
    //     console.log($)
    //     console.log($())
    //     $().ajax({
    //         type: "POST",
    //         url: "/notes",
    //         data: JSON.stringify(noteValue),
    //     })
    // }

