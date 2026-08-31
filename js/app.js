const startButton = document.getElementById("startButton");
const lessonPopup = document.getElementById("lessonPopup");
const closeButton = document.getElementById("closeButton");
const exampleButton = document.getElementById("exampleButton");
const sqlExample = document.getElementById("sqlExample");

startButton.addEventListener("click", function () {
    lessonPopup.style.display = "block";
});

closeButton.addEventListener("click", function () {
    lessonPopup.style.display = "none";
});

exampleButton.addEventListener("click", function () {
    sqlExample.textContent = "SELECT name, city\nFROM customers;";
});