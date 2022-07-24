from django.test import TransactionTestCase
from uuid import uuid4


class BookingTestCase(TransactionTestCase):
    databases = "__all__"

    def test_make_reservation_for_non_existet_screening_returns_400(self):
        res = self.client.post(
            "/make-reservation",
            {
                "customer_id": str(uuid4()),
                "screening_id": str(uuid4()),
                "reservation_number": str(uuid4()),
                "seats_data": [["a", 1], ["b", 2]],
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)

    def test_cancel_reservation_for_non_existet_screening_returns_400(self):
        res = self.client.post(
            "/cancel-reservation",
            {
                "screening_id": str(uuid4()),
                "reservation_number": str(uuid4()),
            },
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)
