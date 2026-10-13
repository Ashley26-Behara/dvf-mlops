# %% 1. Charger les données
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

candidats = [Path("data/processed/dvf_clean.parquet"),
             Path("../data/processed/dvf_clean.parquet")]
chemin = next(p for p in candidats if p.exists())

df = pd.read_parquet(chemin)
print(f"{len(df):,} ventes, {df.shape[1]} colonnes")
df.head()

# %% 2. Prix au m² médian par département
prix_dept = df.groupby("code_departement")["prix_m2"].median().sort_values()
print(prix_dept.round(0))

prix_dept.plot.bar(title="Prix médian au m² par département", ylabel="€ / m²")
plt.xticks(rotation=0)
plt.show()

# %% 3. Distribution des prix au m²
df["prix_m2"].hist(bins=60)
plt.title("Répartition des prix au m²")
plt.xlabel("€ / m²")
plt.ylabel("Nombre de ventes")
plt.show()

# %% 4. Évolution du prix au m² dans le temps
df["periode"] = df["date_mutation"].dt.to_period("M").dt.to_timestamp()
evolution = df.groupby("periode")["prix_m2"].median()

evolution.plot(title="Prix médian au m² par mois", ylabel="€ / m²")
plt.show()

# %% 5. Prix en fonction de la surface (échantillon de 5000 ventes)
df.sample(5000, random_state=0).plot.scatter(
    x="surface_reelle_bati", y="valeur_fonciere", alpha=0.3,
    title="Prix de vente selon la surface")
plt.show()

# %% 6. Communes les plus chères et les moins chères
stats = df.groupby("nom_commune")["prix_m2"].agg(["median", "count"])
stats = stats[stats["count"] >= 200].sort_values("median")

print("Les 10 moins chères :")
print(stats.head(10).round(0))
print("\nLes 10 plus chères :")
print(stats.tail(10).round(0))