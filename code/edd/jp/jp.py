from base64 import b64encode

import networkx as nx  # type: ignore
from IPython.display import HTML, display


def build_html_table(headers: list[str], rows: list[list[str]]) -> str:
    return f"""
    <table>
        <thead>
            <tr>
                {"".join(f"<th>{header}</th>" for header in headers)}
            </tr>
        </thead>
        <tbody>
            {"".join(f"<tr>{"".join(f"<td>{cell}</td>" for cell in row)}</tr>" for row in rows)}
        </tbody>
    </table>
    """


def render_html(html: str) -> None:
    display(HTML(html))


def render_graphviz_svg(G: nx.Graph) -> None:
    A = nx.nx_agraph.to_agraph(G)
    # A.graph_attr.update(rankdir="LR")
    # A.node_attr.update(shape="box", margin=(0.01, 0.1))
    svg = A.draw(format="svg", prog="dot")
    display(HTML(f'<img src="data:image/svg+xml;base64,{b64encode(svg).decode()}">'))
