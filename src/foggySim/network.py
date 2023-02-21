import networkx as nx


class NetWork:
    Link_Bandwidth = "BW"
    "带宽"

    Link_ChannelDelay = "CD"
    "信道延迟"

    Node_IPT = "IPT"
    "Instructions per simulation time"

    def __init__(self):
        self.G = None
        self.nodeAttributes = {}
        self.NodeID = 0

    def get_edges(self):
        """
        :return: list
        """
        return self.G.edges

    def get_edge(self, key):
        return self.G.edges[key]

    def get_nodes(self):
        return self.G.nodes

    def get_node(self, key):
        return self.G.node[key]

    def size(self):
        return len(self.G.nodes)

    def add_node(self, nodes, edges=None):
        self.NodeID += 1
        self.G.add_node(self.NodeID)
        self.G.add_edges_from(zip(nodes, [self.NodeID] * len(nodes)))

        return self.NodeID

    def remove_node(self, node_id):
        self.G.remove_node(node_id)
        return self.size()

    def load(self, data):
        """
            It generates the topology from a JSON file
            see project example: Tutorial_JSONModelling
            Args:
                 data (str): a json
        """
        self.G = nx.Graph()
        for edge in data["link"]:
            self.G.add_edge(edge["s"], edge["d"], BW=edge[self.Link_Bandwidth], PR=edge[self.Link_ChannelDelay])

        # TODO This part can be removed in next versions
        for node in data["entity"]:
            self.nodeAttributes[node["id"]] = node
        # end remove

        # Correct way to use custom and mandatory topology attributes

        valuesIPT = {}
        # valuesRAM = {}
        for node in data["entity"]:
            try:
                valuesIPT[node["id"]] = node["IPT"]
            except KeyError:
                valuesIPT[node["id"]] = 0
            # try:
            #     valuesRAM[node["id"]] = node["RAM"]
            # except KeyError:
            #     valuesRAM[node["id"]] = 0

        nx.set_node_attributes(self.G, values=valuesIPT, name="IPT")
        # nx.set_node_attributes(self.G,values=valuesRAM,name="RAM")

    def load_all_node_attr(self, data):
        self.G = nx.Graph()
        for edge in data["link"]:
            self.G.add_edge(edge["s"], edge["d"], BW=edge[self.Link_Bandwidth], PR=edge[self.Link_ChannelDelay])

        dc = {str(x): {} for x in data["entity"][0].keys()}
        for ent in data["entity"]:
            for key in ent.keys():
                dc[key][ent["id"]] = ent[key]
        for x in data["entity"][0].keys():
            nx.set_node_attributes(self.G, values=dc[x], name=str(x))

        for node in data["entity"]:
            self.nodeAttributes[node["id"]] = node

        self.NodeID = len(self.G.nodes)

    def find_IDs(self, value):
        keys = list(value.keys())[0]

        result = []
        for key in self.nodeAttributes.keys():
            val = self.nodeAttributes[key]
            if keys in val:
                if value[keys] == val[keys]:
                    result.append(key)
        return result

    def get_nodes_att(self):
        return self.nodeAttributes
