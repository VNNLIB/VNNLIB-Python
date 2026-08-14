"""Tests for the public ``vnnlib.query`` namespace."""

import vnnlib
import vnnlib.query as query

PARSING_EXPORTS = (
    "parse_query_file",
    "parse_query_string",
)

QUERY_EXPORTS = (
    "Query",
    "Network",
    "Assertion",
    "InputDefinition",
    "OutputDefinition",
    "HiddenDefinition",
    "Version",
)

ARITHMETIC_EXPORTS = (
    "ArithExpr",
    "Var",
    "Literal",
    "Float",
    "Int",
    "Negate",
    "Plus",
    "Minus",
    "Multiply",
)

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

EXCEPTION_EXPORTS = (
    "VNNLibException",
)

class TestParsingNamespace:

    def test_parsing_group_is_reachable(self):
        """Every parsing function is available from ``vnnlib.query``."""
        for name in PARSING_EXPORTS:
            assert hasattr(query, name), f"vnnlib.query.{name} is missing"

    def test_parsing_group_is_identical_to_root(self):
        """The query namespace re-exports the same objects as the package root."""
        for name in PARSING_EXPORTS:
            assert getattr(query, name) is getattr(vnnlib, name), (
                f"vnnlib.query.{name} is not identical to vnnlib.{name}"
            )

    def test_parse_query_file_from_query_namespace(self, tmp_path):
        """A query file can be parsed through the query namespace."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X Real [1])
            (declare-output Y Real [1])
        )
        (assert (<= X[0] 10.0))
        """

        query_path = tmp_path / "test.vnnlib"
        query_path.write_text(content, encoding="utf-8")

        parsed_query = query.parse_query_file(str(query_path))

        assert isinstance(parsed_query, query.Query)

class TestQueryStructureNamespace:

    def test_query_group_is_reachable(self):
        """Every query type is available from ``vnnlib.query``."""
        for name in QUERY_EXPORTS:
            assert hasattr(query, name), f"vnnlib.query.{name} is missing"

    def test_query_group_is_identical_to_root(self):
        """The query namespace re-exports the same objects as the package root."""
        for name in QUERY_EXPORTS:
            assert getattr(query, name) is getattr(vnnlib, name), (
                f"vnnlib.query.{name} is not identical to vnnlib.{name}"
            )

    def test_parser_returns_query_structure_types(self):
        """The parser returns query structure types from the query namespace."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X Real [2])
            (declare-output Y Real [1])
        )
        (assert (and (<= X[0] 10.0) (>= X[1] 5.0)))
        """

        parsed_query = query.parse_query_string(content)

        assert isinstance(parsed_query, query.Query)
        assert isinstance(parsed_query.networks[0], query.Network)
        assert isinstance(parsed_query.assertions[0], query.Assertion)

class TestArithmeticNamespace:

    def test_arithmetic_group_is_reachable(self):
        """Every arithmetic type is available from ``vnnlib.query``."""
        for name in ARITHMETIC_EXPORTS:
            assert hasattr(query, name), f"vnnlib.query.{name} is missing"

    def test_arithmetic_group_is_identical_to_root(self):
        """The query namespace re-exports the same objects as the package root."""
        for name in ARITHMETIC_EXPORTS:
            assert getattr(query, name) is getattr(vnnlib, name), (
                f"vnnlib.query.{name} is not identical to vnnlib.{name}"
            )

    def test_parser_returns_arithmetic_types(self):
        """The parser returns arithmetic types from the query namespace."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X Real [2])
            (declare-output Y Real [1])
        )
        (assert (and (<= X[0] 10.0) (>= X[1] 5.0)))
        """

        parsed_query = query.parse_query_string(content)
        expression = parsed_query.assertions[0].expr

        assert isinstance(expression, query.And)

        assert isinstance(expression.args[0], query.LessEqual)
        assert isinstance(expression.args[0].lhs, query.ArithExpr)
        assert isinstance(expression.args[0].lhs, query.Var)
        assert isinstance(expression.args[0].rhs, query.ArithExpr)
        assert isinstance(expression.args[0].rhs, query.Float)

        assert isinstance(expression.args[1], query.GreaterEqual)
        assert isinstance(expression.args[1].lhs, query.ArithExpr)
        assert isinstance(expression.args[1].lhs, query.Var)
        assert isinstance(expression.args[1].rhs, query.ArithExpr)
        assert isinstance(expression.args[1].rhs, query.Float)

class TestBooleanNamespace:

    def test_boolean_group_is_reachable(self):
        """Every Boolean type is available from ``vnnlib.query``."""
        for name in BOOLEAN_EXPORTS:
            assert hasattr(query, name), f"vnnlib.query.{name} is missing"

    def test_boolean_group_is_identical_to_root(self):
        """The query namespace re-exports the same objects as the package root."""
        for name in BOOLEAN_EXPORTS:
            assert getattr(query, name) is getattr(vnnlib, name), (
                f"vnnlib.query.{name} is not identical to vnnlib.{name}"
            )

    def test_boolean_group_supports_dnf_conversion(self):
        """A parsed Boolean expression works through the query namespace types."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X Real [2])
            (declare-output Y Real [1])
        )
        (assert (and (<= X[0] 10.0) (>= X[1] 5.0)))
        """

        expression = query.parse_query_string(content).assertions[0].expr
        dnf = expression.to_dnf()

        assert isinstance(expression, query.And)
        assert len(dnf) == 1
        assert len(dnf[0]) == 2
        assert all(isinstance(literal, query.Comparison) for literal in dnf[0])

class TestLinearArithmeticNamespace:

    def test_linear_arithmetic_group_is_reachable(self):
        """Every linear-arithmetic type is available from ``vnnlib.query``."""
        for name in LINEAR_ARITHMETIC_EXPORTS:
            assert hasattr(query, name), f"vnnlib.query.{name} is missing"

    def test_linear_arithmetic_group_is_identical_to_root(self):
        """Linear-arithmetic exports are the same objects as the root exports."""
        for name in LINEAR_ARITHMETIC_EXPORTS:
            assert getattr(query, name) is getattr(vnnlib, name), (
                f"vnnlib.query.{name} is not identical to vnnlib.{name}"
            )

    def test_linear_arithmetic_group_supports_linearization(self):
        """Linearization produces the types exposed by the query namespace."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X float32 [1])
            (declare-output Y float32 [1])
        )
        (assert (<= (+ (* 2.0 X[0]) 3.0) 10.0))
        """

        expression = query.parse_query_string(content).assertions[0].expr
        linear_expression = expression.lhs.to_linear_expr()

        assert isinstance(linear_expression, query.LinearArithExpr)
        assert linear_expression.constant == 3.0
        assert len(linear_expression.terms) == 1
        assert isinstance(linear_expression.terms[0], query.Term)
        assert linear_expression.terms[0].coeff == 2.0
        assert linear_expression.terms[0].var_name == "X[0]"

class TestEnumNamespace:
    def test_enum_group_is_reachable(self):
        """Every enum type is available from ``vnnlib.query``."""
        for name in ENUM_EXPORTS:
            assert hasattr(query, name), f"vnnlib.query.{name} is missing"


    def test_enum_group_is_identical_to_root(self):
        """Enum exports are the same objects as the root exports."""
        for name in ENUM_EXPORTS:
            assert getattr(query, name) is getattr(vnnlib, name), (
                f"vnnlib.query.{name} is not identical to vnnlib.{name}"
            )

    def test_enum_group_matches_parsed_declaration_metadata(self):
        """Parsed declaration metadata uses the enums in the query namespace."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X float32 [1])
            (declare-output Y float32 [1])
        )
        (assert (<= X[0] 10.0))
        """

        parsed_query = query.parse_query_string(content)
        input_definition = parsed_query.networks[0].inputs[0]

        assert input_definition.dtype == query.DType.F32
        assert input_definition.kind == query.SymbolKind.Input

class TestExceptionNamespace:
    def test_exception_group_is_reachable(self):
        """Every exception type is available from ``vnnlib.query``."""
        for name in EXCEPTION_EXPORTS:
            assert hasattr(query, name), f"vnnlib.query.{name} is missing"

    def test_exception_group_is_identical_to_root(self):
        """Exception exports are the same objects as the root exports."""
        for name in EXCEPTION_EXPORTS:
            assert getattr(query, name) is getattr(vnnlib, name), (
                f"vnnlib.query.{name} is not identical to vnnlib.{name}"
            )
