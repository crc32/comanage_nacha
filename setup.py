import setuptools

extras_require = {
    'tests': [
        'pytest',
        'unittest2',
    ],
}

setuptools.setup(
    name='comanage_nacha',
    version='0.0.1',
    url='https://github.com/DisruptiveLabs/comanage_nacha',
    author='DisruptiveLabs',
    author_email='team+nacha@comanage.com',
    description='NACHA File Generation',
    long_description=open('README.md', 'r').read(),
    platforms='any',
    include_package_data=True,
    install_requires=['six'],
    setup_requires=['pytest-runner'],
    extras_require=extras_require,
    tests_require=extras_require['tests'],
    packages=setuptools.find_packages('.', exclude=('tests', 'tests.*')),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    test_suite='nose.collector',
)
