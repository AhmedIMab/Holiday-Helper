import Api from "./api.js"

const selectedCountry = document.querySelector("#selectedCountry");
const optionsContainer = document.querySelector(".options-container");
const optionsList = document.querySelectorAll(".option");
const noCountry = document.querySelector("#noCountrySelected");
const countryPrevAdded = document.querySelector("#countryAlreadyAdded")

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
        let countryCode = (o.querySelector("label"));
        countryCode = countryCode.getAttribute("for");
        // Adds the id of the selected option to the class selected
        selectedCountry.countryCode = countryCode;
        // closes the dropdown
        optionsContainer.classList.remove("active");
    });
});

const deleteCountryButton = $(".deleteCountryButton");

deleteCountryButton.click(function (event) {
    // sets the country code to the value of the selected country
    const countryCode = event.currentTarget.attributes["country-code"].value;
    // Runs the deleteCountry function in the API.js
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
                if (_res.status === 400) {
                    return _res.json().then((data) => {
                        let error = data.error;
                        throw Error(error);
                    })
                }
                else {
                    window.location.href = "/countries";
                }
            }).catch((error) => {
                $(countryPrevAdded).html(error.value);
                $(countryPrevAdded).show();
        });
    } else {
        // If no country is selected / the default value of "Select Countries..." has not been changed
        // shows the noCountry element
        $(noCountry).show();
    }
})