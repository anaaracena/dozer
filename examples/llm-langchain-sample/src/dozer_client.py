"""Client for querying the Dozer REST API."""

import requests


class DozerClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip("/")

    def list_endpoints(self):
        resp = requests.get(f"{self.base_url}/", timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_records(self, endpoint: str, limit: int = 100):
        resp = requests.get(f"{self.base_url}/{endpoint}", params={"limit": limit}, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def get_customer_profile(self, customer_id: int):
        records = self.get_records("customer_profile", limit=1000)
        for r in records:
            if r.get("customer_id") == customer_id:
                return r
        return None

    def get_credit_cards(self):
        return self.get_records("credit_cards", limit=1000)

    def get_transactions(self, customer_id: int = None):
        records = self.get_records("transactions", limit=1000)
        if customer_id is not None:
            records = [r for r in records if r.get("customer_id") == customer_id]
        return records
