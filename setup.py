from setuptools import setup,find_packages
from typing import List


def give_requirements(file_name:str)->List[str]:
    requirements:List[str] = []
    try:
        with open(file_name,'r') as file_obj:

            lines = file_obj.readlines()

            for line in lines:

                requirement = line.strip()

                if requirement and requirement != '-e .':

                    requirements.append(requirement)
    except FileNotFoundError:
        print("requirements.txt is not found !")

    return requirements


setup(
    name="Network Security",
    version="0.0.1",
    author="Sumit Avasthi",
    author_email="sumitavasthi.28@gmail.com",
    packages=find_packages(),
    install_requires=give_requirements('requirements.txt')
)