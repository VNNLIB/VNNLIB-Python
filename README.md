# VNN-LIB Python

A Python package for parsing and manipulating neural network properties in the updated [VNN-LIB format](https://www.vnnlib.org/). 

## Features

Features include:
- Parsing: Convert VNN-LIB file or string into a type-checked AST
- AST traversal: Access, traverse, and convert the AST back to a string.
- Transformers:
    - Linearise arithmetic expressions
    - Convert boolean expressions to Disjunctive Normal Form (DNF)
    - Transform spec to reachability format used in prior VNN-COMPs.

## Installation

Install the latest stable version via PyPi:
```bash
pip install vnnlib
```

## Basic Usage

```python
import vnnlib

# Parse a VNN-LIB specification
query = vnnlib.parse_query_file("path/to/spec.vnnlib")

for assertion in query.assertions:
    print(assertion)
```

## Version compatibility

| VNNLIB-Python version | VNNLIB version |
| --- | --- |
| v1.0.* | v2.0 |
| v0.0.1 | v1.0 |
