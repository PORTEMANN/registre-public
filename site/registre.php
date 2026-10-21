<?php
/**
 * Registre public scellé — rendu pour histoire-des-sciences.eu
 *
 * Doctrine (NOTE-APPLICATIONS, adoptée 2026-10-21) : jamais de calcul
 * côté serveur. Cette page ne fait que LIRE le dépôt canonique
 * (GitHub PORTEMANN/registre-public) et le rendre. Le registre est le
 * dépôt ; les commits en sont les horodatages ; quiconque peut rejouer.
 *
 * Déploiement : copier ce fichier dans /theos-tech/registre.php et
 * adapter $SOURCE (brute du REGISTRE.jsonl distante, mise en cache
 * locale de 3600 s par courtoisie).
 */

$SOURCE = 'https://raw.githubusercontent.com/PORTEMANN/registre-public/main/REGISTRE.jsonl';
$CACHE = __DIR__ . '/cache_registre.jsonl';

function lire_registre($source, $cache) {
    $frais = file_exists($cache) && (time() - filemtime($cache) < 3600);
    $brut = $frais ? file_get_contents($cache)
                   : @file_get_contents($source);
    if ($brut === false) {
        $brut = file_exists($cache) ? file_get_contents($cache) : '';
    } else {
        file_put_contents($cache, $brut);
    }
    $lignes = [];
    foreach (explode("\n", trim($brut)) as $l) {
        if (trim($l) !== '') { $lignes[] = json_decode($l, true); }
    }
    return array_filter($lignes);
}

$entrees = lire_registre($SOURCE, $CACHE);
$ancre = hash('sha256', file_get_contents($CACHE));
$titre = 'Registre public scellé';
?>
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title><?= $titre ?> — Bibliothèque numérique</title>
<link rel="stylesheet" href="/theos-tech/assets/css/style.css">
</head>
<body>
<main class="contenu">
<div class="fil-ariane"><a href="/theos-tech/index.php">Accueil</a> &raquo; <?= $titre ?></div>
<h1><?= $titre ?></h1>
<p class="meta">Protocoles hachés <em>avant</em> la mesure · rejou
trimestriel · dormeurs publiés. Le dépôt
<a href="https://github.com/PORTEMANN/registre-public">GitHub</a>
est le registre (les commits en sont les horodatages) — cette page ne
fait que le lire. Ancre SHA-256 du registre :
<code><?= substr($ancre, 0, 16) ?>…</code></p>

<table>
<thead><tr><th>ID</th><th>Déposé</th><th>Description</th><th>Statut</th><th>Verdict</th></tr></thead>
<tbody>
<?php foreach ($entrees as $e): ?>
<tr>
<td><?= htmlspecialchars($e['id']) ?></td>
<td><?= htmlspecialchars($e['depot']) ?></td>
<td><?= htmlspecialchars($e['description']) ?></td>
<td><?= htmlspecialchars($e['statut']) ?></td>
<td><?= htmlspecialchars($e['verdict'] ?? '—') ?></td>
</tr>
<?php endforeach; ?>
</tbody>
</table>

<p>Pour déposer : ajoutez une entrée dans
<code>REGISTRE.jsonl</code> du dépôt (pull request) — voir le
<a href="https://github.com/PORTEMANN/registre-public">README du registre</a>.
Rien n'est calculé ici : tout se vérifie là-bas.</p>
</main>
</body>
</html>
