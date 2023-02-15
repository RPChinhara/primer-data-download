import json
import subprocess
import shlex
import multiprocessing

def download_genome_data(species):
    print("Downloading: ", species)

    species_new = species.replace(' ', '_')

    command = f'datasets summary genome taxon "{species}"'

    with open(f'{species_new}.json', 'w') as output_file:
        subprocess.call(shlex.split(command), stdout=output_file)

    with open(f'{species_new}.json') as f:
        data = json.load(f)
        subprocess.call(['mkdir', f'{species_new}'])

        for i in range(data['total_count']):
            if data['reports'][i]['assembly_info']['assembly_level'] == 'Complete Genome':
                accessionID = data['reports'][i]['accession']
                command = f'datasets download genome accession {accessionID} --filename {species_new}/{accessionID}.zip'
                subprocess.call(shlex.split(command))

if __name__ == '__main__':
    with open('species.txt') as species_file:
        species = [line.rstrip().lower() for line in species_file]

    print("List of species: ", species)

    with multiprocessing.Pool() as pool:
        pool.map(download_genome_data, species)