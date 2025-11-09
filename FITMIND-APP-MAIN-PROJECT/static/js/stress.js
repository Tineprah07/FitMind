// Detect when the user navigates back to this page (e.g., after visiting Breathe Flow)
// If the page was restored from the back/forward cache reload the latest logs via AJAX
window.addEventListener("pageshow", function(event) {
    if (event.persisted || (window.performance && performance.getEntriesByType("navigation")[0].type === "back_forward")) {
        location.reload();
    }
});

function pageLoaded(flaskData) {
    let data = JSON.parse(flaskData);
    const relaxationList = document.getElementById("relaxation-list");
    relaxationList.innerHTML = "";  // clear old ones

    const suggestions = {
        1: [
            "You're in a great space — keep it up!",
            "Maintain your calm with a nature walk or some gentle stretches."
        ],
        2: [
            "You're doing okay. Try 5 minutes of mindful breathing.",
            "Listen to calming music or take a short digital break."
        ],
        3: [
            "You're feeling in-between. Try journaling your thoughts.",
            "Step outside for a quick walk or hydrate and reset.",
            `Visit the <a href="${breatheFlowURL}"><i class="fas fa-wind"></i> Breathe Flow</a> page for guided relaxation.`
        ],
        4: [
            "You're under pressure — try a calming breathing exercise.",
            "Consider doing a 10-minute meditation or yoga session.",
            `Visit the <a href="${breatheFlowURL}"><i class="fas fa-wind"></i> Breathe Flow</a> page for guided relaxation.`
        ],
        5: [
            "You're overwhelmed. Pause and breathe deeply.",
            "Talk to someone you trust, or listen to a guided meditation.",
            `Visit the <a href="${breatheFlowURL}"><i class="fas fa-wind"></i> Breathe Flow</a> page for guided relaxation.`
        ]
    };

    if (data.length > 0) {
        const latestEntry = data[data.length - 1];
        const rating = parseInt(latestEntry.rating);

        if (suggestions[rating]) {
            suggestions[rating].forEach(suggestion => {
                const li = document.createElement("li");
                li.innerHTML = suggestion;
                relaxationList.appendChild(li);
            });
        } else {
            const li = document.createElement("li");
            li.textContent = "No recommendations available for this level.";
            relaxationList.appendChild(li);
        }
    }
}


// Delete Stress Entry
function deleteStressEntry(id, button) {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    fetch(`/stress/delete/${id}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken 
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            const entry = button.closest('.stress-entry');
            entry.classList.add("removed");
            setTimeout(() => entry.remove(), 200);
        } else {
            alert("Error deleting entry: " + (result.error || ""));
        }
    })
    .catch(err => {
        console.error("Error:", err);
        alert("Something went wrong. Please try again.");
    });
}

// Unified delete button handler using data-id
document.addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-btn")) {
        const button = event.target;
        const id = button.dataset.id;
        if (id) {
            deleteStressEntry(id, button);
        } else {
            console.error("No ID found on delete button.");
        }
    }
});


// Stress Level Form Submission
const form = document.getElementById("stress-form");
const csrfToken = document.querySelector('input[name="csrf_token"]').value;

form.addEventListener("submit", function (e) {
    e.preventDefault(); // stop page reload

    const level = document.querySelector('input[name="stress-level"]:checked');
    const cause = document.querySelector("#stress-cause").value.trim();
    const notes = document.querySelector("#additional-notes").value.trim();

    if (!level) {
        alert("Please select a stress level.");
        return;
    }

    if (!cause) {
        alert("Please enter a stress cause.");
        return;
    }
    
    const isValidCause = /^[A-Za-z\s]+$/.test(cause);
    if (!isValidCause) {
        alert("Please enter a valid stress cause (letters only)");
        return;
    }    

    fetch("/stress", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            "stress-level": level.value,
            "stress-cause": cause,
            "additional-notes": notes
        })
    })
    .then(res => res.text())
    .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const updatedList = doc.querySelector("#stress-list");
        const updatedSuggestions = doc.querySelector("#relaxation-list");
        const newHeader = doc.querySelector("#recommendation-header");

        document.querySelector("#stress-list").innerHTML = updatedList.innerHTML;
        document.querySelector("#relaxation-list").innerHTML = updatedSuggestions.innerHTML;
        if (newHeader) {
            document.querySelector("#recommendation-header").textContent = newHeader.textContent;
        }

        // Reset the form
        form.reset();

        // Smooth scroll to logs
        const logSection = document.querySelector(".stress-log");
        if (logSection) {
            logSection.scrollIntoView({ behavior: "smooth" });
        }

        // Highlight newest log entry
        const lastEntry = document.querySelector("#stress-list li:last-child");
        if (lastEntry) {
            lastEntry.classList.add("new");
        }

        // Load fresh data for updated recommendations
        fetch("/get-latest-logs")
            .then(res => res.json())
            .then(data => {
                pageLoaded(JSON.stringify(data));
        });
    })
    .catch(err => {
        console.error("Failed to log stress:", err);
        alert("Something went wrong.");
    });
});

