from setuptools import setup, find_packages

setup(
    name='CopomCalendar',
    version='0.1.0',
    description='Identificar reuniões ordinárias do Copom',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ['copom_calendar=copom_calendar.cli:main'],
    },
    # metadados
    author='Vinícius Salustiano',
    author_email='vsantsal@gmail.com',
    license='proprietary',
    instal_requires=['pytest', 'requests', 'json', 'datetime']
)
