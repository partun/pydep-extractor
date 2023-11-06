# pydep_extractor


### How to Use pydep_extractor

This script extracts the dependencies from the `pyproject.toml` file and writes them to a `requirements.txt` file.

The `requirements.txt` file is used by the Dockerfile to install the dependencies before installing the application. This is done to speed up the build process and improve caching.

## Installation

```bash
pip install pydep_extractor
```

## Usage

- To process a specific `pyproject.toml` file and create a `requirements.txt` file:
    ```
    python -m pydep_extractor path/to/pyproject.toml
    ```

- To install the dependency without creating a `requirements.txt` file:
    ```
    python -m pydep_extractor path/to/pyproject.toml --install
    ```

- To set a non-default pip command:
    ```
    python -m pydep_extractor path/to/pyproject.toml --pip-command pip3
    ```

- To ignore specific requirements:
    ```
    python -m pydep_extractor path/to/pyproject.toml --ignore string1 string2
    ```


- To specify a different output file for the dependencies:
    ```
    python -m pydep_extractor path/to/pyproject.toml --output path/to/requirements.txt
    ```

- To specify a different output file for the pyproject if using the ignore dependency options:
    ```
    python -m pydep_extractor path/to/pyproject.toml --pyproject-output path/to/pyproject_filtered.toml
    ```
