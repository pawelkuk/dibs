## Saga

The idea of a saga was introduced by Hector Garcia-Molina and Kenneth Salem in 1987 in their paper "Sagas" ([source](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf)). The saga pattern is a pattern for implementing long-lived transactions with some consistency guarantees. It is based on the idea that a long-lived transaction can be divided into a series of subtransactions (`T_1, T_2, ..., T_n`) and corresponding compensating actions (`C_1, C_2, ..., C_n-1`). If a subtransaction `T_i` fails then the compensating actions of the previous subtransactions are executed in reverse order to rollback the changes made by the previous subtransactions (`C_i-1, C_i-2, ..., C_1`). Providing that the compensating actions are implemented correctly, the saga will either complete successfully (every subtransaction is committed) or eventually it will be rolled back to the initial state (every committed subtransaction is rolled back by their corresponding compensating action).

## Distributed Saga

The paper discusses only the case of a single instance database. It says:

> Due to space limitations, we only discuss sagas in a centralized system, although clearly they can be implemented in a distributed database system.

### Advantages and Drawbacks of using Sagas

### Expected problems

## Choreography vs. Orchestration

## Two phase commit protocol

### Advantages and Drawbacks of using 2PC

### Expected problems
