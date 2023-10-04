## Experiment design and description

The script which implements the experiment works as follows:

- it tries to book all available seats in all cinema rooms,
- it books via the API, which means that it uses the same interface as the users,
- the degree of concurrency can be altered via the script's parameters,
- also one can specify whether the seat should be booked using the saga pattern or the two phase commit protocol
- the script measures the time it took to book all seats, it stores information about every booking request as well as the status or result of the booking request,
- stores the information in a file, which can be later used to generate graphs and statistics,
- it checks the result of the experiment for correctness, i.e. it checks whether no seat was booked twice and whether all bookings have associated payment and ticket records,
- it can be run multiple times, each time the results are stored in a separate files.

### Experiment pseudocode

```python=
for screening in movie_screenings:
    async while any_seat_is_available():
        seats = pick_available_seats_to_book_at_random()
        for batch in seats:
            book_seats_with_saga_pattern_or_2PC_asynchronously(batch)
        wait_for_all_bookings_to_finish()
    check_experiment_result_for_errors()
```
