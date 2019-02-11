import pickle
import types
import sys
import os

node_map={}
PATH_SEPERATOR="/"
def build_childs_for(kind,info=""):
    global node_map
    curr = types.SimpleNamespace()
    curr.child=[]
    
    if kind not in node_map:
        node_map[kind]=len(node_map)+1

    #curr.kind=kind

    if kind == "Declare":
        curr.child.append(build_childs_for("Var",info["Var"]))
        curr.child.append(build_childs_for("SecurityClass",info["Label"]))
    
    elif kind == "While":
        curr.child.append(build_childs_for("Condition",info["Condition"]))
        curr.child.append(build_childs_for("Body",info["Body"]))

    elif kind == "Condition":
        curr.child.append(build_childs_for(info["Kind"],info))

    elif kind == "Body":
        curr.child.append(build_childs_for(info["Kind"],info))
        info=""#

    elif kind == "If":
        curr.child.append(build_childs_for("Condition",info["Condition"]))
        curr.child.append(build_childs_for("Then",info["Then"]))
        curr.child.append(build_childs_for("Else",info["Else"]))

    elif kind == "Then":
        curr.child.append(build_childs_for(info["Kind"],info))
        info=""#
    
    elif kind == "Else":
        curr.child.append(build_childs_for(info["Kind"],info))
        info=""#

    elif kind == "Var":
        if isinstance(info,str): #check if instance is called by a declare statement
            curr.child.append(build_childs_for(info))
        else:
            curr.child.append(build_childs_for(info["Name"]))

    elif kind == "SecurityClass":
        curr.child.append(build_childs_for(info))

    else:
        #print("no special kind:",kind)
        curr.kind=kind

    if "Left" in info:
        curr.child.append(build_childs_for(info["Left"]["Kind"],info["Left"]))
        curr.child.append(build_childs_for(info["Right"]["Kind"],info["Right"]))
    
    curr.kind = node_map[kind]
    return curr     



def build_merged_ast(data_directory):
    result = []
    for root,d,files in os.walk(data_directory):
        for file in files:
            try:
                file_path = os.path.join(root,file)
                splits = file_path.split(PATH_SEPERATOR)
                label = splits[len(splits)-3]
                with open(file_path,"rb") as f:
                    ast_representation = pickle.load(f)
                newAST = build_childs_for("Seq",ast_representation)
                result.append({
                    'tree': newAST, 'metadata': {'label': label}
                })
            except Exception as err:
                print (err)
    return result    


def main():
    from_console=True
    input_path = sys.argv[1] if from_console else "PICKLE"
    outfile = sys.argv[2] if from_console else "merged.pkl"   
    merged_ast = build_merged_ast(input_path)

    path_current = os.path.dirname(os.path.realpath(__file__))
    path_current = os.path.join(path_current,"vec")
    if not os.path.isdir(path_current):
        os.makedirs(path_current,0o777)

    path_current = os.path.join(path_current,outfile)

    with open(path_current, 'wb') as file_handler:
        pickle.dump(merged_ast, file_handler)
    with open(path_current+"_map",'wb') as f:
        pickle.dump(node_map,f)

if __name__ == "__main__":
    main()


