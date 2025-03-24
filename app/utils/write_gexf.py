import networkx as nx


def write_gexf(res, filepath: str) -> None:
    G = res.get_as_networkx(directed=True)

    for n in G.nodes:
        bad_keys = []
        node = G._node[n]
        for k, v in node.items():
            if not v:
                bad_keys.append(k)
            elif k.endswith("[]"):
                bad_keys.append(k)
        [node.pop(k) for k in bad_keys]

    nx.write_gexf(G, filepath)
