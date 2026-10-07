const togglePanel = (panel) => {
    const expanded = panel.classList.toggle("is-expanded");
    panel.parentElement.classList.toggle("has-expanded", expanded);
    panel.setAttribute("aria-expanded", String(expanded));
};

const myselfPanel = document.querySelector(".content-panel--expandable");
if (myselfPanel) {
    myselfPanel.addEventListener("click", () => togglePanel(myselfPanel));
}

document.querySelectorAll(".content-panel--projects, .content-panel--contact").forEach((panel) => {
    panel.addEventListener("click", (event) => {
        if (!event.target.closest("a")) {
            togglePanel(panel);
        }
    });
    panel.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            togglePanel(panel);
        }
    });
});
