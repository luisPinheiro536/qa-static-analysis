#!/usr/bin/env python3
"""Setup configuration for robotframework-quality-scanner."""

from setuptools import setup, find_packages

setup(
    name="robotframework_quality_scanner",
    version="0.4.0",
    author="Luis",
    author_email="luis@example.com",
    description="Quality scanner for Robot Framework automation - static analysis, performance, duplication detection, and automatic report generation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/luisPinheiro536/qa-static-analysis",
    project_urls={
        "Repository": "https://github.com/luisPinheiro536/qa-static-analysis.git",
        "Issues": "https://github.com/luisPinheiro536/qa-static-analysis/issues",
        "Documentation": "https://github.com/luisPinheiro536/qa-static-analysis/wiki",
    },
    license="Apache-2.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "robotframework>=6.0",
    ],
    extras_require={
        "dev": ["pytest>=7.0", "black>=22.0", "flake8>=4.0"],
        "api": ["flask>=2.0"],
        "all": ["pytest>=7.0", "black>=22.0", "flake8>=4.0", "flask>=2.0"],
    },
    entry_points={
        "console_scripts": [
            "qa-scanner=robotframework_quality_scanner.cli:main",
        ],
    },
    keywords=["robotframework", "quality", "testing", "static-analysis", "automation"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Testing",
    ],
)
