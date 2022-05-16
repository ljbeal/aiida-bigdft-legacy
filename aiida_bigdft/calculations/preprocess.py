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
    return inp_dict

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

    now = datetime.now()
    header = f"this call comes from within the prepro, written {now}\n"
    with open('/home/test/acwf/debug-aiida-bigdft-plugin.txt', 'a') as o:
        o.write('\n' + '-' * len(header) + '\n')
        o.write(header)
        o.write(f'unique list of atoms: {atoms}\n')
        o.write(f'filepath: {psppath}\n')
        o.write('hgrid data:\n')
        for a, h in hgrids.items():
            o.write(f'{a}: {h}\n')

        o.write(f'\nthe original hgrid (set by protocol) is {protocol_hgrid}\n')
        o.write(f'the current hgrid (set by scaling) is {scaled_hgrid}\n')
        o.write(f'=> scaling value for this run is {scaling_value}\n')

        o.write(f'==> hgrid will be set to {hgrid_new}\n')

    inp_dict['dft']['hgrids'] = hgrid_min

    return inp_dict