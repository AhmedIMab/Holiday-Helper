import Api from "./api.js"

// Api.testUserAndCountryScores(1).then((_res) => {
//     console.log("PASSED")
//     console.log(_res.json)
//     return _res.json
// })

const showBestCountries = $(".showSuggestions")

const waitMessage = document.querySelector("#pleaseWait");

showBestCountries.click(function (event) {
    console.log("showinggggg")
    const travelID = $("#travelIDInput").val()
    console.log("This is the travelID", travelID)
    // Wait message displayed while running the algorithm for ranking countries
    $(waitMessage).show();
    Api.UserCountrySuggestions(travelID).then((_res) => {
        console.log("PASSED")
        console.log(_res.json)
        window.location.href = "/suggestions/" + travelID
    })
})


//
// Api.getSuggestedCountries(1)
//     .then((_res) => {
//         return _res.json()
//         console.log("Hello, how are you?")
// })