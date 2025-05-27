import logging
from pathlib import Path

import toml

__package_version = "unknown"


def get_package_version() -> str:
    """Find the version of this package."""
    global __package_version

    if __package_version != "unknown":
        # We already set it at some point in the past,
        # so return that previous value without any
        # extra work.
        return __package_version

    logger = logging.getLogger()
    pyproject_toml_file = Path(__file__).parent.parent / "pyproject.toml"
    logger.debug("pyproject toml file: %s", pyproject_toml_file)
    if pyproject_toml_file.exists() and pyproject_toml_file.is_file():
        data = toml.load(pyproject_toml_file)
        # check project.version
        if "project" in data and "version" in data["project"]:
            __package_version = data["project"]["version"]
        # check tool.poetry.version
        elif "tool" in data and "poetry" in data["tool"] and "version" in data["tool"]["poetry"]:
            __package_version = data["tool"]["poetry"]["version"]
    return __package_version


