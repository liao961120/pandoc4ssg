from setuptools import setup

with open("README.md", encoding="utf-8") as f:
      long_description = f.read().strip()

setup(name='pandoc4ssg',
      version='0.0.1',
      description="Using Pandoc with Static Site Generators",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/liao961120/pandoc4ssg',
      author='Yongfu Liao',
      author_email='liao961120@github.com',
      license='MIT',
      packages=['pandoc4ssg'],
      install_requires=['pypandoc', 'pyyaml', 'toml'],
      # tests_require=['deepdiff'],
      zip_safe=False)
