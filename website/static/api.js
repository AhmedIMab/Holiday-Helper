class Api {
    addCountry(countryCode) {
        // fetch will send a request to the 'delete-note' endpoint
        return fetch("/usercountries", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            // Takes JS object and turns to a string
            // Serialises the js object into JSON
            body: JSON.stringify({countryCode: countryCode})
        })
    }

    deleteCountry(countryCode) {
        return fetch("/usercountries", {
            method: "DELETE",
            body: JSON.stringify({countryCode: countryCode})
        })
    }

    getLatestQuestion(travelID) {
        return fetch("/api/questions/nextQuestion/" + travelID, {
            method: "GET"
        })
    }

    sendUserResponse(questionID, answerID, travelID) {
        console.log("HERE")
        return fetch("/userQuestionAnswer", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            // sends the answer to the views.py function /UserAnswerQuestion
            body: JSON.stringify({questionID: questionID, answerID: answerID, travelID: travelID})
        })
    }

    newTravel() {
        return fetch("travelID", {
            method: "GET"
        })
    }


    userCountrySuggestions(travelID) {
        return fetch("/suggestions/" + travelID, {
            method: "GET"
        })
    }

    validateTravelID(travelID) {
        return fetch("/validateTravelID/" + travelID, {
            method: "GET"
        })
    }

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

