import pickle
import types
import sys

node_map={}

def build_childs_for(kind,info=""):
    global node_map
    curr = types.SimpleNamespace()
    curr.child=[]
    
    if kind not in node_map:
        node_map[kind]=len(node_map)+1

    curr.kind = node_map[kind]
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
        print("no special kind:",kind)
        curr.kind=kind

    if "Left" in info:
        curr.child.append(build_childs_for(info["Left"]["Kind"],info["Left"]))
        curr.child.append(build_childs_for(info["Right"]["Kind"],info["Right"]))
    
    return curr     



def main():
    print("Try to open file: ", sys.argv[1] )
    with open(sys.argv[1], 'rb') as fh:
            astobj = pickle.load(fh)

    asts=[]
    ast={}
    ast["tree"]=types.SimpleNamespace()
    ast['tree'].element=build_childs_for("Seq",astobj)

    ast["metadata"]=types.SimpleNamespace()
    ast["metadata"].label="invalid/valid"

    asts.append(ast)
    print(node_map)
    print("----------------")
    print(asts)
    print("----------------")

    print("Try to write file: ", sys.argv[2] )
    with open(sys.argv[2], 'wb') as f:
        pickle.dump((asts,node_map), f, pickle.HIGHEST_PROTOCOL)
        f.close()
    print("Sucessfully")
if __name__ == "__main__":
    main()
