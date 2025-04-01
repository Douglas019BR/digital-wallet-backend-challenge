[🇺🇸](#) | [🇧🇷](README-pt.md)

## Considerations

It would be possible to develop a better approach for database testing. I prefer the approach of creating a local container with a test database to make it completely independent from the project's database.
For simplicity and due to time constraints, I'll maintain the approach of simply creating a test user in the database and mocking other database calls.

Due to FastAPI's test organization, combined with the lack of specificity for unit tests but rather for automated tests, the tests were developed around routes, not necessarily around units. This characterizes them more as integration/API tests than actual unit tests. This choice ensures greater test coverage with fewer tests and also better application functioning, as it effectively tests the operation of each route.