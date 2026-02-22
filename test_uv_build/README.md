# Test Distributable Library

## Workflow

- Moved the dist/ created using `uv build` at example-lib/ to test_uv_build/

- Run `uv pip install dist/example_lib-0.1.0-py3-none-any.whl`

- Run `python -c "import example_lib; print(example_lib.hello())"`

- Output: Hello from Python library example-lib!
