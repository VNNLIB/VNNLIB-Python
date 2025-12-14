# Contributing to VNNLIB-Python

## Setting up the project

To setup the project to begin development:

1. Clone the repository with submodules:
   ```bash
   git clone --recurse-submodules https://github.com/VNNLIB/VNNLIB-Python.git
   cd VNNLIB-Python
   ```
   If you have already cloned the repository without submodules, initialize them:
   ```bash
   git submodule update --init --recursive
   ```

## Building and Testing

This project uses `scikit-build-core` to build the C++ extension.

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the package in editable mode along with test dependencies:
   ```bash
   pip install -e .
   pip install pytest
   ```

3. Run the tests:
   ```bash
   pytest
   ```

## Updating the C++ bindings

The C++ core library is located in the `cpp/` submodule.

1. **Update the submodule**:
   Navigate to the `cpp/` directory and pull the latest changes or checkout a specific commit/tag.
   ```bash
   cd cpp
   git pull origin main  # or checkout a specific tag
   cd ..
   ```

3. **Verify changes**:
   Rebuild the Python extension and run tests to ensure compatibility.
   ```bash
   pip install .
   pytest
   ```

## Making a release

1. Update the version number in `pyproject.toml`.

2. Update `README.md` with a new entry to the compatibility table if applicable.

3. Update `CHANGELOG.md` with the new version and a list of changes.

4. Create a new Release on GitHub:
   - Tag the version (e.g., `v1.0.1`).
   - Provide a title and description.
   - Publish the release.

5. The **Build and Deploy Python Wheels** GitHub workflow will automatically trigger:
   - It builds Python wheels for Linux, Windows, and macOS.
   - It uploads these artifacts to PyPI (or TestPyPI if configured as a prelease).
