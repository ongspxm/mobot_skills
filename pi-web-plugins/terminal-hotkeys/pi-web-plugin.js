function tabs() {
  return document.querySelector("pi-web-app")?.shadowRoot
    ?.querySelector("workspace-panel")?.shadowRoot
    ?.querySelector("terminal-panel")?.shadowRoot
    ?.querySelector(".terminal-tabs");
}

function moveTab(direction) {
  const all = [...tabs()?.querySelectorAll("button:not(.new):not(.copy-mode-toggle):not(.soft-keys-toggle)") ?? []];
  const index = all.findIndex((button) => button.classList.contains("selected"));
  all[(index + direction + all.length) % all.length]?.click();
}

export default {
  apiVersion: 1,
  name: "Terminal Hotkeys",
  activate: () => ({
    contributions: {
      actions: [
        { id: "new", title: "New Terminal Shell", shortcut: "mod+g t", group: "Terminal", enabled: () => Boolean(tabs()), run: () => tabs()?.querySelector(".new")?.click() },
        { id: "previous", title: "Previous Terminal Tab", shortcut: "mod+g h", group: "Terminal", enabled: () => Boolean(tabs()), run: () => moveTab(-1) },
        { id: "next", title: "Next Terminal Tab", shortcut: "mod+g l", group: "Terminal", enabled: () => Boolean(tabs()), run: () => moveTab(1) },
        { id: "close", title: "Close Current Terminal Shell", shortcut: "mod+g y", group: "Terminal", enabled: () => Boolean(tabs()), run: () => tabs()?.querySelector("button.selected small")?.click() },
      ],
    },
  }),
};
