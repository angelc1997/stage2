const baseUrl = "http://127.0.0.1:8000/api";

//  Fetch Tags
async function fetchTags() {
  try {
    let mrtAPI = `${baseUrl}/mrts`;
    let data = await fetchData(mrtAPI);
    let mrtdata = data.data;
    mrtdata.forEach((mrt) => {
      const tagList = document.querySelector(".tag-list");
      const tag = document.createElement("div");
      tag.className = "tag";
      tag.textContent = mrt;
      tagList.appendChild(tag);
    });
    const clickTag = document.querySelectorAll(".tag");
    const searchInput = document.getElementById("search-input");
    clickTag.forEach((tag) => {
      tag.addEventListener("click", () => {
        searchInput.classList.add("searching");
        document.getElementById("search-input").value = tag.textContent;
        // console.log(tag.textContent);
        fetchKeywordFirstPage(tag.textContent);
      });
    });
  } catch (error) {
    console.error("無法取得捷運標籤：", error);
  }
}
// Drag Tags
const tagList = document.querySelector(".tag-list");
const icons = document.querySelectorAll(".tag-icon");
icons.forEach((icon) => {
  icon.addEventListener("click", () => {
    tagList.scrollLeft += icon.id === "next" ? 600 : -600;
  });
});

// Fetch Data Response
async function fetchData(url) {
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }
  const data = await response.json();
  return data;
}

let pageNumbers = [];
let keywords = [];

// Fetch Attractions
async function fetchPage(url) {
  try {
    const skeletonList = document.createElement("div");
    skeletonList.classList.add("tag-list", "skeleton", "skeleton-list");

    const cardGrid = document.querySelector(".card-grid");
    for (let i = 0; i < 13; i++) {
      cardGrid.appendChild(createSkeletonCard());
    }

    const data = await fetchData(url);

    const tagList = document.querySelector(".tag-list");
    tagList.classList.remove("skeleton", "skeleton-list");
    document.querySelectorAll(".skeleton-card").forEach((card) => {
      card.remove();
    });

    pageNumbers.shift();
    pageNumbers.push(data.nextPage);
    displayPage(data.data);
    observer.observe(footer);
  } catch (error) {
    console.error("無法取得景點資料：", error);
  }
}

async function fetchFirstPage() {
  try {
    fetchPage(`${baseUrl}/attractions?page=0`);
  } catch (error) {
    console.error("無法取得第一頁景點資料：", error);
  }
}

async function fetchNextPage() {
  try {
    fetchPage(`${baseUrl}/attractions?page=${pageNumbers[0]}`);
  } catch (error) {
    console.error("無法取得新一頁景點資料：", error);
  }
}

async function fetchKeywordFirstPage(keyword) {
  try {
    const keyAPI = `${baseUrl}/attractions?page=0&keyword=${keyword}`;
    const cardGrid = document.querySelector(".card-grid");
    while (cardGrid.firstChild) {
      cardGrid.removeChild(cardGrid.firstChild);
    }
    keywords.shift();
    keywords.push(keyword);
    fetchPage(keyAPI);
  } catch (error) {
    console.error("無法取得關鍵字景點資料：", error);
  }
}

async function fetchKeywordNextPage() {
  try {
    const pageNumber = pageNumbers[0];
    const keyword = keywords[0];
    const keyAPI = `${baseUrl}/attractions?page=${pageNumber}&keyword=${keyword}`;
    fetchPage(keyAPI);
  } catch (error) {
    console.error("無法取得新一頁關鍵字景點資料：", error);
  }
}

// Search By Keyword
document.getElementById("search-btn").addEventListener("click", goSeach);
document.getElementById("search-input").addEventListener("keyup", (e) => {
  if (e.key == "Enter") {
    goSeach();
  }
});

async function goSeach() {
  try {
    const searchInput = document.getElementById("search-input").value;
    fetchKeywordFirstPage(searchInput);
  } catch (error) {
    console.error("無法取得關鍵字景點資料：", error);
  }
}

// Display Data Card
function displayPage(attrdata) {
  try {
    const cardGrid = document.querySelector(".card-grid");

    attrdata.forEach((attr) => {
      const card = createCardElement(attr);
      const cardId = attr.id;
      card.addEventListener("click", () => {
        window.location.pathname = `/attraction/${cardId}`;
      });

      cardGrid.appendChild(card);
    });
  } catch (error) {
    console.error("無法顯示資料：", error);
  }
}
// Create Data Card
function createCardElement(card) {
  const cardContainer = document.createElement("div");
  cardContainer.setAttribute("class", "card-container");

  const cardImg = document.createElement("div");
  cardImg.setAttribute("class", "card-img");
  cardImg.style.backgroundImage = `url(${card.images[0]})`;
  cardContainer.appendChild(cardImg);

  const cardTitle = document.createElement("div");
  cardTitle.setAttribute("class", "card-title");
  cardTitle.textContent = card.name;
  if (cardTitle.textContent.length > 15) {
    cardTitle.textContent = cardTitle.textContent.slice(0, 15) + "...";
  }
  cardImg.appendChild(cardTitle);

  const cardContent = document.createElement("div");
  cardContent.setAttribute("class", "card-content");
  cardContainer.appendChild(cardContent);

  const cardMrt = document.createElement("div");
  cardMrt.setAttribute("class", "card-mrt");
  cardMrt.textContent = card.mrt;
  cardContent.appendChild(cardMrt);

  const cardType = document.createElement("div");
  cardType.setAttribute("class", "card-type");
  cardType.textContent = card.category;
  cardContent.appendChild(cardType);

  return cardContainer;
}

// Display skeleton
function createSkeletonCard() {
  const skeletonCard = document.createElement("div");
  skeletonCard.classList.add("card-container", "skeleton-card");

  const skeletonImg = document.createElement("div");
  skeletonImg.classList.add("card-img", "skeleton");
  skeletonCard.appendChild(skeletonImg);

  const skeletonTitle = document.createElement("div");
  skeletonTitle.classList.add("card-title", "skeleton", "skeleton-body");
  skeletonImg.appendChild(skeletonTitle);

  const skeletonContent = document.createElement("div");
  skeletonContent.classList.add("card-content");
  skeletonCard.appendChild(skeletonContent);

  const skeletonMrt = document.createElement("div");
  skeletonMrt.classList.add("card-mrt", "skeleton", "skeleton-body");
  skeletonContent.appendChild(skeletonMrt);

  const skeletonType = document.createElement("div");
  skeletonType.classList.add("card-type", "skeleton", "skeleton-body");
  skeletonContent.appendChild(skeletonType);

  return skeletonCard;
}
// Observer
const options = {
  root: null,
  rootMargin: "0px 0px 0px 0px",
  threshold: 1,
};
const footer = document.querySelector(".footer");
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      if (pageNumbers[0] !== null) {
        keywords[0] == null ? fetchNextPage() : fetchKeywordNextPage();
      } else {
        observer.unobserve(footer);
      }
    }
  });
}, options);

// Form Login
window.addEventListener("load", function () {
  const token = this.localStorage.getItem("token");
  if (token) {
    showLogoutButton();
  }
});

// Initialize Data
fetchTags();
fetchFirstPage();
