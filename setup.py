from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gif_converter",  # Package name (how it's imported)
    version="0.1.0",
    # ... (rest of the setup.py content is the same as before)
    author="Braxton Heinlein-Manning",
    author_email="brxtnmann@gmail.com",
    description="A tool to convert videos and image sequences to GIF.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brxtnmann/Python_Tools",
    packages=find_packages(), # This will find the gif_converter package
    install_requires=[
        "moviepy",
        "dearpygui",
        "Pillow",
        "ffmpeg_installer",  # ffmpeg_installer is now a *required* dependency
    ],
    entry_points={
        "console_scripts": [
            "gif_converter = gif_converter.gif_converter:main",  # Correct path
        ],
    },
    classifiers=[  # Metadata for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version
    # ... (rest of setup.py is the same)
)