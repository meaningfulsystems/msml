"""Access the installed MSML specification."""

import argparse
import shutil
import sys
from importlib import resources
from pathlib import Path


SPEC_RESOURCE = "msml-specification.md"


def spec_path() -> Path:
    """Return the installed path to the MSML specification."""
    return Path(resources.files("msml").joinpath(SPEC_RESOURCE))


def read_spec() -> str:
    """Read the installed MSML specification."""
    return spec_path().read_text()


def main():
    parser = argparse.ArgumentParser(description="Inspect or copy the installed MSML specification.")
    parser.add_argument("--path", action="store_true", help="Print the installed specification path.")
    parser.add_argument("--print", action="store_true", help="Print the specification contents.")
    parser.add_argument("--copy", metavar="PATH", help="Copy the specification to PATH.")
    args = parser.parse_args()

    if not (args.path or args.print or args.copy):
        parser.print_help()
        return

    if args.copy:
        destination = Path(args.copy)
        if destination.is_dir() or destination.suffix == "":
            destination = destination / SPEC_RESOURCE
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(spec_path(), destination)
        print(destination)
        return

    if args.print:
        sys.stdout.write(read_spec())
        return

    if args.path:
        print(spec_path())


if __name__ == "__main__":
    main()
