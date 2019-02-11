"""Parse nodes from a given data source."""

import os
import ast
import pickle
import sys
from collections import defaultdict, OrderedDict

def parse_raw_data_to_pickle(infile,outfile):
    """Parse nodes with the given args."""
    print ('Loading pickle file')
    maps = {}
    map_filename="Sample_MAP"
    with open(infile, 'rb') as file_handler:
        data_source = pickle.load(file_handler)

    print ('Pickle load finished')

    node_counts = defaultdict(int)
    samples = []

    OrderedDict(sorted(maps.items(), key=lambda t: t[0]))
    #for key, value in maps.items() :
    #    print("%s<=%s" % (value, key))
    #print (map_filename)

    has_capacity = lambda x: -1 < 0 or node_counts[x] < -1
    can_add_more = lambda: 10000 < 0 or len(samples) < -1

    for item in data_source:
        root = item['tree']
        element = root
        new_samples = [
            {
                'node': element.kind,
                'parent': None,
                'children': [int(x.kind) for x in element.child]
            }
        ]
        gen_samples = lambda x: new_samples.extend(_create_samples(x, maps, map_filename))

        _traverse_tree(element, gen_samples)
        for sample in new_samples:
            if has_capacity(sample['node']):
                samples.append(sample)
                node_counts[sample['node']] += 1
            if not can_add_more:
                break
        if not can_add_more:
            break
    print ('dumping sample')
    #print(samples)
    with open(outfile, 'wb') as file_handler:
        pickle.dump(samples, file_handler)
        file_handler.close()

    print('Total: %d' % sum(node_counts.values()))

def _create_samples(node, maps, map_filename):
    """Convert a node's children into a sample points."""
    samples = []
    for child in node.child:
        if hasattr(child,"child"):
            #for x in child.child:
                #if not x.kind in maps:
                #    maps[x.kind] = len(maps)+1
                #    with open(map_filename, 'wb') as f:
                #        pickle.dump(maps, f, pickle.HIGHEST_PROTOCOL)
                #        f.close()
            try:
                sample = {
                    "node": child.kind,
                    "parent": node.kind,
                    'children': [int(x.kind) for x in child.child]
                }
            except TypeError: #child.child was not iterable
                sample = {
                    "node": child.kind,
                    "parent": node.kind,
                    'children': [int(child.child.kind)]
                }
            samples.append(sample)

    return samples

def _traverse_tree(tree, callback):
    """Traverse a tree and execute the callback on every node."""

    queue = [tree]
    while queue:
        current_node = queue.pop(0)
        if not hasattr(current_node,"child"):
            current_node.child=[]
        children = list(current_node.child)
        queue.extend(children)
        callback(current_node)
        

def _name(node):
    """Get the name of a node."""
    return type(node).__name__


def main():
    from_console=True
    input_path = sys.argv[1] if from_console else "vec"+os.sep+"merged.pkl"
    outfile = sys.argv[2] if from_console else "vec"+os.sep+"nodes.pkl"   
    parse_raw_data_to_pickle(input_path, outfile)


if __name__ == "__main__": 
    main()


    
