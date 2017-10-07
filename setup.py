
from setuptools import setup
from ankita import __version__

def readme():
    with open('README.md') as f:
        return f.read()

setup(
      name='pypicview',
      version=__version__,
      description='A simple useful image viewer with some useful features',
      long_description=readme(),
      keywords='pyqt pyqt5 qt5',
      url='http://github.com/ksharindam/pypicview',
      author='Arindam Chaudhuri',
      author_email='ksharindam@gmail.com',
      license='GNU GPLv3',
      packages=['pypicview'],
      classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Environment :: X11 Applications :: Qt',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python :: 3.5',
      'Topic :: Multimedia :: Graphics',
      ],
      entry_points={
          'console_scripts': ['pypicview=pypicview.main:main'],
      },
      data_files=[
                 ('share/applications', ['files/pypicview.desktop']),
      ],
      include_package_data=True,
      zip_safe=False)
