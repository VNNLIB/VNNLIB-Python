"""Tests for the public ``vnnlib.query`` namespace."""

import vnnlib
import vnnlib.query as query


BOOLEAN_EXPORTS = (
    "BoolExpr",
    "Comparison",
    "GreaterThan",
    "GreaterEqual",
    "LessThan",
    "LessEqual",
    "Equal",
    "NotEqual",
    "Connective",
    "And",
    "Or",
)

LINEAR_ARITHMETIC_EXPORTS = (
    "LinearArithExpr",
    "Term",
)

ENUM_EXPORTS = (
    "DType",
    "SymbolKind",
)


def test_boolean_group_is_reachable():
    """Every Boolean type is available from ``vnnlib.query``."""
    for name in BOOLEAN_EXPORTS:
        assert hasattr(query, name), f"vnnlib.query.{name} is missing"


def test_boolean_group_is_identical_to_root():
    """The query namespace re-exports the same objects as the package root."""
    for name in BOOLEAN_EXPORTS:
        assert getattr(query, name) is getattr(vnnlib, name), (
            f"vnnlib.query.{name} is not identical to vnnlib.{name}"
        )


def test_boolean_group_supports_dnf_conversion():
    """A parsed Boolean expression works through the query namespace types."""
    content = """
    (vnnlib-version <2.0>)
    (declare-network test
        (declare-input X Real [2])
        (declare-output Y Real [1])
    )
    (assert (and (<= X[0] 10.0) (>= X[1] 5.0)))
    """

    expression = vnnlib.parse_query_string(content).assertions[0].expr
    dnf = expression.to_dnf()

    assert isinstance(expression, query.And)
    assert len(dnf) == 1
    assert len(dnf[0]) == 2
    assert all(isinstance(literal, query.Comparison) for literal in dnf[0])


def test_linear_arithmetic_group_is_reachable():
    """Every linear-arithmetic type is available from ``vnnlib.query``."""
    for name in LINEAR_ARITHMETIC_EXPORTS:
        assert hasattr(query, name), f"vnnlib.query.{name} is missing"


def test_linear_arithmetic_group_is_identical_to_root():
    """Linear-arithmetic exports are the same objects as the root exports."""
    for name in LINEAR_ARITHMETIC_EXPORTS:
        assert getattr(query, name) is getattr(vnnlib, name), (
            f"vnnlib.query.{name} is not identical to vnnlib.{name}"
        )


def test_linear_arithmetic_group_supports_linearization():
    """Linearization produces the types exposed by the query namespace."""
    content = """
    (vnnlib-version <2.0>)
    (declare-network test
        (declare-input X float32 [1])
        (declare-output Y float32 [1])
    )
    (assert (<= (+ (* 2.0 X[0]) 3.0) 10.0))
    """

    expression = vnnlib.parse_query_string(content).assertions[0].expr
    linear_expression = expression.lhs.to_linear_expr()

    assert isinstance(linear_expression, query.LinearArithExpr)
    assert linear_expression.constant == 3.0
    assert len(linear_expression.terms) == 1
    assert isinstance(linear_expression.terms[0], query.Term)
    assert linear_expression.terms[0].coeff == 2.0
    assert linear_expression.terms[0].var_name == "X[0]"


def test_enum_group_is_reachable():
    """Every enum type is available from ``vnnlib.query``."""
    for name in ENUM_EXPORTS:
        assert hasattr(query, name), f"vnnlib.query.{name} is missing"


def test_enum_group_is_identical_to_root():
    """Enum exports are the same objects as the root exports."""
    for name in ENUM_EXPORTS:
        assert getattr(query, name) is getattr(vnnlib, name), (
            f"vnnlib.query.{name} is not identical to vnnlib.{name}"
        )


def test_enum_group_matches_parsed_declaration_metadata():
    """Parsed declaration metadata uses the enums in the query namespace."""
    content = """
    (vnnlib-version <2.0>)
    (declare-network test
        (declare-input X float32 [1])
        (declare-output Y float32 [1])
    )
    (assert (<= X[0] 10.0))
    """

    parsed_query = vnnlib.parse_query_string(content)
    input_definition = parsed_query.networks[0].inputs[0]

    assert input_definition.dtype == query.DType.F32
    assert input_definition.kind == query.SymbolKind.Input
