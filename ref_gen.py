import json
import subprocess
import shlex

with open('species.txt') as species_file:
    species = [line.rstrip().lower() for line in species_file]

print("List of species: ", species)

for i in species:
    print("Downloading: ", i)

    i_new = i.replace(' ', '_')

    command = f'datasets summary genome taxon "{i}"'

    with open(f'{i_new}.json', 'w') as output_file:
        subprocess.call(shlex.split(command), stdout=output_file)

    with open(f'{i_new}.json') as f:
        data = json.load(f)
        subprocess.call(['mkdir', f'{i_new}'])

        for i in range(data['total_count']):
            if data['reports'][i]['assembly_info']['assembly_level'] == 'Complete Genome':
                accessionID = data['reports'][i]['accession']
                command = f'datasets download genome accession {accessionID} --filename {i_new}/{accessionID}.zip'
                subprocess.call(shlex.split(command))
