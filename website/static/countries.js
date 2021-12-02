import Api from "./api.js"


const selectedCountry = document.querySelector("#selectedCountry");
const optionsContainer = document.querySelector(".options-container");

const optionsList = document.querySelectorAll(".option");

const noCountry = document.querySelector("#noCountrySelected");


// When clicked...
selectedCountry.addEventListener("click", () => {
  // it will toggle the countries dropdown by adding the class 'active' to it
  optionsContainer.classList.toggle("active");
});


// For each element in the list referencing every element with variable 'o'
optionsList.forEach(o => {
  // adds an event listener for when each element ('o') is clicked
    o.addEventListener("click", () => {
        // changes the element which has 'selected' to have the label of the clicked element (i.e. changes the top part of select box to clicked country)
        $(noCountry).hide()
        selectedCountry.innerHTML = o.querySelector("label").innerHTML;
        selectedCountry.countryName = selectedCountry.innerHTML
        let testCode = (o.querySelector("label"));
        testCode = testCode.getAttribute("for");
        // Adds the id of the selected option to the class selected
        selectedCountry.countryCode = testCode;
        // closes the dropdown
        optionsContainer.classList.remove("active");
    });
});



const deleteCountryButton = $(".deleteCountryButton");

deleteCountryButton.click(function (event) {
    console.log("HELLO")
    const countryCode = event.currentTarget.attributes["country-code"].value;
    console.log(countryCode)
    console.log(event.currentTarget.attributes)
    Api.deleteCountry(countryCode)
        .then((_res) => {
                window.location.href = "/countries";
        });

})



const addCountryButton = $(".addCountryButton");


addCountryButton.click(function (event) {
    // Only check second condition if first one is null (short-circuit check)
    if (selectedCountry.countryCode && selectedCountry.countryName) {
        Api.addCountry(selectedCountry.countryCode)
            .then((_res) => {
                window.location.href = "/countries";
            });
    } else {
        $(noCountry).show();
    }

    console.log(selectedCountry.countryCode)
    console.log(selectedCountry.countryName)
    /*    const country_name_selected = $(".optionSelected").text();
        console.log(country_name_selected)*/
    /*    const country_code_selected = event.currentTarget.attributes
        console.log(country_code_selected)
        const country_name_selected = $("#optionSelected").text().trim();
        console.log(country_name_selected)*/
})


