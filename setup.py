from setuptools import setup

setup(
    name='invertsquared',
    version='0.9',
    description='mobile game for quick puzzling',
    author='Jeremiah Blanchard',
    author_email='jjb@eng.ufl.edu',
    url='https://github.com/JAlexHouse/invertsquared',
    install_requires=[
        'kivy',
        'docutils',
        'pygments',
        'pypiwin32',
        'kivy.deps.sd12',
        'kivy.deps.glew'
    ]
    )