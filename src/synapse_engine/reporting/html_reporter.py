from __future__ import annotations

from pathlib import Path

from ..utils.io import write_text


def write_html_report(patches, risk_register, path: str | Path) -> None:
    rows = "".join(
        f"<tr><td>{p.patch_id}</td><td>{p.passed}</td><td>{p.patch_score:.2f}</td></tr>"
        for p in patches
    )
    risk_rows = "".join(
        f"<li>{r.risk_id}: {r.description} ({r.severity})</li>"
        for r in risk_register.items
    )
    html = f"""
    <html>
      <body>
        <h1>Synapse Engine Report</h1>
        <table border="1">
          <tr><th>Patch</th><th>PASS</th><th>Score</th></tr>
          {rows}
        </table>
        <h2>Risk Register</h2>
        <ul>{risk_rows}</ul>
      </body>
    </html>
    """
    write_text(Path(path), html)
