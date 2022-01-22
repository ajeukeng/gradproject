from setuptools import setup, find_packages

with open('../gradproject2/README.md') as f:
    readme_content = f.read()

with open('../gradproject2/LICENSE') as f:
    license_content = f.read()

setup(
    name='PACKAGE_NAME',
    version='0.1',
    description='A description of PACKAGE_NAME',
    long_description=readme_content,
    author='Liz Argueta',
    license=license_content,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True
    # install_requires=[
    # ],
    # entry_points={
    #     'console_scripts': [
    #     ],
    # }
)