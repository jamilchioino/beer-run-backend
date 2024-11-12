# Beer Run
A Python exercise to learn modern Python, tooling and architecture

## Starting the project
Make sure [uv](https://docs.astral.sh/uv/) is installed, then run:
```
uv sync
```
Then to start FastApi
```
uv run fastapi dev
```
## Run tests and pyright (optional)
Normally these would run as GitHub Actions against incoming pull requests, but you can run them as follows:
```
uv run pyright
uv run pytest
```

The project does not reach 100% coverage for testing as it would take too much time for the excercise.

## Rationale
Most of the design choices were researched shortly before the project with three things in mind
* Leverage and trust a type system
* Use modern tooling for package management
* Keep formatting opinionated

By achieving modularity with the types I then tried to separate the business logic from the rest of the aplication. I had recently read about Hexagonal Architecture being a concrete and simpler application of Clean Architecture so I decided to implement it.

The project is separated into three different sections:
* Two adapters (api, and repository)
* One core (The business logic)
* Two port definitions for interacting with the database, using Protocols for composition
* Two actors (FastApi, and a fake in-memory database)

"service" from the core package uses a port for the repository, and also exposes a port for the api to use. None of the adapters directly use each other, making every part swappable as long as it implements the ports fully.

The core itself contains models that the ports use. Since it's paramount that the typing is respected, I used pydantic to ensure that the data flowing is correct, approximating how static typing works in other languages.
