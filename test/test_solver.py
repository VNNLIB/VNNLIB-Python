import vnnlib
import os
import pytest
from vnnlib.solver import Capability, Solver, VerificationResult


def get_test_solver():
    executable = os.environ.get("VNNLIB_TEST_SOLVER")
    if not executable:
        pytest.skip("VNNLIB_TEST_SOLVER is not set")
    return executable


@pytest.mark.parametrize(
    "result, expected",
    [
        ("sat", VerificationResult.Sat),
        ("unsat", VerificationResult.Unsat),
        ("unknown", VerificationResult.Unknown),
        ("timed-out", VerificationResult.TimedOut),
    ],
)
def test_verify_results(tmp_path, monkeypatch, result, expected):
    query = tmp_path / "query.vnnlib"
    query.write_text(
        """
(vnnlib-version <2.0>)
(declare-network f
    (declare-input X float32 [1])
    (declare-output Y float32 [1])
)
(assert (<= X[0] 1.0))
"""
    )

    config = tmp_path / "solver.toml"
    config.write_text(
        f"""
[solver]
name = "Test Solver"
version = "0.1.0"

[[rules]]
match = "*"
result = "{result}"
"""
    )

    monkeypatch.setenv("VNNLIB_TEST_SOLVER_CONFIG", str(config))

    solver = Solver(get_test_solver())

    assert solver.verify(str(query), {}) == expected


def test_verify_allows_stderr(tmp_path, monkeypatch):
    query = tmp_path / "query.vnnlib"
    query.write_text(
        """
(vnnlib-version <2.0>)
(declare-network f
    (declare-input X float32 [1])
    (declare-output Y float32 [1])
)
(assert (<= X[0] 1.0))
"""
    )

    config = tmp_path / "solver.toml"
    config.write_text(
        """
[solver]
name = "Test Solver"
version = "0.1.0"

[[rules]]
match = "*"
result = "sat"
stderr = "solver warning"
"""
    )

    monkeypatch.setenv("VNNLIB_TEST_SOLVER_CONFIG", str(config))

    solver = Solver(get_test_solver())

    assert solver.verify(str(query), {}) == VerificationResult.Sat


def test_verify_allows_nonzero_exit(tmp_path, monkeypatch):
    query = tmp_path / "query.vnnlib"
    query.write_text(
        """
(vnnlib-version <2.0>)
(declare-network f
    (declare-input X float32 [1])
    (declare-output Y float32 [1])
)
(assert (<= X[0] 1.0))
"""
    )

    config = tmp_path / "solver.toml"
    config.write_text(
        """
[solver]
name = "Test Solver"
version = "0.1.0"

[[rules]]
match = "*"
result = "sat"
exit_code = 7
"""
    )

    monkeypatch.setenv("VNNLIB_TEST_SOLVER_CONFIG", str(config))

    solver = Solver(get_test_solver())

    assert solver.verify(str(query), {}) == VerificationResult.Sat


def test_verify_rejects_malformed_output(tmp_path, monkeypatch):
    query = tmp_path / "query.vnnlib"
    query.write_text(
        """
(vnnlib-version <2.0>)
(declare-network f
    (declare-input X float32 [1])
    (declare-output Y float32 [1])
)
(assert (<= X[0] 1.0))
"""
    )

    config = tmp_path / "solver.toml"
    config.write_text(
        """
[solver]
name = "Test Solver"
version = "0.1.0"

[[rules]]
match = "*"
result = "sat"
raw_stdout = "invalid"
"""
    )

    monkeypatch.setenv("VNNLIB_TEST_SOLVER_CONFIG", str(config))

    solver = Solver(get_test_solver())

    with pytest.raises(vnnlib.VNNLibException):
        solver.verify(str(query), {})


def test_verify_rejects_abnormal_termination(tmp_path, monkeypatch):
    query = tmp_path / "query.vnnlib"
    query.write_text(
        """
(vnnlib-version <2.0>)
(declare-network f
    (declare-input X float32 [1])
    (declare-output Y float32 [1])
)
(assert (<= X[0] 1.0))
"""
    )

    config = tmp_path / "solver.toml"
    config.write_text(
        """
[solver]
name = "Test Solver"
version = "0.1.0"

[[rules]]
match = "*"
result = "sat"
crash = true
"""
    )

    monkeypatch.setenv("VNNLIB_TEST_SOLVER_CONFIG", str(config))

    solver = Solver(get_test_solver())

    with pytest.raises(vnnlib.VNNLibException):
        solver.verify(str(query), {})


def test_verify_rejects_missing_executable():
    solver = Solver("definitely-not-a-real-vnnlib-solver")

    with pytest.raises(vnnlib.VNNLibException):
        solver.verify("query.vnnlib", {})


def test_verify_forwards_timeout(tmp_path, monkeypatch):
    query = tmp_path / "query.vnnlib"
    query.write_text(
        """
(vnnlib-version <2.0>)
(declare-network f
    (declare-input X float32 [1])
    (declare-output Y float32 [1])
)
(assert (<= X[0] 1.0))
"""
    )

    config = tmp_path / "solver.toml"
    config.write_text(
        """
[solver]
name = "Test Solver"
version = "0.1.0"

[[rules]]
match = "*"
result = "sat"
delay_seconds = 2
"""
    )

    monkeypatch.setenv("VNNLIB_TEST_SOLVER_CONFIG", str(config))

    solver = Solver(get_test_solver())

    assert solver.verify(str(query), {}, 1) == VerificationResult.TimedOut


def test_verify_forwards_networks(tmp_path, monkeypatch):
    query = tmp_path / "query.vnnlib"
    query.write_text(
        """
(vnnlib-version <2.0>)
(declare-network f
    (declare-input X float32 [1])
    (declare-output Y float32 [1])
)
(assert (<= X[0] 1.0))
"""
    )

    model = tmp_path / "model.onnx"
    model.write_text("")

    config = tmp_path / "solver.toml"
    config.write_text(
        """
[solver]
name = "Test Solver"
version = "0.1.0"

[[rules]]
match = "*"
result = "sat"

[rules.model_element_types]
X = "float32"
"""
    )

    monkeypatch.setenv("VNNLIB_TEST_SOLVER_CONFIG", str(config))

    solver = Solver(get_test_solver())

    assert solver.verify(
        str(query),
        {"f": str(model)},
    ) == VerificationResult.Sat


def test_verify_ignores_assignment_output(tmp_path, monkeypatch):
    query = tmp_path / "query.vnnlib"
    query.write_text(
        """
(vnnlib-version <2.0>)
(declare-network f
    (declare-input X float32 [1])
    (declare-output Y float32 [1])
)
(assert (<= X[0] 1.0))
"""
    )

    model = tmp_path / "model.onnx"
    model.write_text("")

    config = tmp_path / "solver.toml"
    config.write_text(
        """
[solver]
name = "Test Solver"
version = "0.1.0"

[[rules]]
match = "*"
result = "sat"

[rules.assignments]
X = [0.5]
Y = [0.0]
"""
    )

    monkeypatch.setenv("VNNLIB_TEST_SOLVER_CONFIG", str(config))

    solver = Solver(get_test_solver())

    assert solver.verify(
        str(query),
        {"f": str(model)},
    ) == VerificationResult.Sat


SUPPORTS_CONFIG = """
[solver]
name = "Test Solver"
version = "0.1.0"

[capabilities]
onnx-opset-versions = ["13", "21"]
onnx-element-types = ["real", "float32", "float64", "int32"]
vnnlib-versions = ["2.0", "2.0"]
hidden-node-theories = ["NH"]
multiple-input-output-theories = ["SIO"]
multiple-network-theories = ["SNET"]
multiple-node-comparison-theories = ["SNC"]
arithmetic-complexity-theories = ["BND", "LIN"]
optimised-disjunctive-reasoning = false
serialise-assignments = false

[[capabilities.onnx-operators]]
name = "Gemm"
element-types = ["float32", "float64"]

[[capabilities.onnx-operators]]
name = "Relu"

[soundness]
sound-for = ["real", "float32", "float64", "int32"]
"""


def get_supports_solver(tmp_path, monkeypatch, injection=""):
    config = tmp_path / "supports.toml"
    config.write_text(SUPPORTS_CONFIG + injection)

    monkeypatch.setenv("VNNLIB_TEST_SOLVER_CONFIG", str(config))

    return Solver(get_test_solver())


@pytest.mark.parametrize(
    "capability, minimum, maximum",
    [
        (Capability.OnnxOpsetVersions, "13", "21"),
        (Capability.VNNLibVersions, "2.0", "2.0"),
    ],
)
def test_supports_version_ranges(
    tmp_path,
    monkeypatch,
    capability,
    minimum,
    maximum,
):
    solver = get_supports_solver(tmp_path, monkeypatch)

    result = solver.supports(capability)

    assert result.minimum == minimum
    assert result.maximum == maximum


@pytest.mark.parametrize(
    "capability, expected",
    [
        (
            Capability.OnnxElementTypes,
            ["real", "float32", "float64", "int32"],
        ),
        (Capability.HiddenNodeTheories, ["NH"]),
        (Capability.MultipleInputOutputTheories, ["SIO"]),
        (Capability.MultipleNetworkTheories, ["SNET"]),
        (Capability.MultipleNodeComparisonTheories, ["SNC"]),
        (Capability.ArithmeticComplexityTheories, ["BND", "LIN"]),
    ],
)
def test_supports_lists(tmp_path, monkeypatch, capability, expected):
    solver = get_supports_solver(tmp_path, monkeypatch)

    assert solver.supports(capability) == expected


@pytest.mark.parametrize(
    "capability, expected",
    [
        (Capability.OptimisedDisjunctiveReasoning, False),
        (Capability.SerialiseAssignments, False),
    ],
)
def test_supports_booleans(tmp_path, monkeypatch, capability, expected):
    solver = get_supports_solver(tmp_path, monkeypatch)

    assert solver.supports(capability) == expected


def test_supports_rejects_missing_executable():
    solver = Solver("definitely-not-a-real-vnnlib-solver")

    with pytest.raises(vnnlib.VNNLibException):
        solver.supports(Capability.OnnxOpsetVersions)


def test_supports_operators(tmp_path, monkeypatch):
    solver = get_supports_solver(tmp_path, monkeypatch)

    operators = solver.supports(Capability.OnnxOperators)

    assert [operator.name for operator in operators] == ["Gemm", "Relu"]
    assert [operator.element_types for operator in operators] == [
        ["float32", "float64"],
        [],
    ]


def test_supports_allows_stderr(tmp_path, monkeypatch):
    solver = get_supports_solver(
        tmp_path,
        monkeypatch,
        """
[injection]
stderr = "solver warning"
""",
    )

    result = solver.supports(Capability.OnnxOpsetVersions)

    assert result.minimum == "13"
    assert result.maximum == "21"


def test_supports_allows_nonzero_exit(tmp_path, monkeypatch):
    solver = get_supports_solver(
        tmp_path,
        monkeypatch,
        """
[injection]
exit_code = 7
""",
    )

    result = solver.supports(Capability.OnnxOpsetVersions)

    assert result.minimum == "13"
    assert result.maximum == "21"


def test_supports_rejects_malformed_output(tmp_path, monkeypatch):
    solver = get_supports_solver(
        tmp_path,
        monkeypatch,
        """
[injection]
raw_stdout = "13"
""",
    )

    with pytest.raises(vnnlib.VNNLibException):
        solver.supports(Capability.OnnxOpsetVersions)


def test_supports_rejects_abnormal_termination(tmp_path, monkeypatch):
    solver = get_supports_solver(
        tmp_path,
        monkeypatch,
        """
[injection]
crash = true
""",
    )

    with pytest.raises(vnnlib.VNNLibException):
        solver.supports(Capability.OnnxOpsetVersions)
