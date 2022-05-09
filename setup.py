from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in al_fixtures/__init__.py
from al_fixtures import __version__ as version

setup(
	name="al_fixtures",
	version=version,
	description="Fixtures",
	author="Darcos",
	author_email="contact@darcos.dz",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
