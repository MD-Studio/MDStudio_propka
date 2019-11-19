# -*- coding: utf-8 -*-

"""
Unit tests for the PropKa methods
"""

import os
import unittest
import shutil

from mdstudio_propka.propka_run import RunPropka


class TestPropKa(unittest.TestCase):

    tmp_files = []
    currpath = os.path.dirname(__file__)
    tmp_dir = os.path.abspath(os.path.join(currpath, '../tmp'))

    def tearDown(self):
        """
        tearDown method called after each unittest to cleanup
        the working directory
        """

        for tmp_file in self.tmp_files:
            if os.path.isdir(tmp_file):
                shutil.rmtree(tmp_file)

    def test_propka_tmpdir(self):
        """
        Run propka in the systems temporary files directory
        """

        infile = os.path.abspath(os.path.join(self.currpath, '../files/3SGB.pdb'))
        out = None
        with open(infile) as pdbfile:
            pka = RunPropka()
            out = pka.run_propka(pdb=pdbfile.read())
            self.tmp_files.append(pka.workdir)

        for outputfile in ('pka_file', 'propka_input_file'):
            self.assertIsInstance(out, dict)
            self.assertEqual(set(out.keys()), {'pka', 'pka_file', 'propka_input_file', 'pi_folded', 'pi_unfolded'})
            self.assertIsNotNone(out.get(outputfile))
            self.assertTrue(os.path.isfile(out[outputfile]))

    def test_propka_customdir(self):
        """
        Run propka in the custom temporary files directory
        """

        infile = os.path.abspath(os.path.join(self.currpath, '../files/3SGB.pdb'))
        out = None
        with open(infile) as pdbfile:
            pka = RunPropka()
            out = pka.run_propka(pdb=pdbfile.read(), workdir=self.tmp_dir)
            self.tmp_files.append(pka.workdir)

        for outputfile in ('pka_file', 'propka_input_file'):
            self.assertIsInstance(out, dict)
            self.assertEqual(set(out.keys()), {'pka', 'pka_file', 'propka_input_file', 'pi_folded', 'pi_unfolded'})
            self.assertIsNotNone(out.get(outputfile))
            self.assertTrue(os.path.isfile(out[outputfile]))

    def test_propka_pkaoutput(self):
        """
        Run default propka and validate pKa prediction
        """

        test_pdbs = ('../files/3SGB.pdb', '../files/4DFR.pdb', '../files/1FTJ-Chain-A.pdb', '../files/1HPX.pdb')
        for pdb in test_pdbs:

            infile = os.path.abspath(os.path.join(self.currpath, pdb))
            with open(infile) as pdbfile:
                pka = RunPropka()
                out = pka.run_propka(pdb=pdbfile.read())
                self.tmp_files.append(pka.workdir)

            # Parse reference data
            ref = []
            with open('{0}.dat'.format(infile.strip('.pdb')), 'r') as rf:
                ref.extend([float(p.strip()) for p in rf.readlines() if p.strip()])
            print(out)
            calc = out['pka']['pKa'].values()
            self.assertListEqual(list(calc), ref)

    def test_propka_titrate(self):
        """
        Test PropKa option for predicting on subset of residues (titrate)
        """

        infile = os.path.abspath(os.path.join(self.currpath, '../files/3SGB-subset.pdb'))
        with open(infile) as pdbfile:
            pka = RunPropka()
            out = pka.run_propka(pdb=pdbfile.read(),
                                 titrate_only='E:17,E:18,E:19,E:29,E:44,E:45,E:46,E:118,E:119,E:120,E:139')
            self.tmp_files.append(pka.workdir)

        # Parse reference data
        ref = []
        with open('{0}.dat'.format(infile.strip('.pdb')), 'r') as rf:
            ref.extend([float(p.strip()) for p in rf.readlines() if p.strip()])

        calc = out['pka']['pKa'].values()
        self.assertListEqual(list(calc), ref)

    def test_propka_warning(self):
        """
        Test PropKa behaviour on input pdb with errors
        """

        infile = os.path.abspath(os.path.join(self.currpath, '../files/1HPX-warn.pdb'))
        with open(infile) as pdbfile:
            pka = RunPropka()
            out = pka.run_propka(pdb=pdbfile.read())
            self.tmp_files.append(pka.workdir)

        calc = list(out['pka']['pKa'].values())
        self.assertEqual(calc[0], 7.95)
        self.assertTrue(len(calc), 1)
