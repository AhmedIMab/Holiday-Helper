import Api from "./api.js"

Api.testUserAndCountryScores(1, "US").then((_res) => {
    console.log("PASSED")
})
