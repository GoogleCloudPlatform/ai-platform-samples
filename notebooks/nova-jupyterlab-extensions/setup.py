"""
Setup module for the jupyterlab_nova proxy extension
"""
import setuptools
from setupbase import (
    create_cmdclass, ensure_python, find_packages
    )

data_files_spec = [
    ('etc/jupyter/jupyter_notebook_config.d',
     'jupyter-config/jupyter_notebook_config.d', 'jupyterlab_nova.json'),
]

requires = [line.strip() for line in open('requirements.txt').readlines() if not line.startswith("#")]

cmdclass = create_cmdclass(data_files_spec=data_files_spec)

setup_dict = dict(
    name='jupyterlab_nova',
    description='Plugin that allows to submit Notebooks for background training.',
    packages=find_packages(),
    cmdclass=cmdclass,
    author          = 'Viacheslav Kovalevskyi',
    author_email    = 'viacheslav@kovalevskyi.com',
    license         = 'MIT',
    platforms       = "Linux, Mac OS X, Windows",
    keywords        = ['Jupyter', 'JupyterLab', 'GitHub'],
    python_requires = '>=3.5',
    classifiers     = [
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=requires
)

setuptools.setup(
    version="0.3.0",
    **setup_dict
)
