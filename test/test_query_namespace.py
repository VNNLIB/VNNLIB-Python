"""Tests for the public ``vnnlib.query`` namespace."""

import os
from pathlib import Path
import subprocess
import sys
import warnings

import pytest
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

PUBLIC_EXPORTS = (
    PARSING_EXPORTS + QUERY_EXPORTS + ARITHMETIC_EXPORTS + BOOLEAN_EXPORTS
    + LINEAR_ARITHMETIC_EXPORTS + ENUM_EXPORTS + EXCEPTION_EXPORTS
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
            (declare-input X real [1])
            (declare-output Y real [1])
        )
        (assert (<= X[0] 10.0))
        """

        query_path = tmp_path / "test.vnnlib"
        query_path.write_text(content, encoding="utf-8")

        parsed_query = query.parse_query_file(str(query_path))

        assert isinstance(parsed_query, query.Query)

    def test_parser_maps_standard_real_type(self):
        """The parser maps the standard lowercase ``real`` type correctly."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X real [1])
            (declare-output Y real [1])
        )
        (assert (<= X[0] 10.0))
        """

        parsed_query = query.parse_query_string(content)

        assert parsed_query.networks[0].inputs[0].dtype == query.DType.Real
        assert parsed_query.networks[0].outputs[0].dtype == query.DType.Real

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
            (declare-input X real [2])
            (declare-output Y real [1])
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
            (declare-input X real [2])
            (declare-output Y real [1])
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
            (declare-input X real [2])
            (declare-output Y real [1])
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


class TestRootCompatibility:

    def test_legacy_root_paths_match_query_namespace(self):
        """Deprecated root exports remain identical to their replacements."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert vnnlib.Or is vnnlib.query.Or
            assert vnnlib.parse_query_file is vnnlib.query.parse_query_file
            assert vnnlib.DType is vnnlib.query.DType

    def test_legacy_root_path_warns_with_replacement(self):
        """Every deprecated root export emits one warning naming its replacement."""
        for name in PUBLIC_EXPORTS:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                legacy = getattr(vnnlib, name)

            assert legacy is getattr(query, name)
            assert len(caught) == 1, f"vnnlib.{name} must emit exactly one warning"
            assert caught[0].category is DeprecationWarning
            assert str(caught[0].message) == (
                f"vnnlib.{name} is deprecated; use vnnlib.query.{name} instead"
            )

    def test_query_paths_do_not_warn(self):
        """Every new-path export resolves without warnings."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            for name in PUBLIC_EXPORTS:
                assert getattr(vnnlib.query, name) is getattr(vnnlib._core, name)
        assert caught == []

    def test_invalid_root_name_raises_attribute_error(self):
        """Names outside the legacy public API remain unavailable."""
        with pytest.raises(AttributeError):
            getattr(vnnlib, "NotAnExport")


class TestNamespaceConsistency:

    def test_syntax_file_matches_query_namespace(self):
        """Legacy and query namespace paths parse the same syntax test file."""
        path = (
            Path(__file__).resolve().parents[1]
            / "cpp/grammar/syntax/test/single_network.vnnlib"
        )

        with warnings.catch_warnings(record=True) as legacy_warnings:
            warnings.simplefilter("always")
            legacy_query = vnnlib.parse_query_file(str(path))

        with warnings.catch_warnings(record=True) as new_warnings:
            warnings.simplefilter("always")
            new_query = query.parse_query_file(str(path))

        assert isinstance(legacy_query, query.Query)
        assert isinstance(new_query, query.Query)
        assert str(legacy_query) == str(new_query)
        legacy_assertions = [str(assertion) for assertion in legacy_query.assertions]
        new_assertions = [str(assertion) for assertion in new_query.assertions]
        assert legacy_assertions
        assert legacy_assertions == new_assertions
        assert len(legacy_warnings) == 1
        assert legacy_warnings[0].category is DeprecationWarning
        assert str(legacy_warnings[0].message) == (
            "vnnlib.parse_query_file is deprecated; "
            "use vnnlib.query.parse_query_file instead"
        )
        assert new_warnings == []


class TestNamespaceTyping:

    def test_query_namespace_preserves_public_types(self, tmp_path):
        """Mypy recognises all exports and rejects an incorrect parser result type."""
        package = Path(vnnlib.__file__).resolve().parent
        assert (package / "py.typed").is_file()
        assert (package / "__init__.pyi").is_file()
        assert (package / "query/__init__.pyi").is_file()
        assert len(PUBLIC_EXPORTS) == len(set(PUBLIC_EXPORTS)) == 34

        lines = ["from typing import Callable, Type", "import vnnlib as old", "import vnnlib.query as new"]
        for name in PUBLIC_EXPORTS:
            if name in PARSING_EXPORTS:
                lines.append(f"old_{name}: Callable[[str], new.Query] = old.{name}")
                lines.append(f"new_{name}: Callable[[str], new.Query] = new.{name}")
            else:
                lines.append(f"new_{name}: Type[old.{name}] = new.{name}")
                lines.append(f"old_{name}: Type[new.{name}] = old.{name}")
        lines.extend([
            "old_result: new.Query = old.parse_query_string('')",
            "new_result: new.Query = new.parse_query_string('')",
        ])
        probe = tmp_path / "namespace_typing.py"
        probe.write_text("\n".join(lines) + "\n", encoding="utf-8")
        env = os.environ.copy()
        env["MYPYPATH"] = str(package.parent)
        command = [sys.executable, "-m", "mypy", "--strict", "--no-incremental",
                   "--cache-dir", str(tmp_path / "mypy-cache"), str(probe)]
        positive = subprocess.run(command, cwd=tmp_path, env=env, capture_output=True, text=True)
        assert positive.returncode == 0, positive.stdout + positive.stderr

        lines.extend([
            "bad_old: int = old.parse_query_string('')",
            "bad_new: int = new.parse_query_string('')",
        ])
        probe.write_text("\n".join(lines) + "\n", encoding="utf-8")
        negative = subprocess.run(command, cwd=tmp_path, env=env, capture_output=True, text=True)
        assert negative.returncode == 1, negative.stdout + negative.stderr
        assert negative.stdout.count("Incompatible types in assignment") == 2, negative.stdout
