from setuptools import setup, find_packages

setup(name='PythonTests',
      version='1.0',
      description="Practice Automation testing",
      author="Andrii Hnatyshyn",
      author_email="andrew.hnatyshyn@gmail.com",
      packeges=find_packages(),
      zip_safe=False,
      izip_safe=False,
      install_requires=[
          "pytest==6.2.5",
          "pytest-html==3.1.1",
          "requests==2.26.0",
          "requests-oauthlib==1.3.0",
          "PyMySQL==1.0.2",
          "WooCommerce==3.0.0",
          "selenium==4.8.1",
          "allure-pytest==2.9.45",
          "allure-python-commons==2.9.45",
          "webdriver_manager==3.8.6"
      ])