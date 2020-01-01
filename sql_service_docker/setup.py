from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='sql_historical',
    version='0.0.1',
    description='Historical database for cryptocurrencies',
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
    author='Luis Gerardo Guzmán',
    author_email='luisg.guzman@softtek.com',
    license='MIT',

    python_requires='>=3.7',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "flask",
        "pandas",
        "xlrd >= 1.0.0",
        "sqlalchemy",
        "flask-mysqldb",
        "requests"
    ],

    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': ['start-sql_service=sql_service_port:sql_service_app']
    }
)
