function showLoginForm() {
  document.getElementById("login-form-bg").style.visibility = "visible";
  document.getElementById("signup-form-bg").style.visibility = "hidden";
}

function showSignUpForm() {
  document.getElementById("login-form-bg").style.visibility = "hidden";
  document.getElementById("signup-form-bg").style.visibility = "visible";
}

function closeLoginForm() {
  document.getElementById("login-form-bg").style.visibility = "hidden";
}

function closeSignUpForm() {
  document.getElementById("signup-form-bg").style.visibility = "hidden";
}

function showErrorLogin(errorMessage) {
  const errorMsg = document.getElementById("login-message");
  errorMsg.textContent = errorMessage;
  errorMsg.style.color = "red";
  errorMsg.style.display = "block";
}

function showErrorMessage(errorMessage) {
  const errorMsg = document.getElementById("signup-message");
  errorMsg.textContent = errorMessage;
  errorMsg.style.color = "red";
  errorMsg.style.display = "block";
}

function showSuccessMessage(successMessage) {
  const successMsg = document.getElementById("signup-message");
  successMsg.textContent = successMessage;
  successMsg.style.color = "green";
  successMsg.style.display = "block";
}

function showLogoutButton() {
  document.getElementById("login-button").style.display = "none";
  document.getElementById("logout-button").style.display = "block";
}

function logout() {
  localStorage.removeItem("token");
  document.getElementById("login-button").style.display = "block";
  document.getElementById("logout-button").style.display = "none";
  window.location.href = "http://127.0.0.1:8000/";
}

async function submitLoginForm(event) {
  event.preventDefault();
  const email = document.getElementById("input-email").value;
  const password = document.getElementById("input-password").value;

  try {
    const response = await fetch("http://127.0.0.1:8000/api/user/auth", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const data = await response.json();
    // console.log(data);
    if (data.token) {
      localStorage.setItem("token", data.token);
      window.location.href = "http://127.0.0.1:8000/";
    } else {
      showErrorLogin(data.message);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

async function submitSignUpForm(event) {
  event.preventDefault();
  const name = document.getElementById("input-signUp-name").value;
  const email = document.getElementById("input-signUp-email").value;
  const password = document.getElementById("input-signUp-password").value;

  try {
    const response = await fetch("http://127.0.0.1:8000/api/user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, password }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const data = await response.json();
    // console.log(data);
    if (data.ok) {
      showSuccessMessage("註冊成功!");
    } else {
      showErrorMessage(data.message);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}
