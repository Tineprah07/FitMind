// Exercise logging and charting functionality
let exerciseData = JSON.parse(sessionStorage.getItem("exerciseData")) || [];

function pageLoaded() {
    const exerciseTypeSelect = document.querySelector("#exercise-type");
    const customInput = document.querySelector("#custom-exercise");
    const ctx = document.querySelector("#progress-chart").getContext("2d");
    const suggestionsList = document.querySelector("#suggestions-list");

    let progressChart;
    let exerciseData = []; // ⏳ Keep all exercises logged in session

    // Toggle custom input
    exerciseTypeSelect.addEventListener("change", () => {
        customInput.style.display = exerciseTypeSelect.value === "Custom" ? "block" : "none";
    });

    function updateChart(data) {
        if (progressChart) progressChart.destroy();
        const labels = data.map(entry => `${entry.time} (${entry.type})`);
        const durations = data.map(entry => parseInt(entry.duration));
        progressChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels,
                datasets: [{
                    label: "Duration (mins)",
                    data: durations,
                    backgroundColor: "#00bfa5",
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true, // allows flexible resizing
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }

    function updateRecommendations(data) {
        const suggestions = {
            Cardio: ["Great for heart health!", "Try to reach 30 minutes."],
            Stretching: ["Good for flexibility.", "Stretch after every workout."],
            Strength: ["Builds muscle & boosts metabolism.", "Remember to rest."],
            Yoga: ["Mind + flexibility in balance.", "Try guided yoga sessions."],
            HIIT: ["Great fat burner!", "Alternate HIIT and rest days."],
            Pilates: ["Improves core and posture."],
            Recreational: ["Fun is fitness — enjoy!", "Do it regularly."],
            Custom: ["Great custom session!", "Stay consistent with it."]
        };
        const latest = data[data.length - 1];
        const type = latest.type;
        suggestionsList.innerHTML = "";
        (suggestions[type] || ["Stay active and consistent."]).forEach(msg => {
            const li = document.createElement("li");
            li.textContent = msg;
            suggestionsList.appendChild(li);
        });
    }

    // Handle form submit
    const form = document.getElementById("exercise-form");
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    
        const type = document.getElementById("exercise-type").value;
        const custom = document.getElementById("custom-exercise").value.trim();
        const durationInput = document.getElementById("duration").value.trim();
        const duration = parseInt(durationInput);
        const finalType = (type === "Custom" && custom) ? custom : type;
    
        if (!durationInput || isNaN(duration) || duration <= 0) {
            alert("Enter a correct time");
            return;
        }
    
        if (type === "Custom") {
            if (!custom) {
                alert("Please complete all required fields.");
                return;
            }
    
            const isOnlyText = /^[A-Za-z\s]+$/.test(custom);
            if (!isOnlyText) {
                alert("Please enter a valid exercise name");
                return;
            }
        }
    
        fetch("/exercise", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                "Exercise": finalType,
                "duration": duration
            })
        })
        .then(res => res.json())
        .then(data => {
            if (Array.isArray(data)) {
                const entry = data[0];
                const ul = document.getElementById("exercise-list");
    
                const li = document.createElement("li");
                const [datePart, timePart] = entry.time.split(" — ");
                li.classList.add("exercise-entry");

                li.innerHTML = `
                    <div class="entry-text">
                        Date: ${datePart} — Time: ${timePart}<br>
                        Exercise: ${entry.type} (${entry.duration} mins)
                    </div>
                    <button class="remove-btn" onclick="this.parentElement.remove()">🗑️ Delete</button>
                `;
                ul.prepend(li);
    
                exerciseData.push(entry);
                sessionStorage.setItem("exerciseData", JSON.stringify(exerciseData));
                updateChart(exerciseData);
                updateRecommendations(exerciseData);
    
                form.reset();
                document.querySelector(".exercise-log").scrollIntoView({ behavior: "smooth" });
            }
        })
        .catch(err => {
            console.error("Error:", err);
            alert("Something went wrong.");
        });
    });
}
