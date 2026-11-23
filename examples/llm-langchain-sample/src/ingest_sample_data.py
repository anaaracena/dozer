"""Helper to verify sample data files are present and well-formed."""

import csv
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_csv(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def main():
    for fname in ("customers.csv", "transactions.csv", "credit_cards.csv"):
        rows = load_csv(fname)
        print(f"{fname}: {len(rows)} rows loaded")
    print("Sample data OK.")


if __name__ == "__main__":
    main()
