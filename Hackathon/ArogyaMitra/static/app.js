let step = 0;
const steps = document.querySelectorAll(".step");
const bar = document.querySelector(".progress-bar");

function showStep(n) {
  steps.forEach((s, i) => s.classList.toggle("active", i === n));
  bar.style.width = ((n + 1) / steps.length) * 100 + "%";
}

function nextStep() {
  if (step < steps.length - 1) {
    step++;
    showStep(step);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  showStep(step);

  const text = "Hi, I am ArogyaMitra 🤖. I will help assess your health.";
  let i = 0;
  function typeEffect() {
    if (i < text.length) {
      document.getElementById("aiText").innerHTML += text.charAt(i);
      i++;
      setTimeout(typeEffect, 40);
    }
  }
  typeEffect();
});
