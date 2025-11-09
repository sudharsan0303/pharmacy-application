// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.querySelector("form");
  
    registerForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent form submission
  
      // Get form values
      const name = document.getElementById("name").value.trim();
      const email = document.getElementById("email").value.trim();
      const phone = document.getElementById("phone").value.trim();
      const password = document.getElementById("password").value.trim();
  
      // Validate form fields
      if (!name) {
        alert("Please enter your full name.");
        return;
      }
  
      if (!email) {
        alert("Please enter your email.");
        return;
      }
  
      if (!validateEmail(email)) {
        alert("Please enter a valid email address.");
        return;
      }
  
      if (!phone) {
        alert("Please enter your phone number.");
        return;
      }
  
      if (!validatePhone(phone)) {
        alert("Please enter a valid phone number.");
        return;
      }
  
      if (!password) {
        alert("Please enter your password.");
        return;
      }
  
      if (password.length < 6) {
        alert("Password must be at least 6 characters long.");
        return;
      }
  
      // If validation passes, submit the form (or handle registration logic)
      alert("Registration successful!");
      registerForm.submit(); // Uncomment this line to allow form submission
    });
  
    // Function to validate email format
    function validateEmail(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailRegex.test(email);
    }
  
    // Function to validate phone number format
    function validatePhone(phone) {
      const phoneRegex = /^[0-9]{10}$/; // Accepts 10-digit phone numbers
      return phoneRegex.test(phone);
    }
  });