# This is the setup file which will help to install anykind of package as a loacl package
from setuptools import setup, find_packages

# Going to initialize the setup
setup(
    name="medical_chatbot", # name of the my project
    version="0.1.0", # version of the project
    author="Nishant Ketu", # author name
    author_email="nishantketu363@gmail.com", # author email
    description="A medical chatbot that provides health-related information and assistance.", # short description about the
    packages=find_packages(), # It will find the cunstructor file(__init__.py) so where it will find the cunstructor file that folder it will install the local packages
    install_requires=[] # This will automatically take all the dependencies from requirements.txt file and install them

)