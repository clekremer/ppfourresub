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

// Prevent selecting past dates in all date inputs on page load
document.addEventListener('DOMContentLoaded', function () {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    dateInputs.forEach(input => {
        input.setAttribute('min', today);
    });
});

// Prepopulate Edit Appointment Modal
function openModal(id, date, time, reason, urlTemplate) {
    var url = urlTemplate.replace('0', id);  // Replace placeholder with actual appointment ID
    var editForm = document.getElementById('editForm');
    var editDate = document.getElementById('editDate');
    var editTime = document.getElementById('editTime');
    var editReason = document.getElementById('editReason');

    if (editForm && editDate && editTime && editReason) {
        editForm.action = url;
        editDate.value = date;
        editTime.value = time;
        editReason.value = reason;
    }

    modal.style.display = 'block';
}

// Navigation menu toggle
document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    navToggle.addEventListener('click', function () {
        navMenu.classList.toggle('active');
    });
});
