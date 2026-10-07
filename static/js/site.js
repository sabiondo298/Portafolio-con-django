requestAnimationFrame(() => document.body.classList.add("page-ready"));

const themeToggle = document.querySelector(".theme-toggle");
const savedTheme = localStorage.getItem("portfolio-theme");

if (themeToggle) {
    if (savedTheme === "light") {
        document.body.classList.add("light-mode");
        themeToggle.setAttribute("aria-pressed", "true");
        themeToggle.setAttribute("aria-label", "Activar modo oscuro");
        themeToggle.innerHTML = '<i class="bi bi-moon-fill" aria-hidden="true"></i>';
    }

    themeToggle.addEventListener("click", () => {
        const isLightMode = document.body.classList.toggle("light-mode");
        themeToggle.setAttribute("aria-pressed", String(isLightMode));
        themeToggle.setAttribute("aria-label", isLightMode ? "Activar modo oscuro" : "Activar modo claro");
        themeToggle.innerHTML = isLightMode
            ? '<i class="bi bi-moon-fill" aria-hidden="true"></i>'
            : '<i class="bi bi-sun-fill" aria-hidden="true"></i>';
        localStorage.setItem("portfolio-theme", isLightMode ? "light" : "dark");
    });
}

const adminModal = document.querySelector("#admin-modal");
const adminButton = document.querySelector(".admin-button");
const adminModalClose = document.querySelector(".admin-modal-close");
const adminUsername = document.querySelector("#admin-username");

if (adminButton && adminModal && adminModalClose && adminUsername) {
    adminButton.addEventListener("click", () => {
        adminModal.showModal();
        adminUsername.focus();
    });
    adminModalClose.addEventListener("click", () => adminModal.close());
    adminModal.addEventListener("click", (event) => {
        if (event.target === adminModal) {
            adminModal.close();
        }
    });
}

document.querySelectorAll("[data-comment-trigger]").forEach((button) => {
    const form = document.getElementById(button.getAttribute("aria-controls"));
    if (!form) {
        return;
    }

    button.addEventListener("click", () => {
        const isOpen = button.getAttribute("aria-expanded") === "true";
        button.setAttribute("aria-expanded", String(!isOpen));
        form.hidden = isOpen;
        if (!isOpen) {
            form.querySelector("input[name='author']")?.focus();
        }
    });
});
