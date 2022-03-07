from setuptools import setup, find_packages

with open('README.md') as f:
    readme_content = f.read()

with open('LICENSE') as f:
    license_content = f.read()

setup(
    name='cvt',
    version='2.0',
    description='Tool to View Covid Data',
    long_description=readme_content,
    author='Liz Argueta',
    license=license_content,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    install_requires=['click', 'pandas'],
    entry_points={
        'console_scripts': ['cvt=cli:cvt'
                            ],
    }
)
