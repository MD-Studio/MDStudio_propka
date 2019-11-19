# MDStudio ATB

[![Build Status](https://travis-ci.org/MD-Studio/MDStudio_propka.svg?branch=master)](https://travis-ci.org/MD-Studio/MDStudio_propka)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/697c033fd7674ecea28c089150a25dfa)](https://www.codacy.com/app/marcvdijk/MDStudio_ATB?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MD-Studio/MDStudio_ATB&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/MD-Studio/MDStudio_propk/branch/master/graph/badge.svg)](https://codecov.io/gh/MD-Studio/MDStudio_propka)

The MDStudio propka service provides access to the [PROPKA](https://github.com/jensengroup/propka-3.1) software for the
prediction of pKa values of ionizable groups in proteins and protein-ligand complexes based in the 3D structure.
The PROPKA package was developed by the Jensen group at the University of Copenhagen (see reference information below).

## Installation Quickstart
MDStudio propka can be used in the MDStudio environment as Docker container or as standalone service.

### Install option 1 Pre-compiled Docker container
MDStudio propka can be installed quickly from a pre-compiled docker image hosted on DockerHub by:

    docker pull mdstudio/mdstudio_propka
    docker run (-d) mdstudio/mdstudio_propka

In this mode you will first need to launch the MDStudio environment itself in order for the MDStudio ATB service to 
connect to it. You can unify this behaviour by adding the MDStudio ATB service to the MDStudio service environment as:

    MDStudio/docker-compose.yml:
        
        services:
           mdstudio_propka:
              image: mdstudio/mdstudio_propka
              links:
                - crossbar
              environment:
                - CROSSBAR_HOST=crossbar
              volumes:
                - ${WORKDIR}/mdstudio_propka:/tmp/mdstudio/mdstudio_propka

And optionally add `mdstudio_propka` to MDStudio/core/auth/settings.dev.yml for automatic authentication and 
authorization at startup.

### Install option 2 custom build Docker container
You can custom build the MDStudio propka Docker container by cloning the MDStudio_propka GitHub repository and run:

    docker build MDStudio_propka/ -t mdstudio/mdstudio_propka
    
After successful build of the container follow the steps starting from `docker run` in install option 1.

### Install option 3 standalone deployment of the service.
If you prefer a custom installation over a (pre-)build docker container you can clone the MDStudio_propka GitHub
repository and install `mdstudio_propka` locally as:

    pip install (-e) mdstudio_propka/

Followed by:

    ./entry_point_mdstudio_propka.sh
    
or

    export MD_CONFIG_ENVIRONMENTS=dev,docker
    python -u -m mdstudio_propka

## PROPKA References / Citations

Please cite these PROPKA references in publications using this service:

* Sondergaard, Chresten R., Mats HM Olsson, Michal Rostkowski, and Jan H. Jensen. "Improved Treatment of Ligands and Coupling Effects in Empirical Calculation and Rationalization of pKa Values." Journal of Chemical Theory and Computation 7, no. 7 (2011): 2284-2295.

* Olsson, Mats HM, Chresten R. Sondergaard, Michal Rostkowski, and Jan H. Jensen. "PROPKA3: consistent treatment of internal and surface residues in empirical pKa predictions." Journal of Chemical Theory and Computation 7, no. 2 (2011): 525-537.