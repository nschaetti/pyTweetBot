from setuptools import setup, find_packages

setup(
      name='pyTweetBot',
      version='0.1.2',
      description='A Twitter bot to collect articles and news from the Web and tweet/retweet it on your feed',
      classifiers=[
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary'
      ],
      keywords='twitter bot nlp news tweet',
      url='https://github.com/nschaetti/pyTweetBot',
      author='Nils Schaetti',
      author_email='n.schaetti@gmail.com',
      license='GPL',
      include_package_data=True,
      packages=find_packages(),
      install_requires=['nltk', 'argparse', 'logging', 'tweepy', 'sklearn', 'pygithub', 'brotli', 'httplib2',
                        'urlparse2', 'HTMLParser', 'bs4', 'simplejson', 'dnspython', 'dill', 'lxml', 'sqlalchemy',
                        'feedparser', 'textblob', 'numpy', 'scipy', 'mysql-python']
)
