from typing import Any

from django.test import SimpleTestCase

from api.tasks import PaymentStep, ReservationStep, Saga, TicketingStep


class TestStep:
    call_count = 0
    data = None

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
        TestStep.data = None
        self.s = Saga(
            [
                ReservationTestStep(),
                PaymentTestStep(),
                TicketingTestStep(),
            ]
        )
        super().setUp()

    def test_happy_path(self):
        def make_request(self, endpoint: str, expected_input: dict[str, Any]):
            TestStep.call_count += 1
            TestStep.data = expected_input
            return expected_input, True

        TestStep.make_request = make_request
        success = self.s.do()
        self.assertTrue(success)
        self.assertEqual(TestStep.call_count, 3)
        self.assertEqual(TestStep.data, {"passed": "through saga"})

    def test_reservation_first_step_fails(self):
        def make_request(self, endpoint: str, expected_input: dict[str, Any]):
            TestStep.call_count += 1
            TestStep.data = expected_input
            if endpoint == "make-reservation":
                return expected_input, False
            return expected_input, True

        TestStep.make_request = make_request
        success = self.s.do()
        self.assertFalse(success)
        self.assertEqual(TestStep.call_count, 1)
        self.assertEqual(TestStep.data, {"passed": "through saga"})

    def test_payment_second_step_fails(self):
        def make_request(self, endpoint: str, expected_input: dict[str, Any]):
            TestStep.call_count += 1
            TestStep.data = expected_input

            if endpoint == "pay":
                return expected_input, False
            return expected_input, True

        TestStep.make_request = make_request
        success = self.s.do()
        self.assertFalse(success)
        self.assertEqual(TestStep.call_count, 3)
        self.assertEqual(TestStep.data, {"passed": "through saga"})

    def test_ticket_rendering_third_step_fails(self):
        def make_request(self, endpoint: str, expected_input: dict[str, Any]):
            TestStep.call_count += 1
            TestStep.data = expected_input

            if endpoint == "render-ticket":
                return expected_input, False
            return expected_input, True

        TestStep.make_request = make_request
        success = self.s.do()
        self.assertFalse(success)
        self.assertEqual(TestStep.call_count, 5)
        self.assertEqual(TestStep.data, {"passed": "through saga"})
