# Master thesis

## TODO:
- [x] pgadmin init config
- [x] implement db per app
- [x] paying service
- [x] ticketing service
- [x] scripts for initial data
- [x] read model service
    - [x] update read service during saga
    - [x] push updates to FE
- [x] FE
    - [x] room component
    - [x] post request
    - [x] seat picker
    - [x] update room after read service update 
    - [x] fix bug where too many sockets were being created
- [x] integration tests
    - [x] paying
    - [x] ticketing
- [x] orchestrating service/choreographing
    - [x] setup rabbitmq + celery
    - [x] setup auto-reload for celery
    - [x] write controller (saga workflow) as celery task/multiple tasks
- [ ] experiment
    - [x] script which will reserve seats concurrently
    - [ ] alternative - wait for response and only then send next request
    - [x] stats from experiments
        - [x] avg time to reserve seats
        - [x] number of requests which failed
        - [x] number of requests which succeeded
        - [x] time of experiment
    - [x] find out why inconsistent reservations appear
    - [x] check that payments and ticket renders are all correct
    - [x] check for correctness under heavy load
    - [x] write trigger/check for uniqueness of reserved seats
    - [x] different container for read and write path (CQRS) because due to writes reads become unresponsive due to queueing up requests on django
    - [x] read model service shows all screenings instead of just one with uuid given in url
    - [x] benchmark przepisać na CLI
    - [x] fix amount of queries generated by orm
- [x] distributed transactions approach
- [x] use uwsgi instead of django dev server
- [x] check periodically for updates in read model service
