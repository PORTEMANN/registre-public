#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Registre public scelle — validateur et ancre d'integrite.

Verifie le schema de chaque entree de REGISTRE.jsonl et calcule
l'ancre du registre : le SHA-256 du fichier. Toute modification
retroactive de n'importe quelle entree change cette ancre — c'est
le mecanisme d'infalsifiabilite. Stdlib seulement, MIT.

Usage : python moteur/valider.py
"""
import hashlib
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
FICHIER = RACINE / "REGISTRE.jsonl"

CHAMPS = ["id", "depot", "deposant", "description", "hash_protocole",
          "conditions_mort", "date_rejou", "statut", "verdict",
          "lien_donnees"]
STATUTS = {"dort", "rejugée", "morte", "confirmée"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def valider_ligne(ligne, numero):
    erreurs = []
    for champ in CHAMPS:
        if champ not in ligne:
            erreurs.append(f"ligne {numero}: champ manquant '{champ}'")
    if erreurs:
        return erreurs
    if not SHA256.match(ligne["hash_protocole"]):
        erreurs.append(f"ligne {numero}: hash_protocole invalide")
    if ligne["statut"] not in STATUTS:
        erreurs.append(f"ligne {numero}: statut '{ligne['statut']}' "
                       f"inconnu")
    return erreurs


def main():
    brut = FICHIER.read_bytes()
    ancre = hashlib.sha256(brut).hexdigest()
    lignes = [json.loads(l)
              for l in brut.decode("utf-8").splitlines() if l.strip()]
    erreurs = []
    ids = set()
    for i, ligne in enumerate(lignes, 1):
        erreurs += valider_ligne(ligne, i)
        if ligne["id"] in ids:
            erreurs.append(f"ligne {i}: id dupliqué '{ligne['id']}'")
        ids.add(ligne["id"])
    print("=" * 72)
    print(f"REGISTRE PUBLIC — {len(lignes)} entrée(s)")
    print(f"ancre SHA-256 : {ancre}")
    for ligne in lignes:
        v = ligne["verdict"] if ligne["verdict"] else "—"
        print(f"  {ligne['id']} [{ligne['statut']}] {ligne['description']}"
              f" → {v}")
    if erreurs:
        print("ERREURS :")
        for e in erreurs:
            print("  -", e)
        sys.exit(1)
    print("schéma valide — aucune erreur")


if __name__ == "__main__":
    main()
