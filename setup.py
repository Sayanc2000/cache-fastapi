from setuptools import setup

long_description = """"
# Cache-FastAPI

A lightweight caching library which leverages FastAPI's middleware functionality
and follows best practices of cache-control to easily speed up your large requests.

N.B: Only GET requests get cached
"""

setup(
    name="cache_fastapi",
    packages=['cache_fastapi'],
    version="0.0.2",
    author="Sayan Chakraborty",
    author_email="sayanc20002@gmail.com",
    description="Clean caching library for FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sayanc2000/cache-fastapi",
    include_package_data=True,
    install_requires=['redis', 'python-dotenv'],
    license='MIT License',
    keywords=[
            'redis', 'aioredis', 'asyncio', 'fastapi', 'starlette', 'cache'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
      ],
    python_requires='>=3.6',
)
