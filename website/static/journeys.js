import Api from "./api.js"


const newJourneyButton = $(".newJourney")


newJourneyButton.click(function () {
    console.log("Hello")
    Api.newTravel()
        .then((_res) => {
            return _res.json()
        }).then((travelID) => {
            console.log("This is the newest travelID", travelID)
            window.location.href = "/questions";
            console.log("after href")
        })
})