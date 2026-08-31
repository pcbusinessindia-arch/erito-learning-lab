const startButton = document.getElementById("startButton");
const lessonPopup = document.getElementById("lessonPopup");
const closeButton = document.getElementById("closeButton");

startButton.addEventListener("click", function () {
    lessonPopup.style.display = "block";
});

closeButton.addEventListener("click", function () {
    lessonPopup.style.display = "none";
});