from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-event-scheduler',
    version='0.6.0',
    description='This plugin schedules event at given time.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Risto Kowaczewski',
    author_email='risto.kowaczewski@gmail.com',
    packages=['tracardi_event_scheduler'],
    install_requires=[
        'tracardi_plugin_sdk>=0.6.18',
        'asyncio',
        'tracardi',
        'pytimeparse'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    keywords=['tracardi', 'plugin'],
    include_package_data=True,
    python_requires=">=3.8",
)
