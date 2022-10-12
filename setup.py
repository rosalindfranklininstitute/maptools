#
# Copyright (C) 2020 RFI
#
# Author: James Parkhurst
#
# This code is distributed under the Apache license, a copy of
# which is included in the root directory of this package.
#

from setuptools import setup


def main():
    """
    Setup the package

    """
    tests_require = ["pytest", "pytest-cov", "mock"]

    setup(
        packages=["maptools"],
        install_requires=[
            "styled",
            "gemmi",
            "matplotlib",
            "mrcfile",
            "numpy",
            "pyyaml",
            "scipy",
            "scikit-image",
        ],
        setup_requires=["setuptools_scm", "pytest-runner"],
        tests_require=tests_require,
        test_suite="tests",
        use_scm_version={"write_to": "maptools/_version.py"},
        extras_require={
            "build_sphinx": ["sphinx", "sphinx_rtd_theme"],
            "test": tests_require,
        },
        include_package_data=True,
    )


if __name__ == "__main__":
    main()
