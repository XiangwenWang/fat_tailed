from setuptools import setup


with open('README.md') as fp:
    readme = fp.read()

setup(
    name='fat_tailed',
    version='1.0.0',
    description='Perform distribution analysis on fat-tailed distributed data',
    long_description=readme,
    author='Xiangwen Wang',
    author_email='wangxiangwen1989@gmail.com',
    url='https://github.com/XiangwenWang/fat_tailed',
    keywords='fat-tailed distribution',
    packages=['fat_tailed'],
    include_package_data=True,
    install_requires=['numpy', 'scipy', 'pandas', 'mpmath', 'matplotlib'],
    license="BSD 2-Clause License",
    zip_safe=True,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: BSD 2-Clause "Simplified" License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
