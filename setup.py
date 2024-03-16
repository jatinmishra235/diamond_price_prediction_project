from setuptools import find_packages,setup
hypen_e_dot = '-e .'

def get_requirements(filepath):
    requirements = []
    with open(filepath, 'r') as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if hypen_e_dot in requirements:
            requirements.remove(hypen_e_dot)
    return requirements

setup(
    name = 'DiamondPricePrediction',
    version = '0.0.1',
    author = 'jatin',
    author_email= 'jatinmishra235@gmail.com',
    install_requires = get_requirements('requirements.txt'),
    packages = find_packages()


)