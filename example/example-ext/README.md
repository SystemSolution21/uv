# Projects with extension modules

Most Python projects are "pure Python", meaning they do not define modules in other languages like C, C++, FORTRAN, or Rust. However, projects with extension modules are often used for performance sensitive code.

Creating a project with an extension module requires choosing an alternative build system. uv supports creating projects with the following build systems that support building extension modules:

maturin for projects with Rust
scikit-build-core for projects with C, C++, FORTRAN, Cython
Specify the build system with the --build-backend flag:

```bash
uv init --build-backend maturin example-ext
```

## Run

```bash
cd example-ext
uv run example-ext
```
