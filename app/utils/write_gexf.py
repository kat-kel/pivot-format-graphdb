from kuzu import QueryResult
import networkx as nx
from datetime import date


def write_gexf(res: QueryResult, filepath: str) -> None:
    G = res.get_as_networkx(directed=True)

    for n in G.nodes:
        bad_keys = []
        node = G._node[n]
        for k, v in node.items():
            if not v:
                bad_keys.append(k)
            elif isinstance(v, list):
                bad_keys.append(k)
            elif isinstance(v, date):
                v = str(v)
                node.update({k: v})
        [node.pop(k) for k in bad_keys]

    nx.write_gexf(G, filepath)
