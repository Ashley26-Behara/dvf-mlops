"""Nettoie les données DVF brutes et produit un dataset prêt pour le ML."""
from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")
OUT_PATH = Path("data/processed/dvf_clean.parquet")

USECOLS = [
    "id_mutation", "date_mutation", "nature_mutation", "valeur_fonciere",
    "code_postal", "code_commune", "nom_commune", "code_departement",
    "type_local", "surface_reelle_bati", "nombre_pieces_principales",
    "surface_terrain", "longitude", "latitude",
]


def load_raw() -> pd.DataFrame:
    files = sorted(RAW_DIR.glob("dvf_*.csv.gz"))
    if not files:
        raise FileNotFoundError("Aucun fichier dans data/raw. Lance d'abord `make data`.")
    dtypes = {"code_postal": "string", "code_commune": "string", "code_departement": "string"}
    frames = [pd.read_csv(f, usecols=USECOLS, dtype=dtypes) for f in files]
    return pd.concat(frames, ignore_index=True)


def clean(df: pd.DataFrame) -> pd.DataFrame:
    n0 = len(df)

    # 1. Uniquement les ventes d'appartements et de maisons
    df = df[(df["nature_mutation"] == "Vente")
            & (df["type_local"].isin(["Appartement", "Maison"]))]

    # 2. Pas de valeurs manquantes sur les variables essentielles
    df = df.dropna(subset=["valeur_fonciere", "surface_reelle_bati",
                           "nombre_pieces_principales", "longitude", "latitude"])

    # 3. Une mutation = un seul bien (évite les ventes multi-lots au prix ambigu)
    counts = df.groupby("id_mutation")["type_local"].transform("size")
    df = df[counts == 1]

    # 4. Filtres de cohérence (outliers)
    df = df.assign(prix_m2=df["valeur_fonciere"] / df["surface_reelle_bati"])
    df = df[
        df["surface_reelle_bati"].between(9, 400)
        & df["nombre_pieces_principales"].between(1, 10)
        & df["prix_m2"].between(500, 30_000)
    ].copy()

    # 5. Features temporelles et dédoublonnage
    df["date_mutation"] = pd.to_datetime(df["date_mutation"])
    df["annee"] = df["date_mutation"].dt.year
    df["mois"] = df["date_mutation"].dt.month
    df = df.drop_duplicates(subset=["id_mutation"]).reset_index(drop=True)

    if n0:
        print(f"Lignes : {n0:,} -> {len(df):,} ({len(df) / n0:.1%} conservées)")
    return df


def main() -> None:
    df = clean(load_raw())
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUT_PATH, index=False)
    print(f"Sauvegardé : {OUT_PATH}")
    print(df[["valeur_fonciere", "surface_reelle_bati", "prix_m2"]].describe().round(0))


if __name__ == "__main__":
    main()
