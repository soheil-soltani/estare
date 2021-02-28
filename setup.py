import setuptools

from distutils import core
from distutils.extension import Extension
from Cython.Distutils import build_ext



with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="estare", 
    version="0.0.2",
    author="Soheil Soltani",
    author_email="soheil@netc.eu",
    description="Package for stacking astrophoto images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soheil-soltani/estare",
    packages=setuptools.find_packages(),
    package_dir={'' : './'},
    classifiers=[
        "Programming Language :: Python :: 3",
	"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts' : ['estare = estare.estare:main']
    }
)

core.setup(
    cmdclass = {'build_ext' : build_ext},
    ext_modules = [Extension("calculate", ["estare/src/arc.pyx"])]
    )

