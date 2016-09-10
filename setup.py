from setuptools import setup

from rust_setuptools import (build_rust_cmdclass, build_install_lib_cmdclass,
                             RustDistribution)

setup(
    name='rusty-re',
    version='0.0.1',
    author='David Blewett',
    author_email='david@dawninglight.net',
    description=('Python bindings for the Rust `regex` create. '
                 'This implementation uses finite automata and guarantees '
                 'linear time matching on all inputs.'),
    license='MIT',
    keywords=['regex', 'rust', 'dfa', 'automata', 'data_structures'],
    url='https://github.com/davidblewett/rusty-re',
    setup_requires=[
        'cffi>=1.0.0'],
    install_requires=['cffi>=1.0.0'],
    cffi_modules=['rusty_re/_build_ffi.py:ffi'],
    tests_require=['pytest', 'psutil', 'decorator'],
    distclass=RustDistribution,
    cmdclass={
        'build_rust': build_rust_cmdclass([('rewrapper', 'rusty_re')]),
        'install_lib': build_install_lib_cmdclass()
    },
    packages=['rusty_re'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Text Processing :: Indexing']
)
