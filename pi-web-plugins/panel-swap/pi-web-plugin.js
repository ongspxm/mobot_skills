const swappedAttribute = "data-chat-workspace-swap";

function applySwap(swapped) {
  const app = document.querySelector("pi-web-app");
  const root = app?.shadowRoot;
  if (app === null || root === null || root === undefined) return;

  app.toggleAttribute(swappedAttribute, swapped);

  // The panel is now left of chat, so its resize handle needs left-panel directions.
  const edge = root.querySelector('app-panel-edge-control[controls="workspace-panel"]');
  if (edge === null) return;
  edge.side = swapped ? "navigation" : "workspace";
  edge.style.gridColumn = swapped ? "4" : "";
}

export default {
  apiVersion: 1,
  name: "Panel Swap",
  activate: () => {
    const app = document.querySelector("pi-web-app");
    const root = app?.shadowRoot;
    if (root !== null && root !== undefined) {
      const style = document.createElement("style");
      style.textContent = `
        @media (min-width: 1181px) {
          :host([${swappedAttribute}]) .shell {
            grid-template-columns: var(--navigation-panel-width) 1px var(--workspace-panel-width) 1px minmax(320px, 1fr);
          }
          :host([${swappedAttribute}]) main { grid-column: 5; grid-row: 1; }
          :host([${swappedAttribute}]) app-panel-edge-control[controls="workspace-panel"] { grid-column: 4; grid-row: 1; }
          :host([${swappedAttribute}]) workspace-panel { grid-column: 3; grid-row: 1; }
        }
      `;
      root.append(style);
    }

    requestAnimationFrame(() => { applySwap(true); });

    return {
      contributions: {
        actions: [{
          id: "toggle",
          title: "Toggle Chat / Workspace Panel Position",
          group: "Layout",
          run: () => {
            const app = document.querySelector("pi-web-app");
            applySwap(app?.hasAttribute(swappedAttribute) !== true);
          },
        }],
      },
    };
  },
};
