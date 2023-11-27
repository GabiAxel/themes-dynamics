import json
import shutil
from pathlib import Path

from biotite.structure.io import load_structure
from pydash import substr_left, chain
from pylightxl import readxl, Database
import numpy as np
from pymolPy3 import pymolPy3
from tqdm.contrib.concurrent import process_map

all_rgb = [
    [255, 0, 0],
    [0, 0, 255],
    [139, 0, 0],
    [0, 0, 139],
    [178, 34, 34],
    [0, 71, 171],
    [220, 20, 60],
    [25, 25, 112],
    [255, 36, 0],
    [65, 105, 225],
    [210, 4, 45],
    [0, 150, 255],
    [196, 30, 58],
    [0, 195, 255],
    [255, 49, 49],
    [135, 206, 235]
]

public_path = Path('public')

def process_domain(xlsx_path: Path):

    dir = xlsx_path.parent
    group = xlsx_path.parts[-2]
    domain = substr_left(xlsx_path.stem, '_')
    pdb_path = dir / f'{domain}.pdb'

    structure = load_structure(str(pdb_path))
    length = int(chain(structure).filter({'hetero': False}).map('res_id').max().value())

    pm = pymolPy3(0)

    for i, rgb in enumerate(all_rgb):
        pm(f'set_color color_{i}={rgb}')

    pm(f'load "{pdb_path.absolute()}"; orient')

    pm(f'spectrum count, rainbow, {domain}')
    pm('ray 300, 300')
    thumbnail_path = (public_path / 'thumbnail' / f'{domain}.png').absolute()
    pm(f'png {thumbnail_path}')

    wb: Database = readxl(xlsx_path)
    ws = wb.ws(wb.ws_names[0])
    mode_hinges = np.transpose(ws.range('F3:L100'))
    view_data_dynamic_domains = []

    for i, column in enumerate(mode_hinges):

        mode = f'Mode-{i+1}'
        hinges = [int(residue) for residue in column if residue not in ['', '0']]
        ranges = [f'{hinges[j]}:{hinges[j+1]-1}' for j in range(len(hinges)-1)]
        pm(f'copy {mode}, {domain}; remove model {mode} and not ({" or ".join([f"resi {r}" for r in ranges])})')

        view_data_dynamic_domains.append([[hinges[j], hinges[j+1]-1] for j in range(len(hinges)-1)])

        for j, r in enumerate(ranges):
            pm(f'color color_{j}, model {mode} and resi {r}')

    view_data_themes = []

    for theme, start_residue, end_residue, index in ws.range('A2:D200'):
        if theme == '' or index == '':
            break
        pm(f'copy {theme}, {domain}')
        pm(f'remove model {theme} and not resi {start_residue}:{end_residue}')
        pm(f'cartoon tube, (model {theme}); color yellow, (model {theme})')

        view_data_themes.append([theme, start_residue, end_residue])

    pm(f'color bluewhite, {domain}')
    pm(f'set cartoon_transparency, 0.5, {domain}')

    pm(f'disable all; enable (model {domain} or Mode-1)')
    pymol_path = (public_path / 'pymol' / f'{domain}.pse').absolute()
    pm(f'save {pymol_path}')

    shutil.copyfile(pdb_path, public_path / 'pdb' / pdb_path.parts[-1])
    shutil.copyfile(xlsx_path, public_path / 'xlsx' / xlsx_path.parts[-1])

    return {
        'domain': domain,
        'group': group,
        'length': length,
        'modes': view_data_dynamic_domains,
        'themes': view_data_themes
    }


if __name__ == '__main__':
    xlsx_paths = list(Path('domaingroups').glob('*/[!~]*.xlsx'))
    view_data = process_map(process_domain, xlsx_paths, max_workers=12)
    json.dump(view_data, open(Path('src') / 'assets' / 'domains.json', 'wt'))