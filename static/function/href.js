const baseUrl = "http://127.0.0.1:8000/api";

window.onload = async function () {
  try {
    const token = localStorage.getItem("token");
    if (!token) {
      window.location.href = "http://127.0.0.1:8000/";
    }
    showLogoutButton();

    const response1 = await fetch(`${baseUrl}/booking`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });

    if (!response1.ok) {
      throw new Error(`Error: ${response1.status}`);
    }
    const data1 = await response1.json();

    const response2 = await fetch(`${baseUrl}/user/auth`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    if (!response2.ok) {
      throw new Error(`Error: ${response2.status}`);
    }
    const data2 = await response2.json();

    displayBookingDetail(data1, data2);
  } catch (error) {
    console.error("Error:", error);
  }
};

function displayBookingDetail(data1, data2) {
  // console.log(data1, data2);
  if (data1.data === null) {
    displayEmptyCart(data2);
  } else {
    displayCart(data1, data2);
  }
}

function displayCart(data1, data2) {
  const bookingUserName = document.getElementById("booking-username");

  bookingUserName.textContent = data2.data.name;

  const bookingImage = document.querySelector(".booking-image");
  const bookingImageSrc = document.createElement("img");
  bookingImageSrc.src = data1.data.attraction.image;

  bookingImage.appendChild(bookingImageSrc);

  const bookingTitlename = document.getElementById("booking-titlename");
  bookingTitlename.textContent = data1.data.attraction.name;

  const bookingDate = document.getElementById("booking-date");
  bookingDate.textContent = data1.data.date;

  const bookingTime = document.getElementById("booking-time");

  let time = data1.data.time;
  let timeText = time === "morning" ? "早上9點到下午3點" : "下午3點到晚上9點";
  bookingTime.textContent = timeText;

  const bookingPrice = document.getElementById("booking-price");
  bookingPrice.textContent = `新台幣${data1.data.price}元`;

  const bookingAddress = document.getElementById("booking-address");
  bookingAddress.textContent = data1.data.attraction.address;

  const contactName = document.getElementById("contact-name");
  contactName.value = data2.data.name;

  const contactEmail = document.getElementById("contact-email");
  contactEmail.value = data2.data.email;

  const overlay = document.querySelector(".overlay");
  overlay.style.display = "none";

  const loader = document.querySelector(".loader");
  loader.style.display = "none";
}

function displayEmptyCart(data2) {
  const bookingUserName = document.getElementById("booking-username");
  bookingUserName.textContent = data2.data.name;

  const bookingEmptyMsg = document.querySelector(".booking-empty");
  bookingEmptyMsg.style.display = "block";

  const bookingImage = document.querySelector(".booking-image");
  bookingImage.style.display = "none";

  const bookingInfo = document.querySelector(".booking-info");
  bookingInfo.style.display = "none";

  const bookingContainer = document.querySelectorAll(".booking-container");
  bookingContainer.forEach((container) => {
    container.style.display = "none";
  });

  const hr = document.querySelectorAll("hr");
  hr.forEach((hr) => {
    hr.style.display = "none";
  });

  const footerStyle = document.querySelector(".footer");
  // console.log(footerStyle);
  footerStyle.style.height = "100vh";

  const overlay = document.querySelector(".overlay");
  overlay.style.display = "none";

  const loader = document.querySelector(".loader");
  loader.style.display = "none";
}

async function deleteBooking() {
  try {
    const token = localStorage.getItem("token");
    if (!token) {
      showLoginForm();
      return;
    }

    const response1 = await fetch(`${baseUrl}/booking`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response1.ok) {
      throw new Error(`Error: ${response1.status}`);
    }
    const data1 = await response1.json();

    const response2 = await fetch(`${baseUrl}/user/auth`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response2.ok) {
      throw new Error(`Error: ${response2.status}`);
    }
    const data2 = await response2.json();

    if (data1.ok) {
      displayEmptyCart(data2);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}
