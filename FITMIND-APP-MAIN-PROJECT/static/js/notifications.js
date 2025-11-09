// FitMind App - Notifications Script

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

// Notification Inputs
const addNotificationBtn = document.querySelector("#add-notification");
const activityInput = document.querySelector("#activity-input");
const activityTime = document.querySelector("#activity-time");
const notificationList = document.querySelector("#notification-list");

// Load saved reminders
let notifications = JSON.parse(localStorage.getItem("userNotifications")) || [];

// Add New Notification
addNotificationBtn?.addEventListener("click", () => {
    const activity = activityInput.value.trim();
    const time = activityTime.value;

    if (activity && time) {
        notifications.push({ activity, time, notified: false });
        localStorage.setItem("userNotifications", JSON.stringify(notifications));
        renderNotifications();
        activityInput.value = "";
        activityTime.value = "";
    } else {
        alert("Please enter an activity and select a time.");
    }
});

// Render Notification List
function renderNotifications() {
    notificationList.innerHTML = "";
    notifications.forEach((notification, index) => {
        notificationList.innerHTML += `
            <li>${notification.activity} - ${formatTime(notification.time)}
                <button class="delete-btn" onclick="deleteNotification(${index})">🗑️ Delete</button>
            </li>
        `;
    });
}

// Delete Notification
window.deleteNotification = function (index) {
    notifications.splice(index, 1);
    localStorage.setItem("userNotifications", JSON.stringify(notifications));
    renderNotifications();
};

// Format Time to AM/PM
function formatTime(time) {
    const [hours, minutes] = time.split(":");
    const ampm = hours >= 12 ? "PM" : "AM";
    const formattedHours = hours % 12 || 12;
    return `${formattedHours}:${minutes} ${ampm}`;
}

// Check for Due Reminders
function checkNotifications() {
    const now = new Date();
    const currentTime = `${String(now.getHours()).padStart(2, "0")}:${String(now.getMinutes()).padStart(2, "0")}`;

    console.log("🕒 Checking time:", currentTime);
    console.log("📋 Current Reminders:", notifications);

    notifications.forEach((notification, index) => {
        console.log(`⏰ Comparing ${notification.time} to ${currentTime}`);
        if (notification.time === currentTime && !notification.notified) {
            console.log("🔔 MATCHED! Triggering:", notification.activity);
            showNotification(notification.activity);
            notifications[index].notified = true;
            localStorage.setItem("userNotifications", JSON.stringify(notifications));
        }
    });
}

// Trigger Reminder
function showNotification(activity) {
    showReminderPopup(activity);

    if (Notification.permission === "granted") {
        new Notification("FitMind Reminder", {
            body: `Time for "${activity}"!`,
            icon: "images/notification.png"
        });
    }
}

// Show Popup and Sound
function showReminderPopup(activity) {
    const popup = document.getElementById("reminder-popup");
    const message = document.getElementById("reminder-message");
    const sound = document.getElementById("reminder-sound");

    if (popup && message && sound) {
        message.textContent = `⏰ Reminder: ${activity}`;
        popup.style.display = "block";
        sound.currentTime = 0;
        sound.play().catch((e) => console.warn("Sound play blocked:", e));
    } else {
        console.error("Popup element or sound is missing from the page.");
    }
}

// Close Popup
window.closeReminderPopup = function () {
    const popup = document.getElementById("reminder-popup");
    popup.classList.add("hidden");
    setTimeout(() => {
        popup.style.display = "none";
        popup.classList.remove("hidden");
    }, 300);
};

// Ask for Notification Permission
if (Notification.permission !== "granted") {
    Notification.requestPermission();
}

// Start Checking and Load UI
renderNotifications();
setInterval(checkNotifications, 10000); // Check every 10s for testing

