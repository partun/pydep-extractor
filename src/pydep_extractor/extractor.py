import toml
from typing import Optional, Iterable, List, Dict, Any
from subprocess import run, CalledProcessError


def filter_dependencies(
    pyproject: Dict[str, Any], pyproject_output_path: str, ignored_requirements: Iterable[str]
):
    def filter_ignored(dependency: str) -> bool:
        for ignore in ignored_requirements:
            if dependency.startswith(ignore):
                print(f"ignoring dependency {dependency}")
                return False
        return True

    dependencies = pyproject["project"]["dependencies"]
    dependencies = list(filter(filter_ignored, dependencies))
    pyproject["project"]["dependencies"] = dependencies

    with open(pyproject_output_path, "w") as output_toml_file:
        toml.dump(pyproject, output_toml_file)


def extract_dependencies(
    pyproject_path: str,
    output_file_path: str,
    *,
    pyproject_output_path: str = "pyproject_filtered.toml",
    ignored_requirements: Optional[Iterable[str]] = None,
    install: bool = False,
    included_optional_dep: Optional[Iterable[str]] = None,
    pip_command: str = "pip",
) -> None:
    try:
        # Read the TOML configuration file
        with open(pyproject_path, "r") as toml_file:
            pyproject = toml.load(toml_file)

    except (FileNotFoundError, OSError) as err:
        print(err)
        exit(1)

    if ignored_requirements:
        filter_dependencies(pyproject, pyproject_output_path, ignored_requirements)

    dependencies: List[str] = pyproject["project"]["dependencies"]

    if included_optional_dep:
        for opt_dep in included_optional_dep:
            try:
                opt_dependencies = pyproject["project"]["optional-dependencies"][opt_dep]
                dependencies.extend(opt_dependencies)

            except KeyError:
                print(f"no optional dependencies for '{opt_dep}'")

    if install:
        # install the dependencies
        install_requirements(dependencies, pip_command=pip_command)
    else:
        # create requirements file
        write_requirements(output_file_path, dependencies)


def install_requirements(dependencies: Iterable[str], *, pip_command: str = "pip"):
    cmd = [pip_command, "install"]
    cmd.extend(dependencies)

    if len(cmd) < 3:
        print("nothing to install")
        return

    try:
        run(cmd, check=True)
    except CalledProcessError as err:
        print(err)
        exit(err.returncode)


def write_requirements(output_file_path: str, dependencies: Iterable[str]):
    with open(output_file_path, "w") as requirements_file:
        requirements_file.write("\n".join(dependencies))
        requirements_file.write("\n")
