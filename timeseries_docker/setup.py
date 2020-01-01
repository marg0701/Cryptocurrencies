from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='timeseries_model',
    version='0.0.1',
    description='Here we used Facebook prophet in order to study timeseries for different cryptocurrencies',
    long_description=readme(),
    classifiers=[
        'License :: OSI Approved :: MIT Licence',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],

    keywords='',
    url='',
    author='Miguel Ramírez & Uzmar Gómez',
    author_email='mramirez@softtek.com & uzmar.gomez@softtek.com',
    license='MIT',

    python_requires='>=3.7',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "plotly",
        "ipywidgets",
        "DateTime",
        "numpy",
        "flask",
        "pandas",
        "fbprophet",
        "altair",
        "vega_datasets"
    ],

    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': ['start-timeseries=timeseries_docker:timeseries_app']
    }
)
