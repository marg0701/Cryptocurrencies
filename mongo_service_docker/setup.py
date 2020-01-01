from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='mongo_service',
    version='0.0.1',
    description='Flask example',
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
    author='Fernando Herrera',
    author_email='fernandoj.herrera@softtek.com',
    license='MIT',

    python_requires='>=3.7',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
         "flask==1.1.1",
         "pymongo",
         #"dnspython",
         "pandas",
         #"efficient-apriori",
         #"newspaper3k==0.2.8"
    ],

    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': ['start-service=webscraper_news_mongo:start_app']
    }
)
