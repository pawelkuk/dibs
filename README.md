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
- [x] integration tests
    - [x] paying
    - [x] ticketing
- [x] orchestrating service/choreographing
    - [x] setup rabbitmq + celery
    - [x] setup auto-reload for celery
    - [x] write controller (saga workflow) as celery task/multiple tasks
- [ ] experiment
    - [x] script which will reserve seats concurrently
    - [ ] check for correctness under heavy load
    - [ ] write trigger/check for uniqueness of reserved seats
    - [x] different container for read and write path (CQRS) because due to writes reads become unresponsive due to queueing up requests on django
    - [x] read model service shows all screenings instead of just one with uuid given in url
    - [ ] benchmark przepisać na CLI
- [x] distributed transactions approach
