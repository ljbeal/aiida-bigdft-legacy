from aiida.orm.nodes.data import structure

try:
    from aiida_common_workflows.workflows.relax.bigdft.generator import BigDftCommonRelaxInputGenerator
    cwf = False
except ImportError:
    BigDftCommonRelaxInputGenerator = None
    cwf = False

from datetime import datetime
import aiida_bigdft
import os
import yaml


def treat_input(inp_dict: dict,
                structure: structure,
                auto_hgrid: bool = False) -> dict:
    """

    Args:
        inp_dict:
            BigDFT input dictionary, to be treated before packaging
        structure:
            aiida.orm.structure data containing the system
        auto_hgrid (bool):
            automatically scale the hgrid

    Returns:
        dict: treated BigDFT input dictionary

    """

    if not auto_hgrid:
        return inp_dict

    # extract predefined protocols
    # protocols = BigDftCommonRelaxInputGenerator._protocols

    hgrid_orig = inp_dict['dft'].get('hgrids', None)

    root = os.path.split(aiida_bigdft.__file__)[0]
    psppath = os.path.join(root, 'PyBigDFT/BigDFT/scripts/psppar')
    atoms = structure.get_symbols_set()
    hgrids = {}
    for atom in atoms:
        # set hgrids per atom
        apath = os.path.join(psppath, f'psppar.{atom}')
        with open(apath, 'r') as o:
            for line in o.readlines():
                rcore = -1
                if 'rcore' in line:
                    rcore = float(line.split('     ')[0].strip())

            if rcore == -1:
                # no value available for this element, fall through
                return inp_dict

        hgrids[atom] = round(rcore * 1.1, 2)
    hgrid_min = min(hgrids.values())

    inp_dict['dft']['hgrids'] = [hgrid_min] * 3

    return inp_dict
