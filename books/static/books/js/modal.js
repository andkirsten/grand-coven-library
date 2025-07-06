document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("addBookModal");
  const btn = document.getElementById("addBookBtn");
  const span = document.querySelector(".close");

  if (!modal || !btn || !span) {
    // Elements not found — avoid errors if page doesn’t have modal
    return;
  }

  btn.onclick = () => {
    modal.style.display = "block";
  };

  span.onclick = () => {
    modal.style.display = "none";
  };

  window.onclick = (event) => {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };
});
