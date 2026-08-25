"""
VNNLib Python Bindings

Modern Python bindings for the VNNLib verification language parser.
Built with pybind11 for direct access to the BNFC-generated C++ AST.

Basic Usage:
    import vnnlib
    
    # Parse a VNNLIB file
    query = vnnlib.parse_query_file("path/to/file.vnnlib")
    
    # Access networks and constraints
    for network in query.networks:
        print(f"Network: {network.name}")
        
    # Use compatibility module for reachability format
    import vnnlib.compat
    cases = vnnlib.compat.transform(query)
"""
import warnings
from . import _core
from importlib.metadata import version


# Module metadata
try:
    __version__ = version(__name__)
except Exception:
    __version__ = "dev-version"

__author__ = "Allen Antony and Matthew Daggitt" 
__description__ = "Python bindings for VNN-Lib verification language"
__url__ = "https://github.com/VNNLIB/VNNLIB-Standard"

__all__ = [
    # Parsing functions
    "parse_query_file", "parse_query_string",
    
    # Core AST nodes
    "Query", "Network", "Assertion", 
    "InputDefinition", "OutputDefinition", "HiddenDefinition",
    "Version",
    
    # Expression types  
    "ArithExpr", "BoolExpr",
    "Var", "Literal", "Float", "Int", "Negate", "Plus", "Minus", "Multiply",
    "Comparison", "GreaterThan", "GreaterEqual", "LessThan", "LessEqual", "Equal", "NotEqual",
    "Connective", "And", "Or",
    
    # Linear arithmetic
    "LinearArithExpr", "Term",
    
    # Enums and data types
    "DType", "SymbolKind",
    
    # Exceptions
    "VNNLibException",
]


def __getattr__(name):
    if name in __all__:
        warnings.warn(
            f"vnnlib.{name} is deprecated; use vnnlib.query.{name} instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(_core, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
