// JavaScript for the accordion functionality
var acc = document.getElementsByClassName("accordion");
for (var i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
}

// Get the modal
var modal = document.getElementById("editModal");

// Function to open the modal and populate the form
function openModal(id, date, time, reason, urlTemplate) {
    var url = urlTemplate.replace('0', id);  // Replace the placeholder with the actual appointment id
    document.getElementById("editForm").action = url;
    document.getElementById("editDate").value = date;
    document.getElementById("editTime").value = time;
    document.getElementById("editReason").value = reason;
    modal.style.display = "block";
}

// Function to close the modal
function closeModal() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}