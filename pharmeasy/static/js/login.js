// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("form");
  
    loginForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent form submission
  
      // Get the email and password values
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value.trim();
  
      // Validate email and password
      if (!email) {
        alert("Please enter your email.");
        return;
      }
  
      if (!validateEmail(email)) {
        alert("Please enter a valid email address.");
        return;
      }
  
      if (!password) {
        alert("Please enter your password.");
        return;
      }
  
      // If validation passes, submit the form (or handle login logic)
      alert("Login successful!");
      loginForm.submit(); // Uncomment this line to allow form submission
    });
  
    // Function to validate email format
    function validateEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    }
  });