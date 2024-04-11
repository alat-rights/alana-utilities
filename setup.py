from setuptools import setup

setup(
   name='alana',
   version='0.0',
   description='Utilities for Alana, and maybe you too. Mostly geared toward LLM-heavy workflows.',
   author='Alana',
   author_email='hi@alana.computer',
   packages=['alana'],  #same as name
   install_requires=['re', 'anthropic', 'os', 'typing', 'colorama', 'logging'], #external packages as dependencies
)