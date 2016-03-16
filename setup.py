from setuptools import setup

setup(name='tackdb',
      version='0.1',
      description='The key-value store the world needs.',
      url='https://github.com/vroomwaddle/tackdb.git',
      license='MIT',
      entry_points={'console_scripts': ['tackdb-cli = tackdb.sessions:main']},
      packages=['tackdb'],
      zip_safe=False)
