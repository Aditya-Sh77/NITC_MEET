document.getElementById("register-btn").addEventListener("click", () => {
    // Redirect to the registration page
    window.location.href = "/templates/register.html";
});
document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault(); // Prevent default form submission

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    

    try {
        // Send a POST request to the server with the email and password
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });

        const data = await response.json();

        if (response.ok) {
            // Redirect to the welcome page if login is successful
            window.location.href = data.redirect;
        } else {
            // Display error message if login fails
            document.getElementById("message").textContent = data.message;
            document.getElementById("message").style.color = "red";
        }
    } catch (error) {
        console.error('Login error:', error);
        document.getElementById("message").textContent = "An error occurred during login.";
        document.getElementById("message").style.color = "red";
    }
});


