// Applies the saved color theme before first paint and wires up the theme toggle.
// It mirrors Furo's toggle on docs.postproject.org: the same "theme" storage values
// (auto, light, dark) and the same cycle order. Without this script the page
// follows the system preference and the toggle stays hidden.
(() => {
  const root = document.documentElement;
  const key = "theme";

  // Storage can be unavailable (private windows, blocked site data).
  const read = () => { try { return localStorage.getItem(key); } catch { return null; } };
  const apply = (theme) => {
    root.dataset.theme = theme === "light" || theme === "dark" ? theme : "auto";
    try { localStorage.setItem(key, root.dataset.theme); } catch {}
  };

  apply(read());

  // The first click always visibly changes the theme:
  // auto (dark) -> light -> dark, or auto (light) -> dark -> light.
  const cycle = () => {
    const current = root.dataset.theme;
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    if (prefersDark) apply(current === "auto" ? "light" : current === "light" ? "dark" : "auto");
    else apply(current === "auto" ? "dark" : current === "dark" ? "light" : "auto");
  };

  document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector(".theme-toggle");
    if (!toggle) return;
    toggle.hidden = false;
    toggle.addEventListener("click", cycle);
  });
})();
