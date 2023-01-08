import json
import time

import branch
import copy


class NodeInfo:
    def __init__(self, name):
        self.name = name
        self.identifier = 0
        self.identifier = hash(self)
        print(self.name + ":" + str(self.identifier))

    def get_node_info_hash(self):
        return self.identifier


class Node:
    ###
    # @node_name: node name
    # @father_node_name: list of father nodes' name
    # @son_node_name: list of son nodes' name
    ###
    def __init__(self, node_name, father_node_name, son_node_name):
        self.node_info = NodeInfo(node_name)
        self.father_node_name_list = []
        self.son_node_name_list = []
        self.sub_plot = branch.SubPlot(node_name, [], 0, [10, 10])

        if isinstance(father_node_name, list):
            for itr in father_node_name:
                self.father_node_name_list.append(itr)
            self.number_of_father = len(self.father_node_name_list)
        elif isinstance(father_node_name, str):
            self.father_node_name_list.append(father_node_name)
            self.number_of_father = len(self.father_node_name_list)
        elif father_node_name is None:
            self.number_of_father = 0
        else:
            print("Error father_node_name")

        if isinstance(son_node_name, list):
            for itr in son_node_name:
                if isinstance(itr, dict):
                    temp_key = itr.keys()
                    for key_itr in temp_key:
                        self.son_node_name_list.append(key_itr)
                elif isinstance(itr, str):
                    self.son_node_name_list.append(itr)
                else:
                    print("Error son node name type")
            self.number_of_son = len(self.son_node_name_list)
        elif isinstance(son_node_name, str):
            self.son_node_name_list.append(son_node_name)
            self.number_of_son = len(self.son_node_name_list)
        elif son_node_name is None:
            self.number_of_son = 0
        else:
            print("Error son_node_name")

    def get_node_hash(self):
        return self.node_info.get_node_info_hash()

    def add_son_node(self, son_node):
        self.son_node_name_list = self.son_node_name_list.append(son_node)
        self.number_of_son += len(son_node)
        print(self.node_info.name + "@" + self.node_info.identifier)
        print("Add " + str(len(son_node)) + "son nodes")
        print(son_node)

    def add_father_node(self, father_node):
        self.father_node_name_list = self.father_node_name_list.append(father_node)
        self.number_of_father += len(father_node)
        print(self.node_info.name + "@" + self.node_info.identifier)
        print("Add " + str(len(father_node)) + "father nodes")
        print(father_node)


class Tree:
    def __init__(self, file_name):
        with open(file_name, 'r') as file:
            self.json_data = json.load(file)
            self.node_list = []
            print(self.json_data)
        self.build()
        self.route = [self.node_list[0]]
        self.branch_start = self.node_list[0]
        self.branch_end = self.node_list[0]
        self.cursor = self.node_list[0]
        self.analyser = branch.Analyser()
        self.connect_tree = copy.deepcopy(self.node_list)

    def build(self):
        if len(self.json_data.keys()) == 0:
            print("No Node")
        else:
            self.analyse_dict(None, self.json_data)

    def analyse_dict(self, father_key, dict_node):
        for key in dict_node.keys():
            if isinstance(dict_node[key], dict):
                temp = dict_node[key].keys()
                self.node_list.append(Node(str(key), father_key, list(dict_node[key].keys())))
                self.analyse_dict(key, dict_node[key])
            else:
                self.node_list.append(Node(str(key), father_key, dict_node[key]))
                for node in dict_node[key]:
                    if isinstance(node, dict):
                        # for key_s in node.keys():
                        #     self.node_list.append(Node(str(key_s), str(key), node[key_s]))
                        self.analyse_dict(key, node)
                    else:
                        self.node_list.append(Node(str(node), str(key), None))


if __name__ == "__main__":
    start = time.time()
    test_tree = Tree("./tree.json")
    end = time.time()

    print(end - start)
    print(test_tree)
