# vnnlib

A python package for parsing and manipulating neural network properties in the updated [VNN-LIB format](https://github.com/VNNLIB/VNNLIB-Standard). The package contains a main parsing function for generating an
Abstract Syntax Tree (AST) from the VNN-LIB spec, as well as utilities for transforming the AST into formats more suitable for verification.

## Features
- VNN-LIB Semantic checking: Ensure well-formedness of specification
- VNN-LIB Parsing: Convert VNN-LIB file or string into an AST
- AST Utilities: Access, traverse, and convert the AST back to the specification.
- Transformers:
    - Linearise arithmetic expressions
    - Convert boolean expressions to DNF
    - Transform spec to reachability format used in prior VNN-COMPs

## Installation
Install the latest stable version via PyPi
```bash
pip install vnnlib
```

Or to install an editable/development version
```bash
git clone --recurse-submodules https://github.com/VNNLIB/VNNLIB-Python.git
cd VNNLIB-Python
pip install -e .
```

## Basic Usage
```python
import vnnlib

# Parse a VNN-LIB specification
ast = vnnlib.parse_vnnlib("path/to/spec.vnnlib")

for assertion in ast.assertions:
    print(assertion)
```

## License
MIT License





