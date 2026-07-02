

document.addEventListener("DOMContentLoaded", function () {

    console.log("Task Management System Loaded");

    const searchInput = document.getElementById("searchInput");

    if (searchInput) {

        searchInput.addEventListener("keyup", function () {

            let filter = searchInput.value.toLowerCase();

            let rows = document.querySelectorAll("#taskTable tbody tr");

            rows.forEach(function (row) {

                let text = row.innerText.toLowerCase();

                if (text.indexOf(filter) > -1) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }

            });

        });

    }


    const alertBox = document.querySelector(".alert");

    if (alertBox) {

        setTimeout(function () {

            alertBox.style.transition = "0.5s";
            alertBox.style.opacity = "0";

            setTimeout(function () {
                alertBox.remove();
            }, 500);

        }, 3000);

    }


    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(function (button) {

        button.addEventListener("click", function (e) {

            let confirmDelete = confirm("Are you sure you want to delete this task?");

            if (!confirmDelete) {
                e.preventDefault();
            }

        });

    });


    let rows = document.querySelectorAll("#taskTable tbody tr");

    rows.forEach(function (row) {

        let dueCell = row.cells[5];

        if (!dueCell) return;

        let dueDate = new Date(dueCell.innerText);

        let today = new Date();

        today.setHours(0, 0, 0, 0);

        if (dueDate < today) {

            row.style.background = "#ffe6e6";

        }

    });

    const cards = document.querySelectorAll(".card");

    cards.forEach(function (card) {

        card.addEventListener("mouseenter", function () {

            card.style.transform = "translateY(-8px) scale(1.02)";

        });

        card.addEventListener("mouseleave", function () {

            card.style.transform = "translateY(0px) scale(1)";

        });

    });

    const inputs = document.querySelectorAll("input, textarea, select");

    inputs.forEach(function (input) {

        input.addEventListener("focus", function () {

            input.style.boxShadow = "0 0 8px rgba(78,84,200,0.4)";

        });

        input.addEventListener("blur", function () {

            input.style.boxShadow = "none";

        });

    });

});



function validateTaskForm() {

    let title = document.querySelector("input[name='title']").value.trim();

    let description = document.querySelector("textarea[name='description']").value.trim();

    if (title === "") {

        alert("Task title cannot be empty.");
        return false;

    }

    if (description === "") {

        alert("Task description cannot be empty.");
        return false;

    }

    return true;

}



function validateRegisterForm() {

    let password = document.querySelector("input[name='password']").value;

    let confirm = document.querySelector("input[name='confirm_password']").value;

    if (password.length < 6) {

        alert("Password should be at least 6 characters.");

        return false;

    }

    if (password !== confirm) {

        alert("Passwords do not match.");

        return false;

    }

    return true;

}



function togglePassword(id) {

    let input = document.getElementById(id);

    if (input.type === "password") {

        input.type = "text";

    } else {

        input.type = "password";

    }

}



function setTodayDate() {

    let dateInput = document.querySelector("input[type='date']");

    if (!dateInput) return;

    let today = new Date();

    let day = String(today.getDate()).padStart(2, "0");

    let month = String(today.getMonth() + 1).padStart(2, "0");

    let year = today.getFullYear();

    dateInput.min = `${year}-${month}-${day}`;

}

setTodayDate();