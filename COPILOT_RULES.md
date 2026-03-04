# Règles Copilot — Workspace tdenolle

## Push Git

**Toujours demander l'approbation de l'utilisateur avant de pusher sur `develop` ou `master`.**

- Jouer les tests
- Si les tests passent, présenter le résumé des changements et attendre le feu vert
- Seulement après confirmation explicite, exécuter `git push`

## Versioning

Format **CalVer** : `ANNEE.MOIS.INCREMENT` (ex: `2026.3.0`, `2026.3.1`, ...)

- Premier incrément du mois = `0`
- Versions dev : `ANNEE.MOIS.INCREMENT-dev.YYYYMMDDHHMMSS`
- Fichiers à synchroniser lors d'un bump de version :
  - `bayrol-poolaccess-mqtt/pyproject.toml`
