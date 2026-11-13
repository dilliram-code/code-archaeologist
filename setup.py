from io import open
from setuptools import setup

with open('README.md', encoding='utf-8') as read_me:
    long_description = read_me.read()

setup(
    name='Eel',
    version='0.19.0',
    author='Python Eel Organisation',
    author_email='python-eel@protonmail.com',
    url='https://github.com/python-eel/Eel',
    packages=['eel'],
    package_data={
        'eel': ['eel.js', 'py.typed'],
    },
    install_requires=[
        'bottle>=0.12.25,<1.0.0',
        'bottle-websocket>=0.2.9,<1.0.0',
        'gevent>=24.2.1',
        'gevent-websocket>=0.10.1,<1.0.0',
        'greenlet>=3.0.0',
        'pyparsing>=3.1.0,<4.0.0',
        'typing_extensions>=4.8.0',
        'importlib_resources>=5.0.0; python_version < "3.9"',
    ],
    extras_require={
        "jinja2": ['jinja2>=3.1.0'],
        "test": ['pytest>=8.0.0', 'pytest-timeout>=2.3.0', 'psutil>=5.9.0', 'mypy>=1.10.0'],
    },
    python_requires='>=3.9',
    description='For little HTML GUI applications, with easy Python/JS interop',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['gui', 'html', 'javascript', 'electron'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
    ],
)
