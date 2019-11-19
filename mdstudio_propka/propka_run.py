# -*- coding: utf-8 -*-

"""
file: propka_run.py

Main class for running the PROPKA and propkatraj Python code.
"""

import os
import logging
import tempfile
import MDAnalysis as mda

from propka import molecular_container
from propkatraj import get_propka

from mdstudio_propka import __module__
from mdstudio_propka.propka_helpers import parse_propka_pkaoutput, propka_options

logger = logging.getLogger(__module__)


class Struct:

    def __init__(self, entries):
        self.__dict__.update(entries)


class RunPropka(object):

    """
    Predicts the pKa values of ionizable groups in proteins and protein-ligand
    complexes based in the 3D structure.

    Uses the PROPKA Python code developed by the Jensen group:
    - https://github.com/jensengroup/propka-3.1

    Reference:
    - Sondergaard, Chresten R., Mats HM Olsson, Michal Rostkowski, and Jan H.
      Jensen. "Improved Treatment of Ligands and Coupling Effects in Empirical
      Calculation and Rationalization of pKa Values." Journal of Chemical
      Theory and Computation 7, no. 7 (2011): 2284-2295.
    - Olsson, Mats HM, Chresten R. Sondergaard, Michal Rostkowski, and Jan H.
      Jensen. "PROPKA3: consistent treatment of internal and surface residues
      in empirical pKa predictions." Journal of Chemical Theory and Computation
      7, no. 2 (2011): 525-537.
    """

    def __init__(self, log=logging):

        self.workdir = tempfile.mkdtemp()
        self.currdir = os.getcwd()
        self.log = log

    def run_propkatraj(self, topology=None, trajectory=None, sel='protein', start=None, stop=None, step=None,
                       session=None):
        """
        Run propkatraj

        Runs Propka3.1 on a MD trajectory in a format that can be handled by
        the MDanalysis package

        :param kwargs:  PROPKA options
        :type kwargs:   :py:dict
        :param session: WAMP session object
        :type session:  :py:dict

        :return:        PROPKA results
        :rtype:         :py:dict
        """
        # Load trajectory
        universe = mda.Universe(topology, trajectory)

        # Run propkatraj
        pkatrajdf = get_propka(universe, sel=sel, start=start, stop=stop, step=step)

        return {'session': session}

    def run_propka(self, pdb, **kwargs):
        """
        Run PROPKA

        :param pdb:     3D structure of protein or ptrotein-ligand in RCSB
                        PDB format
        :type pdb:      :py:str
        :param kwargs   additional PROPKA keyword parameters, see:
                        mdstudio_propka/schemas/endpoints/propka_request.v1.json
        :type kwargs    :py:dict

        :return:        Parsed PROPKA output, see:
                        mdstudio_propka/schemas/endpoints/propka_response.v1.json
        :rtype:         :py:dict
        """

        propka_config = propka_options(kwargs)

        # Create alternative workdir
        if 'workdir' in kwargs:
            if not os.path.isdir(kwargs['workdir']):
                os.makedirs(kwargs['workdir'])
            self.workdir = kwargs['workdir']

        os.chdir(self.workdir)
        self.log.info('PropKa working directory: {0}'.format(self.workdir))

        pdbfile = os.path.join(self.workdir, 'propka.pdb')
        with open(pdbfile, 'w') as infile:
            infile.write(pdb)

        # Run PROPKA
        my_molecule = molecular_container.Molecular_container(pdbfile, propka_config)
        my_molecule.calculate_pka()
        my_molecule.write_pka()
        self.log.info('Running PROPKA 3.1: {0}'.format(type(my_molecule.version).__name__.split('.')[-1]))

        # Parse PROPKA output
        output = {}
        for output_types in ('pka', 'propka_input'):
            outputfile = os.path.join(self.workdir, '{0}.{1}'.format(my_molecule.name, output_types))

            if not os.path.isfile(outputfile):
                self.log.error('Propka failed to create output: {0}'.format(outputfile))
                continue

            if output_types == 'pka':
                pkadf = parse_propka_pkaoutput(outputfile)
                output['pka'] = pkadf.to_dict()

            output['{0}_file'.format(output_types)] = outputfile

        # Calculate molecule PI
        pi_labels = ('pi_folded', 'pi_unfolded')
        for i, pi in enumerate(my_molecule.getPI()):
            output[pi_labels[i]] = pi

        # Change back to original dir and return results
        os.chdir(self.currdir)

        return output
