console.log("JavaScript file loaded");

function hashPassword(password) {
  console.log("hashPassword function invoked");
  const shaObj = new jsSHA("SHA-512", "TEXT");
  shaObj.update(password);
  const hashedPassword = shaObj.getHash("HEX");
  return hashedPassword;
}

document.addEventListener("submit", function (event) {
  if (event.target && event.target.tagName === "FORM") {
    event.preventDefault();

    console.log("Form submission event triggered");

    const usernameInput = event.target.querySelector('input[name="username"]');
    const passwordInput = event.target.querySelector('input[name="password"]');
    const roleInput = event.target.querySelector('select[name="role"]'); // Add this line to get the role input
    if (!usernameInput || !passwordInput || !roleInput) {
      console.error("Username or password,  or role input not found");
      return;
    }

    const hashedPassword = hashPassword(passwordInput.value);

    fetch(event.target.action, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: usernameInput.value,
        password: hashedPassword,
        role: roleInput.value, // Include the role field in the JSON data
      }),
    })
      .then((response) => {
        if (response.ok) {
          console.log("Form submitted successfully");
          // Redirect or handle the successful response
          window.location.href = response.url; // Manually redirect to the URL received in the response
        } else {
          console.error("Error submitting form");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
});
