import csv
import json
import os

VOCAB_FILE = 'vocab.csv'
ICONS_DIR = 'invicon/invicon'
NODE_OVERRIDES = 'node_overrides.json'
NODE_ADDITIONS = 'node_additions.json'

# Map icon file names to lowercase item names (not perfect, may contain misc. identifiers, like BE for Bedrock Edition)
icons = {}
for icon_fname in os.listdir(ICONS_DIR):
    name = icon_fname.lower().replace('_', ' ').replace('invicon ', '').split('.')[0]
    icons[name] = icon_fname

# Convert into graph object with nodes and links, for D3
vocab_csv = csv.DictReader(open(VOCAB_FILE))

graph = {
    'nodes': [],
    'links': [],
}

node_overrides = json.load(open(NODE_OVERRIDES))

for word in vocab_csv:
    ety_roots = [root.strip() for root in word['Etymological roots'].split(',') if root.strip() != '']

    word_id = word['Pidgin word']

    new_node = {
        'id': word_id,
        'def': word['English definition'],
        'sessionDocumented': word['Session documented'],
        'etymologicalRoots': ety_roots,
    }
    
    if word_id in node_overrides:
        for key in node_overrides[word_id]:
            new_node[key] = node_overrides[word_id][key]

    graph['nodes'].append(new_node)

    for root in ety_roots:
        graph['links'].append({
            'source': root,
            'target': word['Pidgin word'],
        })
    


# Resolve icons for words if possible
for word in graph['nodes']:
    for sense in word['def'].replace(';', ',').split(','):
        sense = sense.lower().strip()

        if sense in icons:
            word['icon'] = icons[sense]
            break
        elif f'{sense} head' in icons:
            word['icon'] = icons[f'{sense} head']
            break
        elif f'mhf {sense}' in icons:
            word['icon'] = icons[f'mhf {sense}']
            break
        elif f'raw {sense}' in icons:
            word['icon'] = icons[f'raw {sense}']
            break
        elif f'oak {sense}' in icons:
            word['icon'] = icons[f'oak {sense}']
            break

# Save it as JSON
with open('graph.json', 'w') as f:
    additions = json.load(open(NODE_ADDITIONS))
    graph['nodes'].append(additions)
    json.dump(graph, f, indent=2)