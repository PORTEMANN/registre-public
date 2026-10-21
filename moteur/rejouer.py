#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Registre public scelle — moteur de rejou trimestriel.

Pour chaque entree dont la date_rejou est atteinte :
  1. constate les donnees publiees (lien_donnees) ;
  2. si un script de controle est joint (scripts/<id>.py), l'execute
     et consigne sa sortie comme verdict ;
  3. sinon, marque « rejugée — constatation manuelle » ;
  4. ecrit les verdicts dans REGISTRE.jsonl (y compris « morte »).

Le rejou est un commit public : les dormeurs sont publies au meme
titre que les confirmées. Stdlib seulement, MIT.

Usage : python moteur/rejouer.py [YYYY-MM-DD]
"""
import datetime
import json
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
FICHIER = RACINE / "REGISTRE.jsonl"
SCRIPTS = RACINE / "scripts"


def main(date_ref=None):
    date_ref = (datetime.date.fromisoformat(date_ref)
                if date_ref else datetime.date.today())
    lignes = [json.loads(l)
              for l in FICHIER.read_text(encoding="utf-8").splitlines()
              if l.strip()]
    modifie = False
    for ligne in lignes:
        if ligne["statut"] != "dort":
            continue
        d = datetime.date.fromisoformat(ligne["date_rejou"])
        if d > date_ref:
            continue
        script = SCRIPTS / f"{ligne['id']}.py"
        if ligne["lien_donnees"] is None:
            ligne["verdict"] = ("dormeuse : aucune donnée publiée au "
                                "rejou — conditions de mort non "
                                "testables")
            ligne["statut"] = "rejugée"
        elif script.exists():
            r = subprocess.run([sys.executable, str(script),
                                ligne["lien_donnees"]],
                               capture_output=True, text=True,
                               timeout=300)
            ligne["verdict"] = (r.stdout.strip()
                                or f"script sortie {r.returncode}")
            ligne["statut"] = "rejugée"
        else:
            ligne["verdict"] = ("rejugée — constatation manuelle "
                                "(aucun script joint)")
            ligne["statut"] = "rejugée"
        modifie = True
        print(f"{ligne['id']} → {ligne['statut']} : {ligne['verdict']}")
    if modifie:
        FICHIER.write_text("".join(json.dumps(l, ensure_ascii=False)
                                   + "\n" for l in lignes),
                           encoding="utf-8")
        print("REGISTRE.jsonl mis à jour — commiter pour sceller "
              "le rejou.")
    else:
        print("aucune entrée à rejouer à la date de référence.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
