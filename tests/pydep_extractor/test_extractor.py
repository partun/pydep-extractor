from pydep_extractor.extractor import extract_dependencies
from os import remove


def test_extraction():
    extract_dependencies(
        "tests/pydep_extractor/test_pyproject.toml",
        output_file_path="tests/pydep_extractor/test_requirements.txt",
    )

    with open("tests/pydep_extractor/test_requirements.txt", "r") as requirements_file:
        requirements = requirements_file.readlines()

    requirements = list(map(lambda req: req.rstrip("\n"), requirements))
    assert requirements == [
        "toml==0.10.2",
        "pydantic==1.8.2",
        "tqdm==4.62.3",
    ]
    remove("tests/pydep_extractor/test_requirements.txt")


def test_ignore():
    extract_dependencies(
        "tests/pydep_extractor/test_pyproject.toml",
        pyproject_output_path="tests/pydep_extractor/test_pyproject_filtered.toml",
        output_file_path="tests/pydep_extractor/test_requirements.txt",
        ignored_requirements=["toml", "pydantic"],
    )

    with open("tests/pydep_extractor/test_requirements.txt", "r") as requirements_file:
        requirements = requirements_file.readlines()

    requirements = list(map(lambda req: req.rstrip("\n"), requirements))
    assert requirements == [
        "tqdm==4.62.3",
    ]
    remove("tests/pydep_extractor/test_requirements.txt")
    remove("tests/pydep_extractor/test_pyproject_filtered.toml")


def test_optional_dep():
    extract_dependencies(
        "tests/pydep_extractor/test_pyproject.toml",
        output_file_path="tests/pydep_extractor/test_requirements.txt",
        included_optional_dep=["foo"],
    )

    with open("tests/pydep_extractor/test_requirements.txt", "r") as requirements_file:
        requirements = requirements_file.readlines()

    requirements = list(map(lambda req: req.rstrip("\n"), requirements))
    assert requirements == [
        "toml==0.10.2",
        "pydantic==1.8.2",
        "tqdm==4.62.3",
        "pytest==6.2.5",
    ]
    remove("tests/pydep_extractor/test_requirements.txt")
