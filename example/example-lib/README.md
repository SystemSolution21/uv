# Libraries

A library provides functions and objects for other projects to consume. Libraries are intended to be built and distributed, e.g., by uploading them to PyPI.

Libraries can be created by using the --lib flag:

```bash
uv init --lib example-lib
```

## Run

```bash
cd example-lib
uv run python -c "import example_lib; print(example_lib.hello())"
```
