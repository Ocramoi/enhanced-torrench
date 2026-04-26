from setuptools import setup

setup(
    name="torrench",
    version="1.0.0",
    description="A powerful multi-site torrent search tool for the command line",
    author="Mahmoud Almezali",
    author_email="mzmcsmzm@gmail.com",
    url="https://github.com/almezali/enhanced-torrench",
    py_modules=['torrench'],  
    install_requires=[
        "beautifulsoup4>=4.14.3",
        "certifi>=2026.4.22",
        "charset-normalizer>=3.4.7",
        "idna>=3.13",
        "lxml>=6.1.0",
        "pyperclip>=1.11.0",
        "requests>=2.33.1",
        "setuptools>=82.0.1",
        "soupsieve>=2.8.3",
        "tabulate>=0.10.0",
        "termcolor>=3.3.0",
        "typing_extensions>=4.15.0",
        "urllib3>=2.6.3",
    ],
    entry_points={
        'console_scripts': [
            'torrench=torrench:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    requires=[
        "wheel",
    ],
    python_requires=">=3.6"
)

