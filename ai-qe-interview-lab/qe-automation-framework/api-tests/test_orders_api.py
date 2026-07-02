"""API test suite: contract, negative, and lifecycle tests for the Orders API."""

VALID_ORDER = {"email": "qa@example.com", "total": 49.99}


class TestCreateOrder:
    def test_create_order_returns_201_with_contract(self, api, base_url):
        resp = api.post(f"{base_url}/api/orders", json=VALID_ORDER)
        assert resp.status_code == 201
        body = resp.json()
        # contract: exact response shape
        assert set(body.keys()) == {"id", "email", "total", "status"}
        assert body["status"] == "CREATED"
        assert body["email"] == VALID_ORDER["email"]
        assert body["total"] == VALID_ORDER["total"]

    def test_missing_email_returns_400(self, api, base_url):
        resp = api.post(f"{base_url}/api/orders", json={"total": 49.99})
        assert resp.status_code == 400
        assert "email" in resp.json()["error"]

    def test_invalid_email_returns_400(self, api, base_url):
        resp = api.post(f"{base_url}/api/orders", json={"email": "not-an-email", "total": 10})
        assert resp.status_code == 400

    def test_negative_total_returns_400(self, api, base_url):
        resp = api.post(f"{base_url}/api/orders", json={"email": "qa@example.com", "total": -5})
        assert resp.status_code == 400
        assert "total" in resp.json()["error"]

    def test_malformed_json_returns_400(self, api, base_url):
        resp = api.post(
            f"{base_url}/api/orders",
            data="{not json",
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 400


class TestGetOrder:
    def test_unknown_order_returns_404(self, api, base_url):
        resp = api.get(f"{base_url}/api/orders/doesnotexist")
        assert resp.status_code == 404

    def test_order_lifecycle_create_then_get(self, api, base_url):
        created = api.post(f"{base_url}/api/orders", json=VALID_ORDER).json()
        resp = api.get(f"{base_url}/api/orders/{created['id']}")
        assert resp.status_code == 200
        assert resp.json() == created


class TestHealth:
    def test_health_returns_ok(self, api, base_url):
        resp = api.get(f"{base_url}/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}
