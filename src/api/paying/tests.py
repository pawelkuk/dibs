from django.test import TransactionTestCase
from uuid import uuid4


class PaymentTestCase(TransactionTestCase):
    databases = "__all__"

    def test(
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
        import bpdb

        bpdb.set_trace()
