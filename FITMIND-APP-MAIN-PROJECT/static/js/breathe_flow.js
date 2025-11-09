// Breathe Flow Game
let calmPoints = 0;
let isBreathing = false;
let breathStartTime = 0;
let exhalePromptShown = false;
let countdownInterval = null;

const MIN_HOLD_TIME = 10000; // 4 seconds before exhale prompt
const SCORE_VALUE = 10;
const MAX_POINTS = 50;

let calmFill = document.getElementById("calm-fill");
let scoreText = document.getElementById("score");
let feedback = document.getElementById("feedback");
let gameOver = document.getElementById("game-over");
let finalScore = document.getElementById("final-score");
let orb = document.getElementById("orb");

let fillAnimationFrame = null;
let actualFill = calmPoints / MAX_POINTS;
let targetFill = 0;
let startFill = 0;
let startTime = 0;
const INHALE_DURATION = 10000; // 10 seconds in milliseconds


// Prevent spacebar from scrolling
window.addEventListener("keydown", function (e) {
  if (e.code === "Space" && e.target === document.body) {
    e.preventDefault();
  }
});

// Handle keydown: Start inhaling when spacebar is pressed
document.addEventListener("keydown", (e) => {
  if (e.code === "Space" && !isBreathing) {
    isBreathing = true;
    breathStartTime = Date.now();
    exhalePromptShown = false;
    orb.classList.add("breathing"); // Grows the orb
    feedback.textContent = "Inhale... Hold it...";

    startFillingBar();

    countdownInterval = setInterval(() => {
      const heldTime = Date.now() - breathStartTime;
      if (!exhalePromptShown && heldTime >= MIN_HOLD_TIME) {
        exhalePromptShown = true;
        feedback.textContent = "Exhale now (release spacebar)";
      }
    }, 100);
  }
});

document.addEventListener("keyup", (e) => {
  if (e.code === "Space" && isBreathing) {
    isBreathing = false;
    orb.classList.remove("breathing");
    clearInterval(countdownInterval);
    cancelAnimationFrame(fillAnimationFrame);

    const breathDuration = Date.now() - breathStartTime;

    if (breathDuration >= MIN_HOLD_TIME) {
      calmPoints += SCORE_VALUE;
      feedback.textContent = "✅ Great job! Calm points earned.";
      actualFill = calmPoints / MAX_POINTS;
      calmFill.style.width = `${actualFill * 100}%`;
    } else {
      feedback.textContent = "⚠️ Too quick! Wait for the exhale signal.";
      reverseBar();
    }

    updateUI();
  }
});


// start filling the bar
function startFillingBar() {
  const percentPerPoint = SCORE_VALUE / MAX_POINTS; // 10/50 = 0.2
  startTime = Date.now();
  startFill = actualFill;
  targetFill = actualFill + percentPerPoint;

  function animate() {
    if (!isBreathing) return;

    const elapsed = Date.now() - startTime;
    const progress = Math.min(elapsed / INHALE_DURATION, 1); // 0 to 1
    const currentFill = startFill + (percentPerPoint * progress);

    calmFill.style.width = `${currentFill * 100}%`;
    fillAnimationFrame = requestAnimationFrame(animate);
  }

  animate();
}


// Reverse the bar animation if the user releases spacebar too early
function reverseBar() {
  const fallback = calmPoints / MAX_POINTS;

  function animate() {
    if (actualFill > fallback) {
      actualFill -= 0.01; // Slow step back
      if (actualFill < fallback) actualFill = fallback;
      calmFill.style.width = `${actualFill * 100}%`;
      requestAnimationFrame(animate);
    }
  }

  animate();
}


// Update the calm points UI and check for game over
function updateUI() {
  scoreText.textContent = `Calm Points: ${calmPoints}`;
  calmFill.style.width = `${(calmPoints / MAX_POINTS) * 100}%`;

  if (calmPoints >= MAX_POINTS) {
    endGame();
  }
}

// Show the game over screen with final score
function endGame() {
  gameOver.style.display = "block";
  finalScore.textContent = calmPoints;
}

// Restart the game and reset everything
function restartGame() {
  calmPoints = 0;
  actualFill = 0;
  targetFill = 0;
  startFill = 0;
  calmFill.style.width = "0%";
  scoreText.textContent = "Calm Points: 0";
  feedback.textContent = "Press & hold Spacebar to breathe in…";
  gameOver.style.display = "none";
}
