"""Tests for sample data ingestion helper."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ingest_sample_data import load_csv


def test_load_customers():
    rows = load_csv("customers.csv")
    assert len(rows) == 5
    assert rows[0]["name"] == "Alice Johnson"


def test_load_transactions():
    rows = load_csv("transactions.csv")
    assert len(rows) == 11


def test_load_credit_cards():
    rows = load_csv("credit_cards.csv")
    assert len(rows) == 5
