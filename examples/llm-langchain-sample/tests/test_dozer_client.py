"""Tests for the Dozer client (mocked)."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from unittest.mock import patch, MagicMock
from dozer_client import DozerClient


def test_get_customer_profile_filters():
    client = DozerClient("http://localhost:8080")
    fake_records = [
        {"customer_id": 1, "name": "Alice"},
        {"customer_id": 2, "name": "Bob"},
    ]
    with patch.object(client, "get_records", return_value=fake_records):
        assert client.get_customer_profile(2) == {"customer_id": 2, "name": "Bob"}
        assert client.get_customer_profile(99) is None


def test_get_transactions_filter():
    client = DozerClient("http://localhost:8080")
    fake = [
        {"transaction_id": 1, "customer_id": 1, "amount": 10.0},
        {"transaction_id": 2, "customer_id": 2, "amount": 20.0},
    ]
    with patch.object(client, "get_records", return_value=fake):
        res = client.get_transactions(1)
        assert len(res) == 1
        assert res[0]["customer_id"] == 1
