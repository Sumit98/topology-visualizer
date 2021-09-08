#!/usr/local/bin/python3.7

import os
import json

OUTPUT_TOPOLOGY_FILENAME = 'static/topology.js'
CACHED_TOPOLOGY_FILENAME = 'cached_topology.json'
TOPOLOGY_FILE_HEAD = "\n\nvar topologyData = "

# Topology layers would be sorted
# in the same descending order
# as in the tuple below
# NX_LAYER_SORT_ORDER = (
#     'undefined',
#     'outside',
#     'edge-switch',
#     'edge-router',
#     'core-router',
#     'core-switch',
#     'distribution-router',
#     'distribution-switch',
#     'leaf',
#     'spine',
#     'access-switch'
# )

# icon_capability_map = {
#     'router': 'router',
#     'switch': 'switch',
#     'bridge': 'switch',
#     'station': 'host'
# }


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
    '4461-1': 'router',
    '4461-2': 'router',
    '4461-3': 'router',
    '2911-1': 'router',
    '2911-2': 'router',
    '2911-3': 'router',
    'A9K-1': 'router',
    'N9K-1': 'switch',
}


# interface_full_name_map = {
#     'Eth': 'Ethernet',
#     'Fa': 'FastEthernet',
#     'Gi': 'GigabitEthernet',
#     'Te': 'TenGigabitEthernet',
# }


# def if_fullname(ifname):
#     for k, v in interface_full_name_map.items():
#         if ifname.startswith(v):
#             return ifname
#         if ifname.startswith(k):
#             return ifname.replace(k, v)
#     return ifname


# def if_shortname(ifname):
#     for k, v in interface_full_name_map.items():
#         if ifname.startswith(v):
#             return ifname.replace(v, k)
#     return ifname


def get_icon_type(icon_model_map, key):
 
    if key in icon_model_map.keys():
        icon_type = icon_model_map[key]
        return icon_type
    else:
        return 'unknown'
"""
test_data={

'nodes':
[
{'4461-2': ['10.106.69.78', 'ISR4461/K9']},
{'2911-1': ['10.106.68.134', 'CISCO2911/K9']},
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
{'n1': '2911-3', 'i1': 'Gig 0/2/0', 'n2': 'N9K-1', 'i2': 'Eth 1/36'},
{'n1': '4461-1', 'i1': 'Gig 0/0/2', 'n2': '2911-2', 'i2': 'Gig 0/2'},
{'n1': '4461-1', 'i1': 'Gig 0/0/3', 'n2': 'A9K-1', 'i2': 'Gig 0/1/0/1'},
{'n1': '4461-3', 'i1': 'Gig 0/0/1', 'n2': '2911-2', 'i2': 'Gig 0/1'},
{'n1': '2911-2', 'i1': 'Gig 0/2/0', 'n2': 'A9K-1', 'i2': 'Gig 0/1/0/0'}
]

}
"""
def generate_topology_json(test_data):
    """
    JSON topology object genetator.
    Takes as an input:
    - dict with hostname keys,
    - interconnections list,
    - facts dict with hostname keys.
    """
    topology_dict = {'nodes': [], 'links': []}
    i=0
    host_id=0
    temp_host_id=0
    host_id_map = {}
    for data in test_data['nodes']:
        for i,j in data.items():
            host_id_map[i] = host_id
            topology_dict['nodes'].append({
                'id': host_id,
                'name': i,
                'primaryIP': j[0],
                'model': j[1],
                'icon': get_icon_type(icon_model_map,i)
        })
            temp_host_id = host_id

        host_id += 1
    link_id = 0
    #print(host_id_map)
    for data in test_data['edges']:
        if not (data['n1'] in host_id_map):
            temp_host_id+=1
            topology_dict['nodes'].append({
                'id': temp_host_id,
                'name': data['n1'],
                'primaryIP': "0.0.0.0",
                'model': "Unknown",
                'icon': get_icon_type(icon_model_map,i)
        })
            host_id_map[data['n1']]=temp_host_id
        if not (data['n2'] in host_id_map):
            temp_host_id+=1
            topology_dict['nodes'].append({
                'id': temp_host_id,
                'name': data['n2'],
                'primaryIP': "0.0.0.0",
                'icon': get_icon_type(icon_model_map,i)
        })
            host_id_map[data['n2']]=temp_host_id
        topology_dict['links'].append({
            'id': link_id,
            'source': host_id_map[data['n1']],
            'target': host_id_map[data['n2']],
            'srcIfName': data['i1'],
            'srcDevice': data['n1'],
            'tgtIfName': data['i2'],
            'tgtDevice': data['n2'],
        })
        # print(host_id_map[data['n1']])
        # print(host_id_map[data['n2']])
        link_id += 1
    print(host_id_map)
    return topology_dict


def write_topology_file(topology_json, header=TOPOLOGY_FILE_HEAD, dst=OUTPUT_TOPOLOGY_FILENAME):
    with open(dst, 'w') as topology_file:
        topology_file.write(header)
        topology_file.write(json.dumps(topology_json, indent=4, sort_keys=True))
        topology_file.write(';')


def write_topology_cache(topology_json, dst=CACHED_TOPOLOGY_FILENAME):
    with open(dst, 'w') as cached_file:
        cached_file.write(json.dumps(topology_json, indent=4, sort_keys=True))


def read_cached_topology(filename=CACHED_TOPOLOGY_FILENAME):
    if not os.path.exists(filename):
        return {}
    if not os.path.isfile(filename):
        return {}
    cached_topology = {}
    with open(filename, 'r') as file:
        try:
            cached_topology = json.loads(file.read())
        except ValueError as err:
            print(f"Failed to read cache from {filename}: {err}")
            return {}
        except Exception as err:
            print(f"Failed to read cache from {filename}: {err}")
            return {}
    return cached_topology


# def get_topology_diff(cached, current):
#     """
#     Topology diff analyzer and generator.
#     Accepts two valid topology dicts as an input.
#     Returns:
#     - dict with added and deleted nodes,
#     - dict with added and deleted links,
#     - dict with merged input topologies with extended
#       attributes for topology changes visualization
#     """
#     diff_nodes = {'added': [], 'deleted': []}
#     diff_links = {'added': [], 'deleted': []}
#     diff_merged_topology = {'nodes': [], 'links': []}
#     # Parse links from topology dicts into the following format:
#     # (topology_link_obj, (source_hostnme, source_port), (dest_hostname, dest_port))
#     cached_links = [(x, ((x['srcDevice'], x['srcIfName']), (x['tgtDevice'], x['tgtIfName']))) for x in cached['links']]
#     links = [(x, ((x['srcDevice'], x['srcIfName']), (x['tgtDevice'], x['tgtIfName']))) for x in current['links']]
#     # Parse nodes from topology dicts into the following format:
#     # (topology_node_obj, (hostname,))
#     # Some additional values might be added for comparison later on to the tuple above.
#     cached_nodes = [(x, (x['name'],)) for x in cached['nodes']]
#     nodes = [(x, (x['name'],)) for x in current['nodes']]
#     # Search for deleted and added hostnames.
#     node_id = 0
#     host_id_map = {}
#     for raw_data, node in nodes:
#         if node in [x[1] for x in cached_nodes]:
#             raw_data['id'] = node_id
#             host_id_map[raw_data['name']] = node_id
#             raw_data['is_new'] = 'no'
#             raw_data['is_dead'] = 'no'
#             diff_merged_topology['nodes'].append(raw_data)
#             node_id += 1
#             continue
#         diff_nodes['added'].append(node)
#         raw_data['id'] = node_id
#         host_id_map[raw_data['name']] = node_id
#         raw_data['is_new'] = 'yes'
#         raw_data['is_dead'] = 'no'
#         diff_merged_topology['nodes'].append(raw_data)
#         node_id += 1
#     for raw_data, cached_node in cached_nodes:
#         if cached_node in [x[1] for x in nodes]:
#             continue
#         diff_nodes['deleted'].append(cached_node)
#         raw_data['id'] = node_id
#         host_id_map[raw_data['name']] = node_id
#         raw_data['is_new'] = 'no'
#         raw_data['is_dead'] = 'yes'
#         raw_data['icon'] = 'dead_node'
#         diff_merged_topology['nodes'].append(raw_data)
#         node_id += 1
#     # Search for deleted and added interconnections.
#     # Interface change on some side is consideres as
#     # one interconnection deletion and one interconnection insertion.
#     # Check for permutations as well:
#     # ((h1, Gi1), (h2, Gi2)) and ((h2, Gi2), (h1, Gi1)) are equal.
#     link_id = 0
#     for raw_data, link in links:
#         src, dst = link
#         if not (src, dst) in [x[1] for x in cached_links] and not (dst, src) in [x[1] for x in cached_links]:
#             diff_links['added'].append((src, dst))
#             raw_data['id'] = link_id
#             link_id += 1
#             raw_data['source'] = host_id_map[src[0]]
#             raw_data['target'] = host_id_map[dst[0]]
#             raw_data['is_new'] = 'yes'
#             raw_data['is_dead'] = 'no'
#             diff_merged_topology['links'].append(raw_data)
#             continue
#         raw_data['id'] = link_id
#         link_id += 1
#         raw_data['source'] = host_id_map[src[0]]
#         raw_data['target'] = host_id_map[dst[0]]
#         raw_data['is_new'] = 'no'
#         raw_data['is_dead'] = 'no'
#         diff_merged_topology['links'].append(raw_data)
#     for raw_data, link in cached_links:
#         src, dst = link
#         if not (src, dst) in [x[1] for x in links] and not (dst, src) in [x[1] for x in links]:
#             diff_links['deleted'].append((src, dst))
#             raw_data['id'] = link_id
#             link_id += 1
#             raw_data['source'] = host_id_map[src[0]]
#             raw_data['target'] = host_id_map[dst[0]]
#             raw_data['is_new'] = 'no'
#             raw_data['is_dead'] = 'yes'
#             diff_merged_topology['links'].append(raw_data)
#     return diff_nodes, diff_links, diff_merged_topology


# def topology_is_changed(diff_result):
#     diff_nodes, diff_links, *ignore = diff_result
#     changed = (
#         diff_nodes['added']
#         or diff_nodes['deleted']
#         or diff_links['added']
#         or diff_links['deleted']
#     )
#     if changed:
#         return True
#     return False


# def print_diff(diff_result):
#     """
#     Formatted get_topology_diff result
#     console print function.
#     """
#     diff_nodes, diff_links, *ignore = diff_result
#     if not (diff_nodes['added'] or diff_nodes['deleted'] or diff_links['added'] or diff_links['deleted']):
#         print('No topology changes since last run.')
#         return
#     print('Topology changes have been discovered:')
#     if diff_nodes['added']:
#         print('')
#         print('^^^^^^^^^^^^^^^^^^^^')
#         print('New Network Devices:')
#         print('vvvvvvvvvvvvvvvvvvvv')
#         for node in diff_nodes['added']:
#             print(f'Hostname: {node[0]}')
#     if diff_nodes['deleted']:
#         print('')
#         print('^^^^^^^^^^^^^^^^^^^^^^^^')
#         print('Deleted Network Devices:')
#         print('vvvvvvvvvvvvvvvvvvvvvvvv')
#         for node in diff_nodes['deleted']:
#             print(f'Hostname: {node[0]}')
#     if diff_links['added']:
#         print('')
#         print('^^^^^^^^^^^^^^^^^^^^^^')
#         print('New Interconnections:')
#         print('vvvvvvvvvvvvvvvvvvvvvv')
#         for src, dst in diff_links['added']:
#             print(f'From {src[0]}({src[1]}) To {dst[0]}({dst[1]})')
#     if diff_links['deleted']:
#         print('')
#         print('^^^^^^^^^^^^^^^^^^^^^^^^^')
#         print('Deleted Interconnections:')
#         print('vvvvvvvvvvvvvvvvvvvvvvvvv')
#         for src, dst in diff_links['deleted']:
#             print(f'From {src[0]}({src[1]}) To {dst[0]}({dst[1]})')
#     print('')

"""
def good_luck_have_fun():
    ""\"Main script logic\"""
    TOPOLOGY_DICT = generate_topology_json()
    CACHED_TOPOLOGY = read_cached_topology()
    write_topology_file(TOPOLOGY_DICT)
    write_topology_cache(TOPOLOGY_DICT)
    print('Open main.html in a project root with your browser to view the topology')
    # if CACHED_TOPOLOGY:
    #     DIFF_DATA = get_topology_diff(CACHED_TOPOLOGY, TOPOLOGY_DICT)
    #     print_diff(DIFF_DATA)
    #     write_topology_file(DIFF_DATA[2], dst='diff_topology.js')
    #     if topology_is_changed:
    #         print('Open diff_page.html in a project root to view the changes.')
    #         print("Optionally, open main.html and click 'Display diff' button")
    # else:
    #     # write current topology to diff file if the cache is missing
    #     write_topology_file(TOPOLOGY_DICT, dst='diff_topology.js')


if __name__ == '__main__':
    good_luck_have_fun()
"""
