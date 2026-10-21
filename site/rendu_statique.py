#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Registre public scelle — rendu statique (portemann.eu).

Genere un registre.html autonome a partir de REGISTRE.jsonl : la page
de la carte de visite n'execute RIEN, elle affiche un fichier produit
par le depot a chaque commit (action GitHub). Doctrine : la
verifiabilite est dans le depot ; la page est une vitrine.

Usage : python site/rendu_statique.py [sortie.html]
"""
import hashlib
import html
import json
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
FICHIER = RACINE / "REGISTRE.jsonl"


def main():
    import sys
    sortie = Path(sys.argv[1]) if len(sys.argv) > 1 else RACINE / "registre.html"
    brut = FICHIER.read_bytes()
    ancre = hashlib.sha256(brut).hexdigest()
    lignes = [json.loads(l) for l in brut.decode("utf-8").splitlines()
              if l.strip()]
    lignes_html = "\n".join(
        "<tr><td>{id}</td><td>{depot}</td><td>{desc}</td>"
        "<td>{statut}</td><td>{verdict}</td></tr>".format(
            id=html.escape(e["id"]),
            depot=html.escape(e["depot"]),
            desc=html.escape(e["description"]),
            statut=html.escape(e["statut"]),
            verdict=html.escape(e["verdict"] or "—"))
        for e in lignes)
    page = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Registre public scellé</title>
<style>
body {{ font-family: Georgia, serif; max-width: 860px; margin: 2em auto;
       padding: 0 1em; color: #1a1a1a; }}
table {{ border-collapse: collapse; width: 100%; font-size: 0.92em; }}
th, td {{ border: 0.5px solid #bbb; padding: 6px 8px; text-align: left;
          vertical-align: top; }}
th {{ background: #f2f2f2; }}
code {{ font-family: monospace; font-size: 0.9em; }}
.meta {{ color: #555; font-size: 0.9em; }}
</style>
</head>
<body>
<h1>Registre public scellé</h1>
<p class="meta">Protocoles hachés <em>avant</em> la mesure · rejou
trimestriel · dormeurs publiés. Le dépôt
<a href="https://github.com/PORTEMANN/registre-public">GitHub</a> est le
registre — les commits en sont les horodatages, quiconque peut rejouer.
Cette page n'exécute rien : elle affiche un rendu produit par le dépôt.
Ancre SHA-256 : <code>{ancre[:32]}…</code></p>
<table>
<thead><tr><th>ID</th><th>Déposé</th><th>Description</th><th>Statut</th>
<th>Verdict</th></tr></thead>
<tbody>
{lignes_html}
</tbody>
</table>
<p class="meta">Pour déposer : une entrée dans
<code>REGISTRE.jsonl</code> du dépôt (pull request) — voir le
<a href="https://github.com/PORTEMANN/registre-public">README</a>.</p>
</body>
</html>
"""
    sortie.write_text(page, encoding="utf-8", newline="\n")
    print(f"rendu écrit → {sortie} ({len(lignes)} entrée(s), ancre {ancre[:16]}…)")


if __name__ == "__main__":
    main()
