const key = "pi-web:panel-sizes:v1";
let focused = "chat";

document.addEventListener("focusin", (event) => {
  for (const target of event.composedPath()) {
    if (!(target instanceof Element)) continue;
    if (target.id === "navigation-panel" || target.localName === "app-navigation-panel") focused = "navigation";
    if (target.id === "workspace-panel" || target.localName === "workspace-panel") focused = "workspace";
    if (target.localName === "chat-view") focused = "chat";
  }
}, true);

function move(direction) {
  const root = document.querySelector("pi-web-app")?.shadowRoot;
  const shell = root?.querySelector(".shell");
  if (!(shell instanceof HTMLElement)) return;

  const panels = ["navigation", "workspace", "chat"].map((id) => ({
    id,
    element: root.querySelector(id === "chat" ? "main" : `#${id}-panel`),
  })).sort((a, b) => a.element.getBoundingClientRect().left - b.element.getBoundingClientRect().left);
  const index = panels.findIndex((panel) => panel.id === focused);
  const [left, right] = index === panels.length - 1 ? panels.slice(index - 1) : panels.slice(index, index + 2);
  // Chat flexes. Resize the adjacent fixed-width panel instead.
  const panel = left.id === "chat" ? right : left;
  const storage = JSON.parse(localStorage.getItem(key) || "{}");
  const sizeKey = `${panel.id}PanelWidth`;
  const width = storage[sizeKey] ?? (panel.id === "navigation" ? 340 : 480);
  const next = Math.max(panel.id === "navigation" ? 180 : 240, width + (panel === left ? direction : -direction) * 24);

  localStorage.setItem(key, JSON.stringify({ version: 1, ...storage, [sizeKey]: next }));
  shell.style.setProperty(`--${panel.id}-panel-size`, `${next}px`);
}

export default {
  apiVersion: 1,
  name: "Panel Resize",
  activate: () => ({
    contributions: {
      actions: [
        { id: "resize-left", title: "Move Focused Panel Divider Left", shortcut: "mod+h", group: "Layout", run: () => move(-1) },
        { id: "resize-right", title: "Move Focused Panel Divider Right", shortcut: "mod+l", group: "Layout", run: () => move(1) },
      ],
    },
  }),
};
