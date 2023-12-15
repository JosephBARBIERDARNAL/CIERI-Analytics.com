function toggleCode(rCodeId, pythonCodeId, buttonId) {
    var rCode = document.getElementById(rCodeId);
    var pythonCode = document.getElementById(pythonCodeId);
    var button = document.getElementById(buttonId);

    // Check if R code is currently displayed
    if (rCode.style.display !== "none") {
        rCode.style.display = "none";
        pythonCode.style.display = "block";
        button.textContent = "Python";
    } else {
        rCode.style.display = "block";
        pythonCode.style.display = "none";
        button.textContent = "R";
    }
}


