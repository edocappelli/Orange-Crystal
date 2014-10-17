#! /usr/bin/env python3

import imp
import os
import sys
import subprocess

NAME = 'Orange-Crystal'

VERSION = '1.0'
ISRELEASED = False

DESCRIPTION = 'Crystal, Crystal diffraction calculation program'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.txt')
LONG_DESCRIPTION = open(README_FILE).read()
AUTHOR = 'Mark Glass, Manuel Sanchez del Rio, Luca Rebuffi and Bioinformatics Laboratory, FRI UL'
AUTHOR_EMAIL = 'mark.glass@esrf.fr'
URL = 'http://orange.biolab.si/'
DOWNLOAD_URL = 'http://github.com/lucarebuffi/Orange-Shadow'
LICENSE = 'GPLv3'

KEYWORDS = (
    'data mining',
    'machine learning',
    'artificial intelligence',
)

CLASSIFIERS = (
    'Development Status :: 1 - Beta',
    'Environment :: X11 Applications :: Qt',
    'Environment :: Console',
    'Environment :: Plugins',
    'Programming Language :: Python',
    'Framework :: Orange',
    'License :: OSI Approved :: '
    'GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: POSIX',
    'Operating System :: Microsoft :: Windows',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
)

INSTALL_REQUIRES = (
    'setuptools',
    'numpy',
    'scipy',
)

if len({'develop', 'release', 'bdist_egg', 'bdist_rpm', 'bdist_wininst',
        'install_egg_info', 'build_sphinx', 'egg_info', 'easy_install',
        'upload', 'test'}.intersection(sys.argv)) > 0:
    import setuptools
    extra_setuptools_args = dict(
        zip_safe=False,  # the package can run out of an .egg file
        include_package_data=True,
        install_requires=INSTALL_REQUIRES
    )
else:
    extra_setuptools_args = dict()

from setuptools import find_packages, setup

PACKAGES = find_packages(
                         exclude = ('*.tests', '*.tests.*', 'tests.*', 'tests'),
                         )

PACKAGE_DATA = {"orangecontrib.shadow.widgets.optical_elements":["icons/*.png", "icons/*.jpg"],
"orangecontrib.shadow.widgets.experimental_elements":["icons/*.png", "icons/*.jpg"],
"orangecontrib.shadow.widgets.optical_elements":["icons/*.png", "icons/*.jpg"],
"orangecontrib.shadow.widgets.loop_management":["icons/*.png", "icons/*.jpg"],
"orangecontrib.shadow.widgets.plots":["icons/*.png", "icons/*.jpg"],
"orangecontrib.shadow.widgets.preprocessor":["icons/*.png", "icons/*.jpg"],
"orangecontrib.shadow.widgets.sources":["icons/*.png", "icons/*.jpg"],
"orangecontrib.shadow.widgets.user_defined":["icons/*.png", "icons/*.jpg"],
}

SETUP_REQUIRES = (
                  'setuptools',
                  )

INSTALL_REQUIRES = (
                    'Orange',
                    'setuptools',
                    'numpy',
                    ),


NAMESPACE_PACAKGES = ["orangecontrib"]

if __name__ == '__main__':
    setup(
          name = NAME,
          version = VERSION,
          description = DESCRIPTION,
          long_description = LONG_DESCRIPTION,
          author = AUTHOR,
          author_email = AUTHOR_EMAIL,
          url = URL,
          download_url = DOWNLOAD_URL,
          license = LICENSE,
          keywords = KEYWORDS,
          classifiers = CLASSIFIERS,
          packages = PACKAGES,
          package_data = PACKAGE_DATA,
          #          py_modules = PY_MODULES,
          setup_requires = SETUP_REQUIRES,
          install_requires = INSTALL_REQUIRES,
          #extras_require = EXTRAS_REQUIRE,
          #dependency_links = DEPENDENCY_LINKS,
          #entry_points = ENTRY_POINTS,
          namespace_packages=NAMESPACE_PACAKGES,
          include_package_data = True,
          zip_safe = False,
          )
