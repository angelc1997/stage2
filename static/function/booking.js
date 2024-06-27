async function postNewBooking() {
  try {
    // Get data
    const date = document.getElementById("attr-reserve-date").value;
    if (!date) {
      alert("請填寫日期");
      return;
    }
    const time = document.querySelector(
      "input[name='attr-reserv-time']:checked"
    ).id;

    // Set price
    let price = time === "morning" ? 2000 : 2500;

    const url = window.location.href;
    const attractionId = url.split("/").pop();

    const response = await fetch(`${baseUrl}/booking`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify({ attractionId, date, time, price }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }
    window.location.href = "/booking";
  } catch (error) {
    console.error("Error:", error);
  }
}

function showBookingCart() {
  const token = localStorage.getItem("token");
  if (!token) {
    showLoginForm();
    return;
  }

  window.location.href = "/booking";
}
