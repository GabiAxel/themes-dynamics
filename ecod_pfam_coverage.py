import json
from collections import defaultdict
from pathlib import Path

import backoff
import requests
from Bio import SeqIO
from requests import RequestException
from tqdm import tqdm


@backoff.on_exception(backoff.expo, RequestException)
@backoff.on_predicate(backoff.expo, lambda x: 'status' in x and x['status'] == 'PEND')
def get_result_data(uuid: str):
    response = requests.get(f'https://www.ebi.ac.uk/Tools/hmmer/results/{uuid}/score',
                            headers={'Accept': 'application/json'},
                            params={'format': 'json'})
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':

    pdb_paths = Path('domaingroups').glob('*/*.pdb')

    fasta = '\n'.join(f'>{path.stem}\n{next(SeqIO.parse(path, "pdb-atom")).seq}' for path in pdb_paths)

    response = requests.post(f'https://www.ebi.ac.uk/Tools/hmmer/search/hmmscan',
                             allow_redirects=True,
                             data={'hmmdb': 'pfam'},
                             files={'file': fasta},
                             headers={'Accept': 'application/json'})

    job_id = response.json()['job_id']

    response = requests.get(f'https://www.ebi.ac.uk/Tools/hmmer/results/{job_id}',
                            headers={'Accept': 'application/json'},
                            params={'output': 'json'})

    domains_pfam = defaultdict(list)

    for result in tqdm(response.json()['result']):
        for hit in get_result_data(result['uuid'])['results']['hits']:
            for domain in hit['domains']:
                if 'outcompeted' in domain and domain['outcompeted'] == 0:
                    query, pfam, start, end = domain['alisqname'], domain['alihmmacc'], domain['ienv'], domain['jenv']
                    domains_pfam[query[1:]].append([pfam, start, end])

    json.dump(domains_pfam, open('src/assets/pfam.json', 'wt'))