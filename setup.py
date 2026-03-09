from setuptools import setup

setup(
    name="langguard",
    version="1.0.1",
    author="Fatony Ahmad Fauzi",
    author_email="fatonyahmadfauzi@gmail.com",
    description="Multilingual Dictionary Guardian - Analyze and manage DISPLAY_LANGUAGES consistency",
    packages=["langguard"],
    entry_points={
        "console_scripts": [
            "langguard=langguard.main:main",
        ],
    },
)