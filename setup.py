import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'waitress',
    'pymongo',
    ]

tests_requires = requires+[]

setup(name='ratchet',
      version='0.0',
      description='ratchet',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      setup_requires=["nose>=1.0", "coverage"],
      author='SciELO',
      author_email='scielo-dev@googlegroups.com',
      url='http://docs.scielo.org',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_requires,
      test_suite="nose.collector",
      entry_points="""\
      [paste.app_factory]
      main = ratchet:main
      """,
      )
