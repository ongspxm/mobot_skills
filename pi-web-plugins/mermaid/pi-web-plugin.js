const mermaidUrl = "https://cdn.jsdelivr.net/npm/mermaid@11.16.0/dist/mermaid.esm.min.mjs";
let mermaidPromise;
let diagramId = 0;
const watchedRoots = new WeakSet();
const renderedBlocks = new WeakSet();

const loadMermaid = () => mermaidPromise ??= import(mermaidUrl).then(({ default: mermaid }) => {
  mermaid.initialize({ startOnLoad: false, securityLevel: "strict", theme: "default" });
  return mermaid;
});

function renderBlocks(root) {
  for (const pre of root.querySelectorAll("pre")) {
    const code = pre.querySelector("code.language-mermaid, code.lang-mermaid");
    if (code === null || renderedBlocks.has(pre)) continue;

    const source = code.textContent ?? "";
    if (!source.trim()) continue;
    renderedBlocks.add(pre);

    loadMermaid()
      .then((mermaid) => mermaid.render(`pi-web-mermaid-${++diagramId}`, source))
      .then(({ svg, bindFunctions }) => {
        if (!root.contains(pre) || code.textContent !== source) {
          renderedBlocks.delete(pre);
          return;
        }

        const chart = document.createElement("div");
        chart.className = "pi-web-mermaid";
        chart.style.marginBottom = "10px";
        chart.innerHTML = `<label style="display:flex;align-items:center;gap:6px;margin-bottom:4px;font-size:.8em">Diagram width <input type="range" min="50" max="200" step="10" value="100" aria-label="Diagram width" style="width:12rem"><output>100%</output></label><div style="overflow-x:auto;text-align:center" role="img" aria-label="Mermaid diagram">${svg}</div>`;

        const diagram = chart.lastElementChild;
        const [control, output] = chart.querySelectorAll("input, output");
        const renderedSvg = diagram.querySelector("svg");
        renderedSvg.style.cssText = `max-width:none;width:${control.value}%;height:auto`;
        control.addEventListener("input", () => {
          renderedSvg.style.width = `${control.value}%`;
          output.textContent = `${control.value}%`;
        });
        bindFunctions?.(diagram);

        pre.hidden = true;
        pre.before(chart);
      })
      .catch((error) => {
        if (root.contains(pre)) console.error("mermaid.render.failed", error);
      });
  }

  for (const element of root.querySelectorAll("*")) {
    if (element.shadowRoot !== null) watch(element.shadowRoot);
  }
}

function watch(root) {
  if (watchedRoots.has(root)) return;
  watchedRoots.add(root);
  new MutationObserver(() => renderBlocks(root)).observe(root, { childList: true, subtree: true });
  renderBlocks(root);
}

export default {
  apiVersion: 2,
  name: "Mermaid Diagrams",
  activate: () => {
    watch(document);
    return { contributions: {} };
  },
};
