


class Node:
    def __init__(self):
        self.children = {}
        self.payload = None

    def get_children(self):
        return self.children

    def add_child(self, char):
        self.children[char] = Node()

    def add_payload(self, element):
        self.payload = element


class Tri:
    def __init__(self):
        self.root = Node()

    def find_substring_node(self, substring):
        current_node = self.root
        for i, char in enumerate(substring):
            if char in current_node.get_children().keys():
                current_node = current_node.get_children()[char]
            else:
                return None

    def add_word(self, engine_idx, word):
        current_node = self.root
        last_char = False
        for i, char in enumerate(word):

            if char not in current_node.get_children().keys():
                current_node.add_child(char)

            current_node = current_node.get_children()[char]
        current_node.add_payload(engine_idx)

    def dps_print_from_root(self):
        def _print(current_node, layer):
            for char, node in current_node.get_children().items():
                print(layer, char, node.payload)
                _print(node, layer+1)

        _print(self.root, 0)

    def dps_traverse(self, node):
        def _dps_traverse(current_node, table_elements):
            for char, node in current_node.get_children().items():
                if node.payload:
                    table_elements.append(node.payload)
                table_elements = _dps_traverse(node, table_elements)
            return table_elements
        table_elements = [node.payload] if node.payload else []
        table_elements = _dps_traverse(node, table_elements)
        return table_elements

    def get_table_elements(self, substring):
        node = self.find_substring_node(substring)
        if node:
            return self.dps_traverse(node)
        return []

tri = Tri()
tri.add_word(1, "test")
tri.add_word(2, "tester")
tri.add_word(3, "team")

print(tri.get_table_elements("test"))
