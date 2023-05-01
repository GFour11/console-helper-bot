from setuptools import setup, find_namespace_packages

setup(
    name='contact-bot',
    version='1',
    description='console-helper-bot',
    url='https://github.com/Dmytro-Babenko/console-helper-bot',
    author='Dmytro Babenko',
    author_email='dmytro.babenko87@gmail.com',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['contact-bot = console_bot.main:main']}
)