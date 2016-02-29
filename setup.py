from setuptools import setup

setup(
    name           = 'combinedrepo',
    version        = '1.0',
    description    = 'Tool to combine a bunch of seperate local repositories into one single large git repository through git subtree',
    author         = 'devast8a',
    author_email   = 'devast8a@whitefirex.com',
    packages       = ['combinedrepo'],
    package_dir    = {"": "src"},

    entry_points = {
        "console_scripts": [
            'combinedrepo = combinedrepo:main'
        ]
    },

    setup_requires = ['pytest-runner'],
    tests_require  = ['pytest'],
)
