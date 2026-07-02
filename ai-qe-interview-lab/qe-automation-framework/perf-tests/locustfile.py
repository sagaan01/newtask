"""Locust performance test: checkout API under load.

Run (app must be running on :8787):
    locust -f perf-tests/locustfile.py --headless -u 10 -r 5 -t 15s -H http://localhost:8787
"""

from locust import HttpUser, between, task


class CheckoutUser(HttpUser):
    wait_time = between(0.2, 1.0)

    @task(3)
    def create_order(self):
        with self.client.post(
            "/api/orders",
            json={"email": "perf@example.com", "total": 49.99},
            catch_response=True,
        ) as resp:
            if resp.status_code != 201:
                resp.failure(f"expected 201, got {resp.status_code}")
            elif resp.elapsed.total_seconds() > 2.0:
                resp.failure("SLA breach: >2s response time")

    @task(1)
    def health_check(self):
        self.client.get("/health")
