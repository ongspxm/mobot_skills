---
name: marimo
description: Use when writing or fixing marimo notebook scripts.
---

# Marimo Notebooks

## Overview
marimo - build compact, valid marimo notebooks

## Workflows
Use for `.py` marimo notebooks with reactive cells, UI, state, or DAG errors.

## Resources
- marimo docs: https://docs.marimo.io/
- official marimo skill: https://github.com/marimo-team/skills/blob/main/skills/marimo-notebook/SKILL.md

## When to Use
marimo notebooks are Python files. Cells form a DAG from names they define and consume.

Keep notebooks simple. One global name, one owner cell. Use local `_scratch` names for temp work.

## Boundaries
- No duplicate globals. Same global name in two cells raises `DuplicateNameError`.
- Cell args are injected by marimo from matching globals. Do not call cell funcs by hand.
- Each cell is `@app.cell` and returns the globals it exports.
- Return nothing for display-only or local-only cells.
- UI widgets should be globals, e.g. `slider = mo.ui.slider(...)` then return `slider`.
- React to widget changes through `.value` in downstream cells.
- Use `mo.state(initial)` for persistent interactive state.
- Layout: `mo.hstack([...])` for rows, `mo.vstack([...])` for columns.

## Examples
Compact full pattern: setup, globals, locals, UI, state, button, reactive output, layout.

```python
import marimo as mo
app = mo.App(title="Example")


with app.setup:
    # `with app.setup:` creates the special setup cell.
    # It runs before other cells and cannot reference variables from them.
    import marimo as mo
    import numpy as np


@app.cell
def data():
    label = "Global data"  # exported global; unique owner cell
    _label = "Local data"  # safe reuse; not exported
    _tmp = [1, 2, 3]
    return label,


@app.cell
def controls(mo):
    # `mo` is exported by the special `app.setup` cell; do not call it by hand.
    slider = mo.ui.slider(start=1, stop=10, value=5, label="Multiplier")
    mo.hstack([mo.md("### Adjust"), slider])  # last expr displays
    return slider,


@app.cell
def state(mo):
    get_count, set_count = mo.state(0)
    button = mo.ui.button(
        label="Increment",
        on_click=lambda _: set_count(get_count() + 1),
    )
    return button, get_count, set_count


@app.cell
def output(button, get_count, label, mo, slider):
    # Re-runs when any arg changes, e.g. slider.value or button click state.
    value = slider.value * 10
    card = mo.md(
        f"""
        ### Output
        - label: `{label}`
        - slider: `{slider.value}`
        - value: `{value}`
        - count: `{get_count()}`
        """
    )
    controls = mo.hstack([button, slider])
    dashboard = mo.vstack([card, controls])
    dashboard
    return card, controls, dashboard, value


if __name__ == "__main__":
    app.run()
```
