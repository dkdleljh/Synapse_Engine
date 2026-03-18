from __future__ import annotations

from pathlib import Path


def plot_heatmap(values: dict[str, float], out_path: str | Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return

    if not values:
        return

    names = list(values.keys())
    scores = list(values.values())
    plt.figure(figsize=(6, 3))
    plt.bar(names, scores)
    plt.ylim(0, 1)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out)
    plt.close()
