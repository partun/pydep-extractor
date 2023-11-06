"""
This script extracts the dependencies from the pyproject.toml file and
writes them to a requirements.txt file.

The requirements.txt file is used by the Dockerfile to install the dependencies
before installing the application. This is done to speed up the build process and improve caching.
"""

import argparse
from pydep_extractor.extractor import extract_dependencies


def main():
    parser = argparse.ArgumentParser(
        prog="pydep_extractor", description="Process strings with optional ignore flag"
    )
    parser.add_argument(
        "pyproject_path", type=str, nargs="?", default="pyproject.toml", help="file path"
    )

    parser.add_argument(
        "--install",
        action="store_true",
        help="install the dependency without creating a requirement.txt file",
    )
    parser.add_argument(
        "--pip-command",
        type=str,
        action="store",
        help="set a non default pip command",
        nargs="?",
        default="pip",
    )
    parser.add_argument(
        "--ignore",
        "-I",
        action="store",
        help="String to ignore",
        nargs="+",
        default=[],
    )
    parser.add_argument(
        "--include-optional",
        action="store",
        help="String to ignore",
        nargs="+",
        default=[],
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        action="store",
        help="path to the output the dependencies",
        nargs="?",
        default="requirements.txt",
    )

    parser.add_argument(
        "--pyproject-output",
        type=str,
        action="store",
        help="path to the output the pyproject if using the ignore dependency options",
        nargs="?",
        default="pyproject_filtered.toml",
    )

    args = parser.parse_args()

    extract_dependencies(
        args.pyproject_path,
        args.output if args.output is not None else "requirements.text",
        pyproject_output_path=args.pyproject_output
        if args.pyproject_output is not None
        else "pyproject.toml",
        ignored_requirements=args.ignore,
        install=args.install,
    )


if __name__ == "__main__":
    main()
