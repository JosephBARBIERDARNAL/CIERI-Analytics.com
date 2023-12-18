document.addEventListener("DOMContentLoaded", function() {
    // Load the header
    fetch('bid.com/templates/header.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('header-container').innerHTML = data;
        });

    // Load the footer
    fetch('bid.com/templates/footer.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('footer-container').innerHTML = data;
        });
});