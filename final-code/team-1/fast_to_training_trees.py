"""Parse trees from a data source."""
import ast
import sys
import pickle
import random
import os
from collections import defaultdict

def parse_pickle_to_training_trees(infile,outfile):
    """Parse trees with the given arguments."""
    print ('Loading pickle file')

    sys.setrecursionlimit(1000000)
    with open(infile, 'rb') as file_handler:
        data_source = pickle.load(file_handler)

    print('Pickle file load finished')

    train_samples = []
    test_samples = []

    train_counts = defaultdict(int)
    test_counts = defaultdict(int)
    for item in data_source:

        tree = item['tree']
        label = item['metadata']["label"]
        root = tree
        sample, size = _traverse_tree(root)
        
        if size > 10000 or size < 10: #normal was 50
            continue

        roll = random.randint(0, 100)

        datum = {'tree': sample, 'label': label}

        if roll < 30:
            test_samples.append(datum)
            test_counts[label] += 1
        else:
            train_samples.append(datum)
            train_counts[label] += 1

    random.shuffle(train_samples)
    random.shuffle(test_samples)

    # create a list of unique labels in the data
    #labels = list(set(train_counts.keys() , test_counts.keys()))
    labels = list(set(["valid"] + ["invalid"]))


    print('Dumping sample')
    with open(outfile, 'wb') as file_handler:
        pickle.dump((train_samples, test_samples, labels), file_handler)
        file_handler.close()
    print('dump finished')
    print('Sampled tree counts: ')
    print('Training:', train_counts)
    print('Testing:', test_counts)

def _traverse_tree(root):
    num_nodes = 1
    queue = [root]

    root_json = {
        "node": str(root.kind),

        "children": []
    }
    queue_json = [root_json]
    while queue:
      
        current_node = queue.pop(0)
        num_nodes += 1
        # print (_name(current_node))
        current_node_json = queue_json.pop(0)


        children = [x for x in current_node.child]
        queue.extend(children)
       
        for child in children:
            # print "##################"
            #print child.kind

            child_json = {
                "node": str(child.kind),
                "children": []
            }

            current_node_json['children'].append(child_json)
            queue_json.append(child_json)
            # print current_node_json
  
    return root_json, num_nodes

def main():
    from_console=True
    input_path = sys.argv[1] if from_console else "vec"+os.sep+"merged.pkl"
    outfile = sys.argv[2] if from_console else "vec"+os.sep+"trees.pkl"   
    parse_pickle_to_training_trees(input_path,outfile)


if __name__ == "__main__": 
    main()


    
