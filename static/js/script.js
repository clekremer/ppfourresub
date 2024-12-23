// JavaScript for the accordion functionality
var acc = document.getElementsByClassName("accordion");
for (var i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function () {
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

// Function to open the modal and fetch data dynamically
function openModal(id, detailsUrl, editUrl) {
    fetch(detailsUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch appointment data');
            }
            return response.json();
        })
        .then(data => {
            var editForm = document.getElementById('editForm');
            var editDate = document.getElementById('editDate');
            var editTime = document.getElementById('editTime');
            var editReason = document.getElementById('editReason');

            if (editForm && editDate && editTime && editReason) {
                editForm.action = editUrl.replace('0', id); // Set edit action dynamically
                editDate.value = data.date; // ISO format from backend
                editTime.value = data.time;
                editReason.value = data.reason;
            }

            if (modal) {
                modal.style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Error fetching appointment data:', error);
            alert('Failed to load appointment details. Please try again.');
        });
}

// Function to close the modal
function closeModal() {
    if (modal) {
        modal.style.display = "none";
    }
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        closeModal();
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

// Navigation menu toggle
document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navMenu.classList.toggle('active');
        });
    }
});
