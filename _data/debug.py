import yaml
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# -------------------------
# STYLE & COULEURS
# -------------------------
COLOR_MAP = {
    "education": "#9575DE", "experience": "#FF6B6B", "project": "#4D96FF",
    "publication": "#6BCB77", "teaching": "#FFD93D", "award": "#FF9F43",
    "organisation": "#26C6DA", "unknown": "#E0E0E0"
}

with open("_data/profile_rework.yml", "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

G = nx.DiGraph()

# 1. CHARGEMENT
def add_entity(collection, n_type, label_key):
    if not collection: return
    if isinstance(collection, dict):
        for cat in collection:
            for item in collection[cat]: G.add_node(item["id"], label=item[label_key], type=n_type)
    else:
        for item in collection:
            node_id = item.get("id", item.get("title", item.get("name")))
            G.add_node(node_id, label=item[label_key], type=n_type)

add_entity(data.get("education", []), "education", "degree")
add_entity(data.get("experiences", []), "experience", "title")
add_entity(data.get("organisation", []), "organisation", "name")
add_entity(data.get("projects", {}), "project", "name")
add_entity(data.get("teaching", []), "teaching", "title")

# 2. CONSTRUCTION DES LIENS
pivots_pro = [n for n, d in G.nodes(data=True) if d.get('type') in ['education', 'experience']]

all_items = []
# On rassemble tout pour chercher les relations
for k in ["education", "experiences", "organisation", "teaching"]:
    if k in data: all_items += data[k]
if "projects" in data:
    for cat in data["projects"]: all_items += data["projects"][cat]

for node_id in G.nodes():
    item = next((i for i in all_items if i.get("id") == node_id or i.get("title") == node_id or i.get("name") == node_id), None)
    if item and "relationship" in item:
        rels = item["relationship"]
        if isinstance(rels, str): rels = [rels]
        for r in rels:
            if r in G:
                # Lien principal si c'est le parcours académique/pro
                is_main = G.nodes[node_id].get("type") in ["education", "experience"] and \
                          G.nodes[r].get("type") in ["education", "experience"]
                G.add_edge(r, node_id, principal=is_main)

# -------------------------
# 3. POSITIONNEMENT PAR CLUSTERS (SÉPARATION NETTE)
# -------------------------
pos = {}

# A. CLUSTER PRO (Au centre)
# On prend les diplômes et jobs sérieux
main_chain = [n for n in pivots_pro if n != "freelance"] # On exclut le freelance du centre pro
for i, node in enumerate(main_chain):
    angle = (2 * np.pi / len(main_chain)) * i
    pos[node] = np.array([15 * np.cos(angle), 15 * np.sin(angle)])

# B. CLUSTER SECONDAIRE (Loin sur la droite : Freelance, Projets Persos)
# On définit un nouveau centre pour le "bordel" créatif
side_center = np.array([45, 0])
side_pivots = [n for n in G.nodes() if "freelance" in n or "personal" in n]
if not side_pivots: side_pivots = ["freelance"] # Sécurité

for i, node in enumerate(side_pivots):
    if node in G:
        pos[node] = side_center + np.array([i*2, i*2])

# C. POSITIONNEMENT DES SATELLITES
for node in G.nodes():
    if node in pos: continue # Déjà placé
    
    # On cherche le parent
    parents = list(G.predecessors(node))
    if parents:
        parent = parents[0]
        if parent in pos:
            # On le place autour de son parent avec un rayon court
            # pour éviter que les traits ne traversent tout le dessin
            num_siblings = len(list(G.successors(parent)))
            idx = list(G.successors(parent)).index(node)
            angle = (2 * np.pi / num_siblings) * idx
            
            radius = 5.0 if G.nodes[node]['type'] != 'project' else 8.0
            pos[node] = pos[parent] + np.array([radius * np.cos(angle), radius * np.sin(angle)])
    else:
        # Si vraiment aucun lien (orphelin total) -> Coin supérieur
        pos[node] = np.array([-20, 40]) + np.random.uniform(-5, 5, size=2)

# -------------------------
# 4. DESSIN
# -------------------------
plt.figure(figsize=(30, 20))

# Arêtes
main_edges = [(u,v) for u,v,d in G.edges(data=True) if d.get('principal')]
sub_edges = [(u,v) for u,v,d in G.edges(data=True) if not d.get('principal')]

nx.draw_networkx_edges(G, pos, edgelist=main_edges, width=8, edge_color="#2d3436", alpha=0.6)
nx.draw_networkx_edges(G, pos, edgelist=sub_edges, width=1.5, edge_color="#b2bec3", alpha=0.4, style="dashed")

# Noeuds
node_colors = [COLOR_MAP.get(G.nodes[n].get('type'), "#E0E0E0") for n in G.nodes]
nx.draw_networkx_nodes(G, pos, node_size=2500, node_color=node_colors, edgecolors="white", linewidths=2)

# Labels
labels = {n: G.nodes[n].get('label', n).replace(' ', '\n') for n in G.nodes}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_weight="bold")

plt.axis('off')
plt.title("MAP SÉPARÉE : PARCOURS PRO VS PROJETS SECONDAIRES", fontsize=30)
plt.show()