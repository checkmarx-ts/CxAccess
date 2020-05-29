from setuptools import setup

_version = '0.0.1'

install_requires=[
    'PyInquirer',
    'requests',
    'docopt',
    'pyyaml',
    'emoji',
    'pyjwt',
    'yaspin'
]

tests_require=[
    'pytest',
    'mock'
]

setup(
    name='cxacclient',
    version='0.0.2',
    description='Checkmarx CxSAST 9.0 Access Control Client',
    url='https://github.com/checkmarx-ts/CxAcClient',
    author='Uday Korlimarla',
    author_email='Uday.Korlimarla@checkmarx.com',
    classifers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: APACHE-2.0',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='Checkmarx AccessContorl Automation',
    packages=['cxacclient', 'cxacclient.auth', 'cxacclient.utils', 'cxacclient.teams'],
    python_requires='>=3.7',
    install_requires=install_requires,
    extras_require={
        'tests': install_requires + tests_require,
    },
    package_data={'cxacclient': ['templates/*']},
    entry_points={'console_scripts': ['cxacclient=cxacclient.cxacclient:main']}

)
