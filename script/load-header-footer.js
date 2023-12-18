document.addEventListener("DOMContentLoaded", function() {
    // Load the header
    fetch('/templates/header.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header-container').innerHTML = data;
        });

    // Load the footer
    fetch('/templates/footer.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('footer-container').innerHTML = data;
        });
});