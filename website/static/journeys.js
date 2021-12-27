import Api from "./api.js"

const newJourneyButton = $(".newJourney")
const journeyButton = $(".travel")
const waitMessage = $("#pleaseWait");


newJourneyButton.click(function () {
    console.log("Hello")
    Api.newTravel()
        .then((_res) => {
            return _res.json()
        }).then((travelID) => {
            console.log("This is the newest travelID", travelID)
            window.location.href = "/questions/" + travelID;
            return travelID
        })
})


journeyButton.click(function (event) {
    const travelID = event.currentTarget.id;
    console.log(travelID)
    Api.getLatestQuestion(travelID)
        .then((_res) => {
            // If there is a Not Acceptable error (code: 406)
            if (_res.status === 406) {
                // Generates an error object which says the message "No more questions"
                // as this status code will only be returned by views.py when there are no more questions
                throw Error("No more questions");
            }
            else {
                console.log("TEST")
                window.location.href = "/questions/" + travelID
            }
        }).catch((error) => {
            console.log("This is the error", error)
            if (error == "Error: No more questions") {
                // Wait message displayed while running the algorithm for ranking countries
                $(waitMessage).show();
                Api.userCountrySuggestions(travelID)
                    // Gets the response from the userCountrySuggestions API function
                    .then(() => {
                        window.location.href = "/suggestions/" + travelID
                    })
            }
        })
})



