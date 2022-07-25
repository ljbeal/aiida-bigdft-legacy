from aiida.orm.nodes.data import structure

from aiida_common_workflows.workflows.relax.bigdft.generator import BigDftCommonRelaxInputGenerator

from datetime import datetime
import aiida_bigdft
import os

def treat_input(inp_dict: dict,
                structure: structure) -> dict:
    """

    Args:
        inp_dict:
            BigDFT input dictionary, to be treated before packaging
        structure:
            aiida.orm.structure data containing the system

    Returns:
        dict: treated BigDFT input dictionary

    """

    # extract predefined protocols
    protocols = BigDftCommonRelaxInputGenerator._protocols

    acwf_params = inp_dict.pop('acwf_params', {})  # remove the acwf params
    return inp_dict  # passthrough for now

    hgrid_orig = inp_dict['dft'].get('hgrids', None)

    root = os.path.split(aiida_bigdft.__file__)[0]
    psppath = os.path.join(root, 'PyBigDFT/BigDFT/scripts/psppar')
    atoms = structure.get_symbols_set()
    hgrids = {}
    for atom in atoms:
        # set hgrids per atom
        apath = os.path.join(psppath, f'psppar.{atom}')
        with open(apath, 'r') as o:
            this = float(o.readlines()[-1].split('     ')[0].strip())

        hgrids[atom] = round(this*1.1, 2)
    hgrid_min = min(hgrids.values())

    inp_dict['dft']['hgrids'] = hgrid_min

    print(f'hgrid updated from {hgrid_orig} to {hgrid_min}')

    return inp_dict