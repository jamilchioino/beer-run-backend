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

