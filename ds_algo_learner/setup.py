from setuptools import setup, find_packages

setup(
    name="ds_algo_learner",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'ds_algo_learner=ds_algo_learner.cli:main',
        ],
    },
    author="Your Name",
    description="A package for learning data structures and algorithms with web interface",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)