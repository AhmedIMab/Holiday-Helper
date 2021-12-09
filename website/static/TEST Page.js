import Api from "./api.js"

Api.testUserAndCountryScores(1, "AL").then((_res) => {
    console.log("PASSED")
})
