from setuptools import setup, find_packages

setup(
    name='battle_field',
    version='0.1',
    author='afomin/akalmykov',
    company='topcon',
    author_email='afomin@topcom.com',
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'battle_field= battle_field.start_battle:main',
            'battle_field_client= battle_field.sample_client:main',
        ],
    },
    package_data={
        'battle_field': ['images/*', ]
    },
)
