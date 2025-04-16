from setuptools import setup

setup(
    name='FICOFORD',
    version='0.1',
    description="Fico For D...",
    long_description="",
    author='rskene',
    author_email='rjskene83@gmail.com',
    license='none',
    zip_safe=False,
    install_requires=[
        'docutils',
        'jinja2',
        'nbconvert==5.6.1',
        'traitlets',
        'nbformat',
        'sphinx>=1.8',
        'sphinx-rtd-theme',
        'ipython',
        ],
)