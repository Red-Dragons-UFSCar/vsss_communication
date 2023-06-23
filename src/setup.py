from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Pacote de comunicacao VSSS - Red Dragons'
LONG_DESCRIPTION = 'Pacote criado para realizar a interface de comunicacao python entre as areas da equipe Red Dragons UFSCar'

# Setting up
setup(
       # 'name' deve corresponder ao nome da pasta 'verysimplemodule'
        name="vss_communication", 
        version=VERSION,
        author="Joao Carlos",
        author_email="<campijoao@estudante.ufscar.br>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # adicione outros pacotes que 
        # precisem ser instalados com o seu pacote. Ex: 'caer'
        
        keywords=['python', 'vsss', 'communication'],
        classifiers= [
            #"Development Status :: 3 - Alpha",
            #"Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX :: Linux",
        ]
)