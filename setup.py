import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="manga-indexer-neetlord",
    version="0.0.1",
    author="neetlord",
    author_email="neetlord@fpoint.tech",
    description="A python tool for indexing manga websites",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neet-lord/manga-indexer",
    
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        manga-indexer=manga-indexer.__main__:main
    '''
)