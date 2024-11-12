# Beer Run
A Python exercise to learn modern Python, tooling and architecture

## Starting the project
Make sure `uv` is installed, then run:
```
uv sync
```
Then to start FastApi
```
uv run fastapi dev
```
## Run tests and pyright (optional)
Normally these would run as GitHub Actions against incoming pull requests.
```
uv run pyright
uv run pytest
```

