from setuptools import setup, find_packages

setup(
   name='alana',
   version='0.0',
   description='Utilities for Alana, and maybe you too. Mostly geared toward LLM-heavy workflows.',
   author='Alana',
   author_email='hi@alana.computer',
   packages=find_packages(),  #same as name
   install_requires=['anthropic', 'typing', 'colorama'], #external packages as dependencies
)