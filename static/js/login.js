(function () {
  const toggle = document.querySelector(".login-toggle-pw");
  if (!toggle) return;

  toggle.addEventListener("click", () => {
    const id = toggle.getAttribute("data-target");
    const input = document.getElementById(id);
    if (!input) return;

    const show = input.type === "password";
    input.type = show ? "text" : "password";
    toggle.setAttribute("aria-label", show ? "Hide password" : "Show password");
  });
})();
