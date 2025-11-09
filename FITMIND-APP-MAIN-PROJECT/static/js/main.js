// This file contains the main JavaScript code for the FITMIND web application.
// It handles sidebar toggling, notification reminders, and user interactions.

// === SIDEBAR TOGGLE ===
const menuBtn = document.querySelector("#menu-icon");
const menuBox = document.querySelector("#menu-box");

if (menuBtn && menuBox) {
    menuBtn.addEventListener("click", function (event) {
        event.stopPropagation();
        menuBox.classList.toggle("active");
    });

    document.addEventListener("click", function (event) {
        if (!menuBox.contains(event.target) && !menuBtn.contains(event.target)) {
            menuBox.classList.remove("active");
        }
    });
}

// === GLOBAL REMINDER POPUP ===
let notifications = JSON.parse(localStorage.getItem("userNotifications")) || [];

function checkNotifications() {
    const now = new Date();
    const currentTime = `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;

    notifications.forEach((notification, index) => {
        if (notification.time === currentTime && !notification.notified) {
            showReminderPopup(notification.activity);
            notifications[index].notified = true;
            localStorage.setItem("userNotifications", JSON.stringify(notifications));
        }
    });
}

function showReminderPopup(activity) {
    const popup = document.getElementById("reminder-popup");
    const message = document.getElementById("reminder-message");
    const sound = document.getElementById("reminder-sound");

    if (popup && message && sound) {
        message.textContent = `⏰ Reminder: ${activity}`;
        popup.style.display = "block";
        sound.currentTime = 0;
        sound.play().catch(e => console.warn("Sound play blocked:", e));
    } else {
        console.error("Popup or sound element is missing.");
    }
}

window.closeReminderPopup = function () {
    const popup = document.getElementById("reminder-popup");
    if (popup) {
        popup.classList.add("hidden");
        setTimeout(() => {
            popup.style.display = "none";
            popup.classList.remove("hidden");
        }, 300);
    }
};

// Ask permission once
if (Notification.permission !== "granted") {
    Notification.requestPermission();
}

// Start reminder check
setInterval(checkNotifications, 10000); // Every 10 seconds

