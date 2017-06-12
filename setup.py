from setuptools import setup, find_packages

setup(name='gmopg',
      version='0.0.3',
      description='Python API Client for GMO Payment Gateway',
      license="MIT",
      keywords="gmopg",
      author='a_r_g_v',
      author_email='info@arg.vc',
      url='https://github.com/a-r-g-v/gmo-payment-python',
      packages=['gmopg'],
      install_requires=['requests', 'six', 'typing']
      )
