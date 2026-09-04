const styleId = "git-diff-wrap-style";
const css = `
  .git-panel .git-viewer,
  .git-panel .git-diffs,
  .git-panel .git-diff-section,
  .git-panel .git-diff-scroller { min-width: 0; }
  .git-panel .git-diff-grid {
    grid-template-columns: max-content max-content 2ch minmax(0, 1fr);
    width: 100%;
    min-width: 0;
  }
  .git-panel .git-content {
    min-width: 0;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
  }
`;
const watchedRoots = new WeakSet();

function watch(root) {
  if (watchedRoots.has(root)) return;
  watchedRoots.add(root);

  const scan = () => {
    if (root.querySelector(".git-panel") !== null) {
      let style = root.querySelector(`#${styleId}`);
      if (style === null) {
        style = document.createElement("style");
        style.id = styleId;
        style.textContent = css;
        root.append(style);
      } else if (root.lastElementChild !== style) {
        // Keep this after the Git panel's own style.
        root.append(style);
      }
    }
    for (const element of root.querySelectorAll("*")) {
      if (element.shadowRoot !== null) watch(element.shadowRoot);
    }
  };

  new MutationObserver(scan).observe(root, { childList: true, subtree: true });
  scan();
}

export default {
  apiVersion: 2,
  name: "Git Diff Wrap",
  activate: () => {
    watch(document);
    return { contributions: {} };
  },
};
