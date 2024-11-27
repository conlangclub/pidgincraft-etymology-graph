import csv
import json
import os
from PIL import Image

VOCAB_FILE = 'vocab.csv'
ICONS_DIR = 'invicon/invicon/'
NODE_OVERRIDES = 'node_overrides.json'
NODE_ADDITIONS = 'node_additions.json'

SPRITE_SHEET_OUT = 'spritesheet.png'

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
    if 'icon' in word: continue

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

# Write icons as a sprite sheet, so the web client doesn't have to request every
# single one individually.
# This will cause the node['icon'] to turn into the icon's index in the sprite sheet
icon_nodes = [node for node in graph['nodes'] if 'icon' in node]
sprite_sheet = Image.new('RGBA', (len(icon_nodes)*32, 32))

for i, node in enumerate(icon_nodes):
    icon = Image.open(ICONS_DIR + node['icon'])
    icon = icon.resize((32, 32), resample=Image.Resampling.NEAREST)
    sprite_sheet.paste(icon, (i * 32, 0))
    node['icon'] = i

sprite_sheet.save('./spritesheet.png')

# Save graph as JSON
with open('graph.json', 'w') as f:
    additions = json.load(open(NODE_ADDITIONS))
    graph['nodes'] += additions
    json.dump(graph, f, indent=2)