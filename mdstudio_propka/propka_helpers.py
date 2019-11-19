# -*- coding: utf-8 -*-

"""
file: propka_helpers.py

Helper functions to parse PROPKA output
"""

import os
import json
import logging
import pkg_resources

from pandas import DataFrame
from propka.lib import parse_res_string

from mdstudio_propka import __package_path__, __module__

logger = logging.getLogger(__module__)
PROPKA_SCHEMA = os.path.join(__package_path__, 'schemas/endpoints/propka_request.v1.json')


class AttributeDict(dict):

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value


def propka_options(options):
    """
    Construct a dictionary like object of PROPKA parameters using
    the JSON schema as default (schemas/endpoints/propka_request.v1.json)
    supplemented with user defined parameters.

    :param options: user defined PROPKA parameters
    :type options:  :py:dict

    :return:        PROPKA parameter object
    :rtype:         :py:AttributeDict
    """

    # Parse default PROPKA options from JSON schema.
    default_options = AttributeDict()
    with open(PROPKA_SCHEMA) as prs:
        dfs = json.load(prs)
        for key, value in dfs['properties'].items():
            default_options[key] = value.get('default', None)

    # Update with existing data
    if options:
        for key, value in options.items():
            if key in default_options:
                default_options[key] = value
            else:
                logger.warning('Parameter {0} not supported by PROPKA'.format(key))

    # Set propka.cfg file
    default_options.parameters = pkg_resources.resource_filename('propka', "propka.cfg")

    # Convert titrate_only string to a list of (chain, resnum) items:
    if default_options.titrate_only:
        res_list = []
        for res_str in default_options.titrate_only.split(','):
            try:
                chain, resnum, inscode = parse_res_string(res_str)
            except ValueError:
                logger.critical('Invalid residue string: "%s"' % res_str)
                continue
            res_list.append((chain, resnum, inscode))
        default_options.titrate_only = res_list

    return default_options


def parse_propka_pkaoutput(pkafile):
    """
    Parse PROPKA .pka output

    Extract pka SUMMARY block and parse to Pandas dataframe

    :param pkafile: pka file
    :type pkafile:  :py:str

    :return:        Pandas DataFrame
    """

    output = []
    with open(pkafile, 'r') as pkf:
        p = None
        for line in pkf.readlines():
            if line.startswith('SUMMARY OF THIS PREDICTION'):
                p = 1
                continue
            if line.startswith('------'):
                p = None
                continue
            if isinstance(p, int):
                if p <= 0:
                    output.append(line.split())
                p -= 1

    df = DataFrame(output)
    if df.empty:
        return df

    if df.shape[1] == 5:
        df.columns = ['resname', 'resnum', 'chain', 'pKa', 'model-pKa']
    else:
        df.columns = ['resname', 'resnum', 'chain', 'pKa', 'model-pKa', 'lig-attype']

    # Convert dtypes
    df['pKa'] = df['pKa'].astype(float)
    df['model-pKa'] = df['model-pKa'].astype(float)

    return df


def validate_file_object(path_file):
    """
    Validate a MDStudio path_file object

    - If no 'content' check if path exists and import file

    :param path_file: path_file object
    :type path_file:  :py:dict

    :return:          validated path_file object
    :rtype:           :py:dict
    """

    if path_file['path'] is not None:

        if os.path.exists(path_file['path']):
            with open(path_file['path']) as pf:
                path_file['content'] = pf.read()
        else:
            logger.error('File path does not exist: {0}'.format(path_file['path']))

    return path_file['content']
