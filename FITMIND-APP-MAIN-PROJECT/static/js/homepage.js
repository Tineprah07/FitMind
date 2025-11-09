
// ✅ 🔔 Flash Message Popup
const flashPopup = document.getElementById("flash-popup");
if (flashPopup) {
    flashPopup.style.display = "block";
    setTimeout(() => {
    flashPopup.style.display = "none";
    }, 3000);
}

// Real-time Greeting Message
const greetingEl = document.getElementById("greeting-text");
function getGreeting() {
    const now = new Date();
    const hour = now.getHours();

    if (hour < 12) return "Good Morning";
    if (hour < 18) return "Good Afternoon";
    return "Good Evening";
}

if (greetingEl) {
    greetingEl.textContent = getGreeting();
}

