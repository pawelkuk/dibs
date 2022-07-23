from django.test import TransactionTestCase
from uuid import uuid4


class TicketTestCase(TransactionTestCase):
    databases = "__all__"

    def test(
        self,
    ):
        res = self.client.post(
            "/render-ticket",
            data={
                "details": {"some": "detail"},
                "reservation_id": str(uuid4()),
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 201)
