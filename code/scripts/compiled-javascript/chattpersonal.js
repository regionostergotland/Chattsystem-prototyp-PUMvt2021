// Declares io so not to recieve error when compiling
var socket;
var modal = document.getElementById("myModal");
// Get the button that opens the modal
var btn = document.getElementById("authButton");
var nameInput = document.getElementById("nameInput");
btn.addEventListener("click", (e) => {
    if (nameInput.value != "") {
        console.log(nameInput.value);
        modal.style.display = "none";
        socket.emit('details_assignment', {
            name: nameInput.value, backgroundColor: "red", userIconSource: "/images/user.png", role: "personal"
        });
        socket.emit('authenticate');
    }
});
// Defines the different components
modal.style.display = "block";
