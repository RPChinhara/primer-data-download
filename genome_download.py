import argparse
import json
import subprocess
import shlex
from multiprocessing import Pool

def download_genome(accessionID, species_new):
    command = f'datasets download genome accession {accessionID} --filename {species_new}/{accessionID}.zip'
    subprocess.call(shlex.split(command))

def download_genome_data(species, num_cores):
    print("Downloading: ", species)

    species_new = species.replace(' ', '_')

    command = f'datasets summary genome taxon "{species}"'

    with open(f'{species_new}.json', 'w') as output_file:
        subprocess.call(shlex.split(command), stdout=output_file)

    with open(f'{species_new}.json') as f:
        data = json.load(f)
        subprocess.call(['mkdir', f'{species_new}'])

        accessionIDs = []
        for i in range(data['total_count']):
            if data['reports'][i]['assembly_info']['assembly_level'] == 'Complete Genome':
                accessionID = data['reports'][i]['accession']
                accessionIDs.append(accessionID)

        with Pool(processes=num_cores) as pool:
            pool.starmap(download_genome, [(accessionID, species_new) for accessionID in accessionIDs])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download genomes for a list of species.')
    parser.add_argument('species_file', type=str, help='file containing a list of species')
    parser.add_argument('-n', '--num_cores', type=int, default=1, help='number of cores to use')
    args = parser.parse_args()

    with open(args.species_file) as species_file:
        species = [line.rstrip().lower() for line in species_file]

    print("List of species: ", species)

    for i in species:
        download_genome_data(i, args.num_cores)