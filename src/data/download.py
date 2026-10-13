"""Télécharge les fichiers Géo-DVF (transactions immobilières) depuis data.gouv.fr."""
import argparse
from pathlib import Path

import requests

BASE_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/{year}/departements/{dept}.csv.gz"
RAW_DIR = Path("data/raw")


def download(dept: str, year: int) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    dest = RAW_DIR / f"dvf_{year}_{dept}.csv.gz"
    if dest.exists():
        print(f"[skip] {dest} existe déjà")
        return dest

    url = BASE_URL.format(year=year, dept=dept)
    print(f"[download] {url}")
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 20):
                f.write(chunk)
    return dest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dept", nargs="+", required=True, help="ex: 75 92 93")
    parser.add_argument("--years", nargs="+", type=int, required=True, help="ex: 2022 2023")
    args = parser.parse_args()

    for year in args.years:
        for dept in args.dept:
            try:
                download(dept, year)
            except requests.HTTPError as e:
                print(f"[erreur] {dept}/{year}: {e}")


if __name__ == "__main__":
    main()
