const token = localStorage.getItem("token");

async function fetchUser(token) {
  try {
    if (!token) {
      return;
    }
    const response = await fetch("http://127.0.0.1:8000/api/user/auth", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    const data = await response.json();
    // console.log(data.data);
    if (data.data !== null) {
      showLogoutButton();
    } else {
      logout();
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

fetchUser(token);
