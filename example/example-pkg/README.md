# Packaged applications

Many use-cases require a package. For example, if you are creating a command-line interface that will be published to PyPI or if you want to define tests in a dedicated directory.

The --package flag can be used to create a packaged application:

```bash
uv init --package example-pkg
```

## Run

```bash
cd example-pkg
uv run example-pkg
```
