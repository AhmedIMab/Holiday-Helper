import Api from "./api.js";

const select_element = document.getElementById('num-cards');
const pathname = window.location.pathname.split('/')
const travel_id = pathname[pathname.length - 1]
console.log("this is travel_ID:", travel_id)
console.log("this is TEST:")


select_element.addEventListener("change", filterDisplayedCountries)

function filterDisplayedCountries() {
    var option_value = select_element.value;
    console.log("This is the selected option value:", option_value);
    if (option_value) {
        Api.displayCountries(option_value)
            .then((_res) => {
                console.log("This is the response:", _res)
            }).catch((error) => {
                console.log("caught error:", error)
            })
    }
}
