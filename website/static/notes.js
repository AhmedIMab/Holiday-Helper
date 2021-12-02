import Api from "./api.js"


// creates a variable which uses jQuery based on the "deleteNoteButton" class in the delete buttons
const deleteNoteButton = $(".deleteNoteButton");
// adds an event when the button is clicked
deleteNoteButton.click(function (event) {
    // creates a variable which access' the note-id part of the note being deleted
    const noteID = event.currentTarget.attributes["note-id"].value
    // uses the 'deleteNote' function in the Api class in api.js with the note id parameter so the function knows which note to delete
    Api.deleteNote(noteID)
        // Adds a callback when the 'promise' is done
        .then((_res) => {
        // this will reload the window
        window.location.href = "/notes";
    });

    // console.log(event.currentTarget.attributes["note-id"].value)
})


const addNoteButton = $(".addNoteButton");

addNoteButton.click(function (event) {
    const note_value = $("#noteData").val();
    Api.addNote(note_value)
        .then((_res) => {
            window.location.href = "/notes";
    });
})

