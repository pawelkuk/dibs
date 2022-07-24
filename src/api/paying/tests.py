from django.test import TransactionTestCase
from uuid import uuid4


class PaymentTestCase(TransactionTestCase):
    databases = "__all__"

    def test_payment(
        self,
    ):
        res = self.client.post(
            "/pay",
            data={
                "amount": "32.32",
                "currency": "USD",
                "user_id": str(uuid4()),
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)

    def test_refund(
        self,
    ):
        res = self.client.post(
            "/pay",
            data={
                "amount": "32.32",
                "currency": "USD",
                "user_id": str(uuid4()),
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
        payment_id: str = res.json()["payment_id"]
        res = self.client.post(
            "/refund",
            data={
                "payment_id": payment_id,
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 204)
