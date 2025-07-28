"""
Setup script for Thomson PDF Generator
"""
from setuptools import setup, find_packages
import os

# Read README file
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_path, 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(requirements_path, 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="thomson-pdf-generator",
    version="1.0.0",
    author="Thomson-BG",
    author_email="contact@thomson-bg.com",
    description="A comprehensive PDF converter, viewer, editor, and signing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Thomson-BG/thomson_pdf_generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "thomson-pdf-generator=main:main",
        ],
    },
    keywords="pdf converter editor signer document office",
    project_urls={
        "Bug Reports": "https://github.com/Thomson-BG/thomson_pdf_generator/issues",
        "Source": "https://github.com/Thomson-BG/thomson_pdf_generator",
        "Documentation": "https://github.com/Thomson-BG/thomson_pdf_generator/wiki",
    },
    include_package_data=True,
    zip_safe=False,
)