import setuptools
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.txt')) as f:
    long_description = f.read()

setuptools.setup(
    # This is the name of the project.
    name='testing',  

    # Version
    version='0.1.0',

    # This is a one-line description
    description='Modbus testing project',

    # This is an optional longer description
    long_description=long_description,  # Optional

    # Classifiers help users find your project by categorizing it.
    classifiers=[  # Optional
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=['testing', 'testing/lib', 'testing/tests'],  # Required

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['pymodbus', 'pyserial']  # Optional
)