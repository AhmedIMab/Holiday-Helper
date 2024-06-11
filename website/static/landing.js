import Api from "./api.js";

const guest_journey_button = document.getElementById("guest-journey-button");

guest_journey_button.addEventListener("click", function () {
    console.log("Starting a new guest journey")
    Api.newTravel()
        .then((_res) => {
            return _res.json()
        }).then((travelID) => {
            console.log("This is the newest travelID:", travelID)
            window.location.href = "/questions/" + travelID;
            return travelID
    })
});