# -*- coding: utf-8 -*-

"""
MDStudio propka component

PROPKA predicts the pKa values of ionizable groups in proteins and
protein-ligand complexes based in the 3D structure.

When using this component in scientific work please cite:
- Mats H.M. Olsson, Chresten R. Sondergard, Michal Rostkowski, and Jan H. Jensen
  "PROPKA3: Consistent Treatment of Internal and Surface Residues in Empirical
  pKa predictions." Journal of Chemical Theory and Computation, 7(2):525-537
  (2011)
"""

import os

__module__ = 'mdstudio_propka'
__docformat__ = 'restructuredtext'
__version__ = '{major:d}.{minor:d}'.format(major=1, minor=0)
__author__ = 'Marc van Dijk'
__status__ = 'release alpha1'
__date__ = '12 december 2019'
__licence__ = 'Apache Software License 2.0'
__url__ = 'https://github.com/MD-Studio/MDStudio_propka'
__copyright__ = "Copyright (c) VU University, Amsterdam"
__package_path__ = os.path.dirname(os.path.realpath(__file__))
