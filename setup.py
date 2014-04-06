from setuptools import setup

setup(name='synology',
      version='0.1',
      description='Synology DSM 5 API',
      url='http://github.com/satreix/synology',
      author='Steve Barrau',
      author_email='satreix@gmail.com',
      license='MIT',
      packages=['synology'],
      install_requires=[
          'urllib3',
          'clint'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
