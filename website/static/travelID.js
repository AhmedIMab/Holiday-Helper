import Api from "./api.js"

const showBestCountries = $(".showSuggestions")

const waitMessage = document.querySelector("#pleaseWait");

showBestCountries.click(function (event) {
    const travelID = $("#travelIDInput").val()
    console.log("This is the travelID", travelID)
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
})
