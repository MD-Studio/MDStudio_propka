# -*- coding: utf-8 -*-

"""
file: wamp_services.py

WAMP service methods the module exposes.
"""

from mdstudio.api.endpoint import endpoint
from mdstudio.component.session import ComponentSession

from mdstudio_propka.propka_run import RunPropka
from mdstudio_propka.propka_helpers import validate_file_object


class PropkaWampApi(ComponentSession):

    def authorize_request(self, uri, claims):
        """
        If you were allowed to call this in the first place,
        I will assume you are authorized
        """
        return True

    @endpoint('propka', 'propka_request', 'propka_response')
    def run_propka(self, request, claims):
        """
        Run PROPKA predicts of the pKa values of ionizable groups in proteins
        and protein-ligand complexes based in the 3D structure.

        For a detailed input description see:
          mdstudio_propka/schemas/endpoints/propka_request.v1.json

        For a detailed output description see:
          mdstudio_propka/schemas/endpoints/propka_response.v1.json
        """

        # Validate input path_file object for PDB file
        pdb = validate_file_object(request['pdb'])
        if pdb:
            del request['pdb']
        else:
            return {'status': 'failed'}

        # Run propka
        propka = RunPropka(log=self.log)
        result = propka.run_propka(pdb=pdb, **request)

        return {'status': 'completed', 'output': result}
