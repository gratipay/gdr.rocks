from setuptools import setup, find_packages


setup( name='gdr'
     , packages=find_packages()
     , entry_points = {'console_scripts': ['chomp=gdr.chomp:main']}
      )
