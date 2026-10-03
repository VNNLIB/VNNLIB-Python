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
        assert query.arithmetic_complexity_theory(parsed_query) == "BND"
        assert query.element_type_theories(parsed_query) == ["Real"]

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
        assert query.arithmetic_complexity_theory(parsed_query) == "BND"
        assert query.element_type_theories(parsed_query) == ["Real"]

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
        assert query.arithmetic_complexity_theory(parsed_query) == "BND"
        assert query.element_type_theories(parsed_query) == ["Real"]

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
        assert query.arithmetic_complexity_theory(parsed_query) == "BND"
        assert query.element_type_theories(parsed_query) == ["Real"]

    def test_snet_network(self):
        """A query with a single network declaration belong to SNET."""
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
        assert query.arithmetic_complexity_theory(parsed_query) == "BND"
        assert query.element_type_theories(parsed_query) == ["F32"]

    def test_mnet_networks(self):
        """A query with an arbitrary number of network declarations belong to MNET."""
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
        assert query.arithmetic_complexity_theory(parsed_query) == "BND"
        assert query.element_type_theories(parsed_query) == ["F32"]

    def test_minet_networks(self):
        """A query with multiple network declarations where all but one contains either an isomorphic-to or equal-to declaration belong to MINET."""
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
        assert query.arithmetic_complexity_theory(parsed_query) == "BND"
        assert query.element_type_theories(parsed_query) == ["F32"]

    def test_menet_networks(self):
        """A query with multiple network declarations where all but one contain an equal-to declaration belong to MENET."""
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
        assert query.arithmetic_complexity_theory(parsed_query) == "BND"
        assert query.element_type_theories(parsed_query) == ["F32"]

    def test_single_node_comparison(self):
        """A query with comparisons that do not reference variables from different nodes of the same network belong to SNC."""
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
        assert query.arithmetic_complexity_theory(parsed_query) == "LIN"
        assert query.element_type_theories(parsed_query) == ["F32"]

    def test_multiple_node_comparisons(self):
        """A query with comparisons that reference variables from different nodes of the same network belong to MNC."""
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
        assert query.arithmetic_complexity_theory(parsed_query) == "LIN"
        assert query.element_type_theories(parsed_query) == ["F32"]

    def test_theory_functions_are_core_bindings(self):
        """The query namespace re-exports the same functions as the core module."""
        assert query.hidden_node_theory is _core.hidden_node_theory
        assert query.input_output_theory is _core.input_output_theory
        assert query.multiple_networks_theory is _core.multiple_networks_theory
        assert query.multiple_node_comparisons_theory is _core.multiple_node_comparisons_theory
        assert query.arithmetic_complexity_theory is _core.arithmetic_complexity_theory
        assert query.element_type_theories is _core.element_type_theories

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
        assert query.arithmetic_complexity_theory(parsed_query) == "BND"
        assert query.element_type_theories(parsed_query) == ["Real"]


class TestArithmeticComplexityTheory:
    """Section 4.1.5 examples: BND, OUTC, LIN and POLY."""

    NETWORK = """
    (vnnlib-version <2.0>)
    (declare-network test
        (declare-input X real [2])
        (declare-output Y real [2])
    )
    """

    def classify(self, assertions):
        parsed_query = query.parse_query_string(self.NETWORK + assertions)
        return query.arithmetic_complexity_theory(parsed_query)

    def test_bounds_only(self):
        """Single variables against constants is BND."""
        assert self.classify("(assert (<= X[0] 1.0)) (assert (>= Y[0] 0.5))") == "BND"

    def test_output_comparison(self):
        """Two output variables compared directly is OUTC."""
        assert self.classify("(assert (<= X[0] 1.0)) (assert (>= Y[0] Y[1]))") == "OUTC"

    def test_linear_expression(self):
        """A linear expression over inputs is LIN."""
        assert self.classify(
            "(assert (<= (+ (* 0.5 X[0]) (* 0.75 X[1])) 1.0)) (assert (>= (+ Y[0] Y[1]) 0.5))"
        ) == "LIN"

    def test_polynomial_expression(self):
        """A product of two variables is POLY."""
        assert self.classify(
            "(assert (<= (* X[0] X[1]) 1.0)) (assert (>= (+ Y[0] Y[1]) 0.5))"
        ) == "POLY"

    def test_highest_level_wins(self):
        """One polynomial assertion makes the whole query POLY."""
        assert self.classify("(assert (<= X[0] 1.0)) (assert (<= (* X[0] X[1]) 1.0))") == "POLY"


class TestElementTypeTheories:
    """Section 4.1.6: one theory per declared element type."""

    def test_single_element_type(self):
        content = """
        (vnnlib-version <2.0>)
        (declare-network test
            (declare-input X real [2])
            (declare-output Y real [1])
        )
        (assert (<= X[0] 1.0))
        """
        parsed_query = query.parse_query_string(content)
        assert query.element_type_theories(parsed_query) == ["Real"]

    def test_mixed_element_types(self):
        """A query can belong to more than one element type theory."""
        content = """
        (vnnlib-version <2.0>)
        (declare-network a
            (declare-input X float16 [2])
            (declare-output Y float32 [1])
        )
        (assert (<= X[0] 1.0))
        """
        parsed_query = query.parse_query_string(content)
        assert query.element_type_theories(parsed_query) == ["F16", "F32"]
