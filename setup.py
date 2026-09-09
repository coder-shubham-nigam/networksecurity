"""
    This is an essential part of packaging and distributing Python projects. It is used by setuptools to define the configuration of the project, such as its metadata, dependencies and more. 
"""

from setuptools import find_packages,setup
from typing import List 

def get_requirements()->List[str]:
    '''
    This function will return list of requirements
    '''
    requirement_lst:List[str] = [] 
    try:
        with open('requirements.txt' , 'r') as f:
            lines = f.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
        
    return requirement_lst

setup(
    name= "NetworkSecurity",
    version="0.0.1",
    author="Shubham Nigam",
    author_email= "shubham.nigam2005@gmail.com",
    packages=find_packages(),
    install_requires= get_requirements()
)