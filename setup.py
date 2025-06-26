from setuptools import setup, find_packages

setup(
    name='rotation_enhance',
    version='0.1.0',
    description='A library for image and label rotation enhancement with YOLO support',
    author='li',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
        'ultralytics'
    ],
    python_requires='>=3.7',
    include_package_data=True,
)