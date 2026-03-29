const countEl = document.getElementById("count");
const incBtn = document.getElementById("increment");
const decBtn = document.getElementById("decrement");
const resetBtn = document.getElementById("reset");

let count = 0;

function render() {
  countEl.textContent = count;
}

incBtn.addEventListener("click", () => {
  count += 1;
  render();
});

decBtn.addEventListener("click", () => {
  count -= 1;
  render();
});

resetBtn.addEventListener("click", () => {
  count = 0;
  render();
});

const form = document.getElementById("name-form");
const nameInput = document.getElementById("name-input");
const greetingEl = document.getElementById("greeting");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const name = nameInput.value.trim() || "frie nd";
  greetingEl.textContent = `Hello, ${name}!`;
});
