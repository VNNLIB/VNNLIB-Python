"""Tests for query classification under VNN-LIB 2.0 sections 4.1.1 and 4.1.2."""

import vnnlib.query as query
from vnnlib import _core


class TestQueryTheories:

    def test_single_input_output_without_hidden_nodes(self):
        """A tensor with multiple elements still has a single input declaration."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X real [2])
            (declare-output Y real [1])
        )
        (assert (<= X[0] 1.0))
        """

        parsed_query = query.parse_query_string(content)

        assert query.hidden_node_theory(parsed_query) == "NH"
        assert query.input_output_theory(parsed_query) == "SIO"

    def test_hidden_node_declaration(self):
        """A hidden declaration belongs to H even without an assertion reference."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X real [2])
            (declare-hidden H real [1] "hidden")
            (declare-output Y real [1])
        )
        (assert (<= X[0] 1.0))
        """

        parsed_query = query.parse_query_string(content)

        assert query.hidden_node_theory(parsed_query) == "H"
        assert query.input_output_theory(parsed_query) == "SIO"

    def test_multiple_input_declarations(self):
        """Multiple input declarations in one network belong to MIO."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X real [2])
            (declare-input Z real [1])
            (declare-output Y real [1])
        )
        (assert (<= X[0] 1.0))
        """

        parsed_query = query.parse_query_string(content)

        assert query.hidden_node_theory(parsed_query) == "NH"
        assert query.input_output_theory(parsed_query) == "MIO"

    def test_multiple_output_declarations(self):
        """Multiple output declarations in one network belong to MIO."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X real [2])
            (declare-output Z real [1])
            (declare-output Y real [1])
        )
        (assert (<= X[0] 1.0))
        """

        parsed_query = query.parse_query_string(content)

        assert query.hidden_node_theory(parsed_query) == "NH"
        assert query.input_output_theory(parsed_query) == "MIO"

    def test_theory_functions_are_core_bindings(self):
        """The query namespace re-exports the same functions as the core module."""
        assert query.hidden_node_theory is _core.hidden_node_theory
        assert query.input_output_theory is _core.input_output_theory

    def test_theory_functions_from_file(self, tmp_path):
        """A query parsed from a file supports both theory classification functions."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X real [1])
            (declare-input Z real [1])
            (declare-hidden H real [1] "hidden")
            (declare-output Y real [1])
        )
        (assert (<= X[0] 1.0))
        """

        query_path = tmp_path / "query.vnnlib"
        query_path.write_text(content, encoding="utf-8")

        parsed_query = query.parse_query_file(str(query_path))

        assert query.hidden_node_theory(parsed_query) == "H"
        assert query.input_output_theory(parsed_query) == "MIO"
