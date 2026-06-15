import yaml
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np

# ─────────────────────────────────────────
# CHARGEMENT
# ─────────────────────────────────────────
with open("_data/profile_rework2.yml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

G = nx.Graph()  # NON-DIRIGÉ → élimine les doublons A↔B naturellement

def add_nodes(collection, node_type, label_key):
    if not collection: return
    if isinstance(collection, dict):
        for cat, items in collection.items():
            for item in (items or []):
                nid = item.get("id")
                if nid:
                    G.add_node(nid, label=item.get(label_key) or item.get("name") or nid, type=node_type)
    else:
        for item in collection:
            nid = item.get("id") or item.get("title") or item.get("name")
            if nid:
                G.add_node(nid, label=item.get(label_key) or item.get("name") or item.get("title") or nid, type=node_type)

add_nodes(data.get("education",    []), "education",    "degree")
add_nodes(data.get("experiences",  []), "experience",   "title")
add_nodes(data.get("organisation", []), "organisation", "name")
add_nodes(data.get("projects",     {}), "project",      "name")
add_nodes(data.get("teaching",     []), "teaching",     "title")
add_nodes(data.get("publications", []), "publication",  "title")
add_nodes(data.get("awards_and_achievements", []), "award", "title")
add_nodes(data.get("people",       []), "people",       "name")

# Collecte de tous les items
all_items = []
for k in ["education","experiences","organisation","teaching","publications","people"]:
    for item in (data.get(k) or []):
        all_items.append((item, "linked_to"))
for cat, lst in (data.get("projects") or {}).items():
    for item in (lst or []):
        all_items.append((item, "linked_to"))
for item in (data.get("awards_and_achievements") or []):
    c = dict(item)
    if "id" not in c: c["id"] = c.get("title")
    all_items.append((c, "linked_to"))

# Ajout des arêtes — Graph non-dirigé déduplique automatiquement
for item, _ in all_items:
    src = item.get("id") or item.get("title")
    if not src or src not in G: continue
    for ref in (item.get("linked_to") or []):
        if ref in G:
            G.add_edge(src, ref, kind="linked_to")
    for ref in (item.get("publications") or []):
        if ref in G:
            G.add_edge(src, ref, kind="publication")
    for ref in (item.get("teaching") or []):
        if ref in G:
            G.add_edge(src, ref, kind="teaching")

degree = dict(G.degree())
print(f"Noeuds: {G.number_of_nodes()}, Arêtes: {G.number_of_edges()}")
print("Top hubs:", sorted(degree.items(), key=lambda x: -x[1])[:5])

# ─────────────────────────────────────────
# LAYOUT : Kamada-Kawai — meilleur pour lisibilité
# Les hubs se placent naturellement au centre
# ─────────────────────────────────────────
# Poids inversement proportionnel au degré combiné
# pour que les hubs soient tirés vers le centre
def edge_weight(u, v):
    return 1.0 / (1 + degree[u] + degree[v])

for u, v in G.edges():
    G[u][v]["weight"] = edge_weight(u, v)

pos = nx.kamada_kawai_layout(G, weight="weight", scale=4.0)

# ─────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────
BG = "#0d1117"

COLORS = {
    "education":    "#a78bfa",
    "experience":   "#f87171",
    "organisation": "#38bdf8",
    "project":      "#4ade80",
    "teaching":     "#fbbf24",
    "publication":  "#34d399",
    "award":        "#fb923c",
    "people":       "#f472b6",
}

# Couleur + transparence par type d'arête
EDGE_STYLE = {
    "linked_to":   dict(color="#3b5268", lw=0.8,  alpha=0.55, zorder=1),
    "publication": dict(color="#34d399", lw=1.8,  alpha=0.80, zorder=2),
    "teaching":    dict(color="#fbbf24", lw=1.8,  alpha=0.80, zorder=2),
}

max_deg = max(degree.values())

def node_size(n):
    d = degree[n]
    # Echelle: 150 (feuille) → 4800 (hub max)
    return 150 + (d / max_deg) ** 1.6 * 4650

# ─────────────────────────────────────────
# DESSIN
# ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(24, 18))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

# — Halo sur les hubs (degré ≥ 4) — calque 0
for n, (x, y) in pos.items():
    d = degree[n]
    if d < 4: continue
    ntype = G.nodes[n].get("type", "unknown")
    color = COLORS.get(ntype, "#888")
    for mult, a in [(0.25, 0.04), (0.16, 0.07), (0.09, 0.12)]:
        circle = plt.Circle((x, y), radius=mult + d*0.014,
                             color=color, alpha=a, zorder=0)
        ax.add_patch(circle)

# — Arêtes DROITES, groupées par type —
for kind, style in EDGE_STYLE.items():
    edge_list = [(u, v) for u, v, d in G.edges(data=True) if d.get("kind") == kind]
    if not edge_list: continue

    # Tracé manuel ligne par ligne pour éviter tout artefact de nx
    for u, v in edge_list:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        ax.plot(
            [x0, x1], [y0, y1],
            color=style["color"],
            lw=style["lw"],
            alpha=style["alpha"],
            zorder=style["zorder"],
            solid_capstyle="round",
        )

# — Noeuds —
for ntype, color in COLORS.items():
    nodelist = [n for n in G.nodes() if G.nodes[n].get("type") == ntype]
    if not nodelist: continue
    nx.draw_networkx_nodes(
        G, pos, nodelist=nodelist, ax=ax,
        node_size=[node_size(n) for n in nodelist],
        node_color=color,
        edgecolors="#0d1117",
        linewidths=1.5,
        alpha=0.92,
    )

# — Labels : uniquement degré ≥ 2, sans bbox, taille proportionnelle —
def wrap_label(label, max_chars=18):
    """Coupe le label en 2 lignes si trop long."""
    words = label.split()
    if len(label) <= max_chars or len(words) <= 2:
        return label
    mid = len(words) // 2
    return " ".join(words[:mid]) + "\n" + " ".join(words[mid:])

for n in G.nodes():
    d = degree[n]
    if d < 2: continue
    x, y = pos[n]
    lbl   = wrap_label(G.nodes[n].get("label", n))
    fsize = 6.0 + min(d * 0.45, 4.5)   # 6 → 10.5 pt
    bold  = "bold" if d >= 5 else "normal"
    col   = "white" if d >= 5 else "#94a3b8"
    ax.text(x, y, lbl,
            fontsize=fsize, fontweight=bold,
            ha="center", va="center",
            color=col, fontfamily="monospace",
            multialignment="center",
            zorder=5)

# — Annotation degré sous les 3 hubs principaux —
TOP3 = ["phd_robotic", "engineering_degree", "internship_inl"]
for hub in TOP3:
    if hub not in pos: continue
    x, y = pos[hub]
    d = degree[hub]
    ax.text(x, y - 0.38, f"({d})",
            fontsize=6, color="#475569",
            ha="center", va="center",
            fontfamily="monospace", zorder=6)

# — Légende —
node_handles = [
    mpatches.Patch(color=COLORS[t], label=t.capitalize(), alpha=0.88)
    for t in COLORS
]
edge_handles = [
    Line2D([0],[0], color=EDGE_STYLE["linked_to"]["color"],   lw=1.2, label="linked_to",   alpha=0.8),
    Line2D([0],[0], color=EDGE_STYLE["publication"]["color"], lw=2.0, label="publication",  alpha=0.9),
    Line2D([0],[0], color=EDGE_STYLE["teaching"]["color"],    lw=2.0, label="teaching",     alpha=0.9),
]

leg1 = ax.legend(handles=node_handles, loc="upper left",
                 fontsize=8, framealpha=0.10,
                 facecolor="#1e293b", labelcolor="white",
                 title="Node type", title_fontsize=8)
leg1.get_title().set_color("#64748b")
ax.add_artist(leg1)

leg2 = ax.legend(handles=edge_handles, loc="lower left",
                 fontsize=8, framealpha=0.10,
                 facecolor="#1e293b", labelcolor="white",
                 title="Edge type", title_fontsize=8)
leg2.get_title().set_color("#64748b")

ax.set_title("Grégory Loubet-Bonino — Connection Map",
             fontsize=14, color="#e2e8f0", pad=14,
             fontfamily="monospace", fontweight="bold")
ax.axis("off")

plt.tight_layout(pad=0.5)
plt.savefig("graph_connections.png", dpi=180, bbox_inches="tight", facecolor=BG)
print("Sauvegardé.")