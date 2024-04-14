from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
   name='alana',
   version='0.0.4',  # Update the version number as needed
   author='Alana',
   author_email='hi@alana.computer',
   description='Utilities for Alana, and maybe you too. Mostly geared toward LLM-heavy workflows.',
   long_description=long_description,
   long_description_content_type="text/markdown",
   url='https://github.com/alat-rights/alana-utilities',
   packages=find_packages(),
   classifiers=[
         'Development Status :: 3 - Alpha',
         'Intended Audience :: Developers',
         'License :: OSI Approved :: MIT License',
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.6',
         'Programming Language :: Python :: 3.7',
         'Programming Language :: Python :: 3.8',
         'Programming Language :: Python :: 3.9',
   ],
   keywords='LLM, utilities',  # Add relevant keywords
   python_requires='>=3.6',
   install_requires=[
      'anthropic',
      'colorama',
   ],
)