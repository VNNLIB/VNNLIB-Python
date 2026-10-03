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
        assert query.multiple_networks_theory(parsed_query) == "SNET"
        assert query.multiple_node_comparisons_theory(parsed_query) == "SNC"

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
        assert query.multiple_networks_theory(parsed_query) == "SNET"
        assert query.multiple_node_comparisons_theory(parsed_query) == "SNC"

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
        assert query.multiple_networks_theory(parsed_query) == "SNET"
        assert query.multiple_node_comparisons_theory(parsed_query) == "SNC"

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
        assert query.multiple_networks_theory(parsed_query) == "SNET"
        assert query.multiple_node_comparisons_theory(parsed_query) == "SNC"

    def test_snet_network(self):
        content = """
        (vnnlib-version <2.0>)
        (declare-network f
            (declare-input X float32 [1])
            (declare-output Y float32 [1])
        )
        (assert (<= X[0] 1.0))
        """

        parsed_query = query.parse_query_string(content)

        assert query.hidden_node_theory(parsed_query) == "NH"
        assert query.input_output_theory(parsed_query) == "SIO"
        assert query.multiple_networks_theory(parsed_query) == "SNET"
        assert query.multiple_node_comparisons_theory(parsed_query) == "SNC"

    def test_mnet_networks(self):
        content = """
        (vnnlib-version <2.0>)
        (declare-network f
            (declare-input X float32 [1])
            (declare-output Y float32 [1])
        )
        (declare-network g
            (declare-input U float32 [1])
            (declare-output W float32 [1])
        )
        (assert (<= X[0] 1.0))
        """

        parsed_query = query.parse_query_string(content)

        assert query.hidden_node_theory(parsed_query) == "NH"
        assert query.input_output_theory(parsed_query) == "SIO"
        assert query.multiple_networks_theory(parsed_query) == "MNET"
        assert query.multiple_node_comparisons_theory(parsed_query) == "SNC"

    def test_minet_networks(self):
        content = """
        (vnnlib-version <2.0>)
        (declare-network f
            (declare-input A float32 [1,10])
            (declare-output B float32 [1,2])
        )
        (declare-network g
            (isomorphic-to f)
            (declare-input C float32 [1,10])
            (declare-output D float32 [1,2])
        )
        (assert (<= A[0, 0] 1.0))
        """

        parsed_query = query.parse_query_string(content)

        assert query.hidden_node_theory(parsed_query) == "NH"
        assert query.input_output_theory(parsed_query) == "SIO"
        assert query.multiple_networks_theory(parsed_query) == "MINET"
        assert query.multiple_node_comparisons_theory(parsed_query) == "SNC"

    def test_menet_networks(self):
        content = """
        (vnnlib-version <2.0>)
        (declare-network f
            (declare-input A float32 [1,10])
            (declare-output B float32 [1,2])
        )
        (declare-network f_copy
            (equal-to f)
            (declare-input C float32 [1,10])
            (declare-output D float32 [1,2])
        )
        (assert (<= A[0, 0] 1.0))
        """

        parsed_query = query.parse_query_string(content)

        assert query.hidden_node_theory(parsed_query) == "NH"
        assert query.input_output_theory(parsed_query) == "SIO"
        assert query.multiple_networks_theory(parsed_query) == "MENET"
        assert query.multiple_node_comparisons_theory(parsed_query) == "SNC"

    def test_single_node_comparison(self):
        content = """
        (vnnlib-version <2.0>)
        (declare-network f
            (declare-input X float32 [2])
            (declare-output Y float32 [1])
        )
        (declare-network g
            (declare-input A float32 [2])
            (declare-hidden H float32 [1] "hidden")
            (declare-output B float32 [1])
        )
        (assert (<= (+ X[0] X[1]) 0.1))
        (assert (<= Y[0] 0.1))
        (assert (<= H[0] 0.5))
        (assert (== Y[0] A[0]))
        """

        parsed_query = query.parse_query_string(content)

        assert query.hidden_node_theory(parsed_query) == "H"
        assert query.input_output_theory(parsed_query) == "SIO"
        assert query.multiple_networks_theory(parsed_query) == "MNET"
        assert query.multiple_node_comparisons_theory(parsed_query) == "SNC"

    def test_multiple_node_comparisons(self):
        content = """
        (vnnlib-version <2.0>)
        (declare-network f
            (declare-input X float32 [2])
            (declare-output Y float32 [1])
        )
        (declare-network g
            (declare-input A float32 [2])
            (declare-hidden H float32 [1] "hidden")
            (declare-output B float32 [1])
        )
        (assert (<= (+ X[0] Y[0]) 0.1))
        (assert (<= H[0] A[1]))
        (assert (== B[0] H[0]))
        """

        parsed_query = query.parse_query_string(content)

        assert query.hidden_node_theory(parsed_query) == "H"
        assert query.input_output_theory(parsed_query) == "SIO"
        assert query.multiple_networks_theory(parsed_query) == "MNET"
        assert query.multiple_node_comparisons_theory(parsed_query) == "MNC"

    def test_theory_functions_are_core_bindings(self):
        """The query namespace re-exports the same functions as the core module."""
        assert query.hidden_node_theory is _core.hidden_node_theory
        assert query.input_output_theory is _core.input_output_theory
        assert query.multiple_networks_theory is _core.multiple_networks_theory
        assert query.multiple_node_comparisons_theory is _core.multiple_node_comparisons_theory

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
        assert query.multiple_networks_theory(parsed_query) == "SNET"
        assert query.multiple_node_comparisons_theory(parsed_query) == "SNC"
