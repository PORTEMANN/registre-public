# Registre public scellé

**Quoi.** Un registre où l'on dépose le **hash SHA-256 d'un protocole
avant la mesure** — protocole d'analyse, prédiction chiffrée, critère
de conformité — avec ses conditions de validation et de mort datées.
Quand les données arrivent, le registre **rejoue** et rend un verdict.
Personne n'a à croire le serveur : le dépôt Git public est le registre,
les commits sont les horodatages, quiconque peut rejouer.

**Doctrine** (adoptée le 2026-10-21, voir
[NOTE-APPLICATIONS](https://github.com/PORTEMANN/noetic-machine-complete/blob/main/docs/NOTE-APPLICATIONS.md)) :

1. **Vérifiabilité rejouable** — jamais de calcul caché ; le service
   héberge les scellements et les registres, pas le calcul.
2. **Dormeurs publiés** — les rejou rendent leurs verdicts négatifs et
   leurs entrées dormantes au même titre que les positifs.
3. **Registres séparés** — ce registre est distinct du corpus physique
   (le 59 meV et la veille scientifique restent canoniques dans
   `noetic-machine-complete`).

## Comment déposer

1. Rédigez votre protocole (texte, script, critères) — tenez-le
   privé jusqu'au rejou s'il est sensible.
2. Calculez son SHA-256 : `sha256sum protocole.txt`.
3. Ajoutez une entrée dans `REGISTRE.jsonl` (voir le schéma ci-dessous)
   et proposez une pull request — ou écrivez à
   patrice@portemann.eu pour un dépôt assisté.
4. Le dépôt validé et commité est votre scellement : horodaté par le
   commit, public, infalsifiable a posteriori.

## Schéma d'entrée (REGISTRE.jsonl)

```json
{
  "id": "REG-2026-001",
  "depot": "2026-10-21",
  "deposant": "nom ou pseudonyme",
  "description": "ce qui est scellé, en une phrase",
  "hash_protocole": "sha256 hex du protocole (64 caractères)",
  "conditions_mort": "ce qui tue la prédiction, daté",
  "date_rejou": "YYYY-MM-DD (trimestriel : 01-01, 04-01, 07-01, 10-01)",
  "statut": "dort | rejugée | morte | confirmée",
  "verdict": null,
  "lien_donnees": "URL des données publiées (le jour du rejou)"
}
```

## Le rejou trimestriel

Aux dates trimestrielles, le moteur (`moteur/rejouer.py`) :
vérifie l'ancrage de chaque entrée (le hash déposé n'a pas changé),
constate les données publiées, exécute le protocole déclaré si un
script est joint, et écrit le verdict dans l'entrée — **y compris
« morte » et « dormeuse »**. Le registre se pilote lui-même : les
verdicts sont des commits publics.

## Vérifier l'intégrité du registre

```bash
python moteur/valider.py
```

Calcule le hash d'ancrage du registre (SHA-256 de `REGISTRE.jsonl`)
et contrôle le schéma de chaque entrée. Ce hash est l'ancre : toute
modification rétroactive le change.

## Statut

Phase 1 de la feuille de route (2026-10-21) — moteur et schéma
fonctionnels, première entrée démo. La page publique de consultation vit sur
portemann.eu (carte de visite, à côté de la veille — rendu du présent
dépôt, rien ne s'exécute côté serveur : un rendu statique régénéré à
chaque commit). MIT, stdlib Python seulement.
