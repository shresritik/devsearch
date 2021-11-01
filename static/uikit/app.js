// Invoke Functions Call on Document Loaded

alertClose = document.querySelectorAll(".alert__close");
alertClose.forEach((element) => {
  element.addEventListener("click", () => {
    element.closest(".alert").remove();
  });
});
