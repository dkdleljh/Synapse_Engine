from __future__ import annotations

from pathlib import Path


def plot_graph(nodes, edges, out_path: str | Path) -> None:
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except Exception:
        return

    g = nx.DiGraph()
    for n in nodes:
        g.add_node(n.id)
    for e in edges:
        g.add_edge(e.source, e.target)

    plt.figure(figsize=(6, 4))
    pos = nx.spring_layout(g, seed=42)
    nx.draw(g, pos, with_labels=True, arrows=True)
    plt.tight_layout()
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out)
    plt.close()
