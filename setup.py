from setuptools import setup, find_packages

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

setup(
    name="FanpieFilmFeed",
    version="1.0.0",
    description="🎬A fully complete FanpieFilm podcast rss feed with detailed shownotes.",
    long_description=readme,
    author="Reyshawn",
    author_email="reshawnchang@gmail.com",
    url="https://github.com/Reyshawn/FanpieFilmFeed",
    packages=find_packages(exclude=['test']),
    install_requires=[
        "scrapy==2.4.0"
    ]
)
