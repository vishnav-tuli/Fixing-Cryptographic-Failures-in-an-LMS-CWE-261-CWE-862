console.log("JavaScript2 file loaded");

// Define hashPassword function
function hashPassword(password) {
  console.log("hashPassword function invoked");
  const shaObj = new jsSHA("SHA-512", "TEXT"); // Change SHA-1 to SHA-512
  shaObj.update(password);
  const hashedPassword = shaObj.getHash("HEX");
  return hashedPassword;
}

// Use DOMContentLoaded event listener to ensure the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Access the login form and attach a submit event listener
  document
    .getElementById("loginForm")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent default form submission

      // Get the username and password inputs from the form
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;

      // Hash the password using SHA-512
      const hashedPassword = hashPassword(password);

      // Log the username and hashed password (for debugging)
      console.log("Username:", username);
      console.log("Hashed Password:", hashedPassword);

      // Send the form data as a JSON payload
      fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: hashedPassword,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.message) {
            document.getElementById("message").textContent = data.message;
            // Redirect or handle the successful response
            window.location.href = "/courses"; // Redirect to courses page after successful login
          } else {
            document.getElementById("message").textContent = data.error;
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
});
