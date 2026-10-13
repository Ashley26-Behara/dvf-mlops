# DVF MLOps : prédiction de prix immobiliers

Pipeline ML complet, de la donnée brute (transactions réelles DVF) à une API déployée et monitorée.

## Problématique
Estimer le prix d'un bien (appartement ou maison) en Île-de-France à partir de ses caractéristiques
et de sa localisation, puis garantir la qualité du modèle dans le temps (suivi, dérive, reproductibilité).

## Stack
Python · pandas · scikit-learn · XGBoost · SHAP · MLflow · DVC · FastAPI · Docker · GitHub Actions · Evidently

## Roadmap
- [x] Étape 1 : téléchargement et nettoyage des données DVF
- [ ] Étape 2 : exploration (EDA) et feature engineering
- [ ] Étape 3 : modèle baseline vs XGBoost, suivi MLflow
- [ ] Étape 4 : explicabilité avec SHAP
- [ ] Étape 5 : API FastAPI + Docker
- [ ] Étape 6 : CI/CD avec GitHub Actions
- [ ] Étape 7 : monitoring de la dérive avec Evidently

## Démarrage rapide
```bash
python -m venv .venv && source .venv/bin/activate
make install
make data    # télécharge DVF (75, 92, 93, 94 / 2021-2023)
make clean   # produit data/processed/dvf_clean.parquet
make test
```

## Source des données
[Géo-DVF](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres-geolocalisees/) (data.gouv.fr, Licence Ouverte).

## Structure
```
src/data/       téléchargement et nettoyage
notebooks/      exploration
tests/          tests unitaires
data/           données (non versionnées)
```
