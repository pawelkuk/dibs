from uuid import uuid4
from django.core.management.base import BaseCommand
from paying.domain.model import PaymentStatus
from ticketing.domain.model import TicketStatus
from booking import models
from paying.models import Payment
from ticketing.models import Ticket
from itertools import product
import random


class Command(BaseCommand):
    help = "Initial data for booking service"

    def add_arguments(self, parser):
        ...

    def handle(self, *args, **options):
        rows = range(1, 11)
        places = (chr(ord("a") + i) for i in range(20))
        theatre_seats = [[row, place] for row, place in product(rows, places)]
        theatre = models.Theatre(seats=theatre_seats)
        theatre.save()

        movie_titles = [
            "The Seven Samurai",
            "The Godfather",
            "The Wizard of Oz",
            "Citizen Kane",
            "The Shawshank Redemption",
            "Pulp Fiction",
            "Casablanca",
            "2001: A Space Odyssey",
            "Schindler's List",
            "Star Wars",
            "Back to the Future",
            "Raiders of the Lost Ark",
            "Forrest Gump",
            "It's a Wonderful Life",
            "Chinatown",
        ]
        movies = [models.Movie.objects.create(title=title) for title in movie_titles]

        def seat_generator():
            taken_seats = random.sample(theatre_seats, len(theatre_seats) // 2)
            for seat in taken_seats:
                yield seat

        screening = models.Screening.objects.create(
            theatre=theatre, movie=random.choice(movies)
        )
        seats = seat_generator()
        while True:
            reservation = models.Reservation()
            n_of_seats = random.randint(1, 4)
            try:
                reservation.seats = [next(seats) for _ in range(n_of_seats)]
            except Exception:
                break
            reservation.screening = screening
            reservation.customer_id = uuid4()
            reservation.save()
            if random.random() < 0.5:
                continue
            payment = Payment(
                user_id=reservation.customer_id,
                payment_id=uuid4(),
                status=PaymentStatus.SUCCESS.value,
                currency=random.choice(["USD", "PLN", "GBP"]),
                amount="9.99",
            )
            payment.save()
            if random.random() < 0.5:
                continue

            ticket = Ticket(
                ticket_id=uuid4(),
                reservation_id=reservation.reservation_number,
                status=TicketStatus.SUCCESS.value,
                ticket_url=f"/dibs_tickets/some-s3-path/{uuid4()}.pdf",
            )
            ticket.save()

        self.stdout.write("Data created 🍏")
