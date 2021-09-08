icon_model_map = {
    'CSR1000V': 'router',
    'Nexus': 'switch',
    'IOSXRv': 'router',
    'IOSv': 'switch',
    '2901': 'router',
    '2921': 'router',
    '2951': 'router',
    '4321': 'router',
    '4331': 'router',
    '4351': 'router',
    '4421': 'router',
    '4431': 'router',
    '4451': 'router',
    '2960': 'switch',
    '3750': 'switch',
    '3850': 'switch',
    '4461-1': 'switch',
    '4461-2': 'switch',
    '4461-3': 'switch',
    '2911-1': 'switch',
    '2911-2': 'switch',
    '2911-3': 'router',
    'A9K-1': 'switch',
    'N9K-1': 'switch',
}

test_data={

'nodes':
[
{'2911-3': ['10.106.71.192', 'CISCO2911/K9']},
{'4461-1': ['10.106.68.132', 'ISR4461/K9']},
{'A9K-1': ['10.106.49.6', 'ASR9K']},
{'4461-3': ['10.106.68.135', 'ISR4461/K9']},
{'2911-2': ['10.106.69.22', 'CISCO2911/K9']},
{'N9K-1': ['10.106.71.26', 'Nexus9000 C9336C-FX2-E Chassis']}
],

'edges':
[
{'n1': '4461-2', 'i1': 'Gig 0/0/3', 'n2': '2911-3', 'i2': 'Gig 0/2'},
{'n1': '4461-2', 'i1': 'Gig 0/0/2', 'n2': '2911-1', 'i2': 'Gig 0/1'},
{'n1': '4461-2', 'i1': 'Gig 0/0/1', 'n2': 'N9K-1', 'i2': 'Eth 1/18'},
{'n1': '2911-1', 'i1': 'Gig 0/2', 'n2': '4461-3', 'i2': 'Gig 0/0/0'},
{'n1': '2911-1', 'i1': 'Gig 0/2/0', 'n2': '4461-1', 'i2': 'Gig 0/0/0'},
{'n1': '2911-3', 'i1': 'Gig 0/1', 'n2': '4461-3', 'i2': 'Gig 0/0/2'},
{'n1': '2911-3', 'i1': 'Gig 1/0', 'n2': '2900-4', 'i2': 'Gig 0/18'},
{'n1': '2911-3', 'i1': 'Gig 1/1', 'n2': '2900-4', 'i2': 'Gig 0/17'},
{'n1': '2911-3', 'i1': 'Gig 0/2/0', 'n2': 'N9K-1', 'i2': 'Eth 1/36'},
{'n1': '4461-1', 'i1': 'Gig 0/0/2', 'n2': '2911-2', 'i2': 'Gig 0/2'},
{'n1': '4461-1', 'i1': 'Gig 0/0/3', 'n2': 'A9K-1', 'i2': 'Gig 0/1/0/1'},
{'n1': '4461-3', 'i1': 'Gig 0/0/1', 'n2': '2911-2', 'i2': 'Gig 0/1'},
{'n1': '2911-2', 'i1': 'Gig 0/2/0', 'n2': 'A9K-1', 'i2': 'Gig 0/1/0/0'}
]

}

# print(test_data['nodes'][0]['4461-2'][1])
# print(test_data['edges'][0]['n1'])

# for data in test_data['edges']:
#     print("Source: "+ data['n1'])
#     print("Destination: "+ data['n2'])
#     print("Source Interface: "+ data['i1'])
#     print("Destination Interface: "+ data['i2'])
    
def get_icon_type(icon_model_map, key):
 
    if key in icon_model_map.keys():
        icon_type = icon_model_map[key]
        return icon_type
    else:
        return 'unknown'

for data in test_data['nodes']:
    for i,j in data.items():
         print("Name: "+ i)
         print("Type: "+ get_icon_type(icon_model_map,i))

    
    