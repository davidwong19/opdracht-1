from setuptools import setup, find_packages

setup(name='Nextbook',
      version='0.1',
      description='My first package!',
      author='Me, myself and I',
      license='MIT',
      packages=find_packages(include=['Nextbook']),
      install_requires=['time','json','requests','bs4','pandas','pymongo','timedelta','redis']
)

