## Technologies used in the project

- JavaScript + React.js - for the frontend application which visualizes the cinema rooms, booking process as well allows the use user book seats themselves
- Node.js + Express + Socket.io - for realtime communication between the frontend and the read model of the application, it allows the frontend to be notified about changes in the read model without the need to poll the backend
- Django - for the backend application which implements the business logic of the application, it also provides the API for the frontend application
- SqlAlchemy - for the ORM layer of the backend application, it allows to query the database in a more convenient way than using raw SQL, it can be configured to use sql queries for the 2 phase commit protocol,
- Postgres - for the database layer of the application, it is used to store the data about bookings, payments and tickets,
- HaProxy - for the reverse proxy layer of the application, it is used to load balance the requests between the backend instances,
- Docker - for containerization of the application, it allows to run the application on any machine which has docker installed,
- Rabbitmq + Celery - for the message broker layer of the application, it is used to notify the saga pattern workflow as well as for notifying the read model about new bookings,
- Python - for the implementation of the backend application, it is used because of the Django framework and SqlAlchemy ORM,
- Typescript - for the implementation of the experiment script, since it is well suited for dealing with concurrency and IO workloads,
- Rust - for the analysis of the experiment results as well as result visualization in the form of graphs and statistics.

## Application logic description

The reservation process consists of the following steps:

- the user selects the movie screening and the seats they want to book,
- the frontend application sends a request to the backend application to book the selected seats,
- the backend application checks whether the seats are available,
- if the seats are available, then the following three things happen atomically on different databases in this order:
  1. the seats are be marked as booked,
  2. the payment is be made,
  3. the ticket is be generated,
- if any of the steps fails then the whole process is rolled back and the seats are marked as available again,
- the frontend application is notified about the result of the booking process.

### Difference between distributed saga pattern and two phase commit protocol

The difference between the distributed saga pattern and the two phase commit protocol is that in the saga pattern the rollback is done by executing compensating actions, while in the two phase commit protocol the rollback is done by executing the rollback phase of the transaction. In the saga pattern the compensating actions are executed in the reverse order of the original actions. In the two phase commit protocol the rollback phase is executed by the coordinator of the transaction, which is the coordinator database instance. In the case of the saga pattern the rollback is done by the backend application so there are intermediate steps where the database state isn't consistent. Consistency is guaranteed on the application level, not on the database level. In the case of the two phase commit protocol the rollback is done by the database so there are no intermediate steps where the database state isn't consistent. Consistency is guaranteed on the database level, not on the application level.

## High-level architecture

### Backend architecture

### Frontend architecture

### Database layer architecture

### Architecture diagram

![Architecture diagram](assets/dibs-architecture.png "Architecture diagram")

## Implementation details

## Problems and pitfalls

### n+1 query problem and unnecessary queries in Django ORM

The N+1 query problem is a common problem in ORMs. It happens when the ORM executes N+1 queries instead of 1 query. For example, when we want to get all the reserved seats and for each screening. In this case the ORM will execute 1 query to get all the screenings and then N queries to get all the reservation seats for each screening. This is a problem because it lead to performance issues and it does not reflect the sql queries created by SqlAlchemy. I solved the problem by rewriting the logic in SqlAlchemy where I could take advantage of eagerly loading this foreign key relationship. This results in 1 big query instead of N+1 small queries.

### Postgres instances configuration for distributed transactions

Postgres does not support distributed transaction by default. It needs to be configured first. In order to do so I had to configure the postgres instances to use the 2 phase commit protocol. This required setting the `max_prepared_transactions` GUC parameter to a non-zero value. It controls the upper bound of the number of foreign transactions the coordinator server controls. Since one transaction could accesses multiple foreign servers, this parameter has to be set to: `(max_connections) * (# of foreign servers that are capable of 2PC)` ([source](https://wiki.postgresql.org/wiki/Atomic_Commit_of_Distributed_Transactions)). The other participant instances have to set the `max_prepared_transactions` to `max_connections` of the coordinator. After this SqlAlchemy can be configured to use the 2 phase commit protocol as well by setting `twophase=True` in the sessionmaker ([source](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#enabling-two-phase-commit)).

### Postgres database connection configuration

Postgres can run out of connections. This is a problem because the application will not be able to connect to the database. It can be solved in two ways. Either by running a connection pooler (like PgBouncer) in front of the database or by increasing the number of connections in the postgres configuration file. I oped for the second approach. This was implemented by setting the `max_connections` parameter to a higher value. This parameter controls the maximum number of concurrent connections to the database server. Setting it to a higher value has also its drawbacks. It increases the memory usage of the database server. It also increases the number of locks the database server has to manage. This can lead to performance issues. However, finding an optimal values for this parameter and handling the performance issues is out of scope of this thesis.

### Webserver configuration (number of workers)

To complete a saga workflow the backend application has to execute multiple steps. Each step in the saga is a separate http request to the backend application. If the number of worker threads is too low then the backend application will not be able to accept the request in time and timeout the request. This will lead to the saga workflow not being completed. If the number of workers is too high then the backend application has other problems. The web server is limited by available resources of the underlying host. If the number of concurrent requests is too big then this leads to a big memory footprint, a greater cost for context switching and eventually to greater time for request processing/timeouts. This will lead to the saga workflow not getting completed. Finding an optimal value for the number of worker processes/threads is out of scope of this thesis. It was enough to set the number of workers to a high value (20 processes \* 5 thread per process = 100 worker threads) to prevent requests from being timed out/not accepted at all.

### Reverse proxy configuration

It was enough to set the number of workers to a higher value then the number of workers in the backend application. This was done by setting the `maxconn` parameter to a higher value. This parameter controls the maximum number of concurrent connections to the backend application. Setting it to a higher value has also its drawbacks. It increases the memory usage of the reverse proxy server. It also increases the number of locks the reverse proxy server has to manage. This can lead to performance issues. However, no problems of this sort were encountered during the experiment.

### Too many websockets connections creation

React rebuilds the DOM tree every time the state changes. This means that every time the state changes the DOM tree is rebuilt and all the components are recreated. This means that every time the state changes the websocket connection is recreated. This is a problem because the backend application has a limit on the number of websocket connections it can handle. This means that if the state changes too often then the backend application will not be able to handle all the websocket connections. This bug was caused due to placing the websocket connection creation logic in a react hook component which get rerendered every time the state changes. I solved this problem by moving the websocket connection creation logic to a react component which only gets rerendered at the appropriate time. This means that the websocket connection is created only once on screening room entering.
