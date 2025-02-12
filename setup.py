from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ffmpeg_installer",
    version="0.1.0",  # Or your preferred version
    author="Your Name",  # Replace with your name
    author_email="brxtnmann@gmail.com",
    description="A tool to install FFmpeg.",  # More specific description
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brxtnmann/Python_Tools",
    py_modules=["install_ffmpeg"],  # List your script
    entry_points={
        "console_scripts": [
            "install_ffmpeg = install_ffmpeg:main",
        ],
    },
    classifiers=[  # Metadata for PyPI (Optional, but recommended)
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Or your minimum Python version
)