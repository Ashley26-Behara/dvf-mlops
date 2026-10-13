import pandas as pd

from src.data.clean import clean


def make_row(**kw):
    base = dict(id_mutation="A", date_mutation="2023-05-01", nature_mutation="Vente",
                valeur_fonciere=300_000, code_postal="75011", code_commune="75111",
                nom_commune="Paris 11e", code_departement="75", type_local="Appartement",
                surface_reelle_bati=50, nombre_pieces_principales=2, surface_terrain=None,
                longitude=2.38, latitude=48.86)
    base.update(kw)
    return base


def test_keeps_valid_row():
    out = clean(pd.DataFrame([make_row()]))
    assert len(out) == 1
    assert out.loc[0, "prix_m2"] == 6000


def test_drops_outlier_price():
    out = clean(pd.DataFrame([make_row(valeur_fonciere=1_000)]))
    assert out.empty


def test_drops_multi_lot_mutation():
    rows = [make_row(id_mutation="B"), make_row(id_mutation="B", surface_reelle_bati=30)]
    assert clean(pd.DataFrame(rows)).empty
