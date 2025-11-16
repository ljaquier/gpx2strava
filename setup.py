from setuptools import setup, find_packages

setup(
    name='gpx2strava',
    version='1.0.0',
    url='https://github.com/ljaquier/ctb2strava',
    author='ljaquier',
    author_email='83839893+ljaquier@users.noreply.github.com',
    description='Simple Python script/library that allows to create an activity on Strava from a GPX file.',
    packages=find_packages(),    
    install_requires=['gpxpy==1.6.2', 'requests==2.32.5']
)
