from typing import Any

from django.test import SimpleTestCase

from api.tasks import PaymentStep, ReservationStep, Saga, TicketingStep


class TestStep:
    call_count = 0

    def make_request(self, endpoint: str, expected_input: dict[str, Any]):
        raise NotImplementedError


class ReservationTestStep(TestStep, ReservationStep):
    pass


class PaymentTestStep(TestStep, PaymentStep):
    pass


class TicketingTestStep(TestStep, TicketingStep):
    pass


class TestSagaWorkflow(SimpleTestCase):
    def setUp(
        self,
    ):
        TestStep.call_count = 0
        self.s = Saga(
            [
                ReservationTestStep(),
                PaymentTestStep(),
                TicketingTestStep(),
            ],
            {},
        )
        super().setUp()

    def test_happy_path(self):
        def make_request(self, endpoint: str, expected_input: dict[str, Any]):
            TestStep.call_count += 1
            return {}, True

        TestStep.make_request = make_request
        success = self.s.do()
        self.assertTrue(success)
        self.assertEqual(TestStep.call_count, 3)

    def test_reservation_first_step_fails(self):
        def make_request(self, endpoint: str, expected_input: dict[str, Any]):
            TestStep.call_count += 1
            if endpoint == "make-reservation":
                return {}, False
            return {}, True

        TestStep.make_request = make_request
        success = self.s.do()
        self.assertFalse(success)
        self.assertEqual(TestStep.call_count, 1)

    def test_payment_second_step_fails(self):
        def make_request(self, endpoint: str, expected_input: dict[str, Any]):
            TestStep.call_count += 1
            if endpoint == "pay":
                return {}, False
            return {}, True

        TestStep.make_request = make_request
        success = self.s.do()
        self.assertFalse(success)
        self.assertEqual(TestStep.call_count, 3)

    def test_ticket_rendering_third_step_fails(self):
        def make_request(self, endpoint: str, expected_input: dict[str, Any]):
            TestStep.call_count += 1
            if endpoint == "render-ticket":
                return {}, False
            return {}, True

        TestStep.make_request = make_request
        success = self.s.do()
        self.assertFalse(success)
        self.assertEqual(TestStep.call_count, 5)
