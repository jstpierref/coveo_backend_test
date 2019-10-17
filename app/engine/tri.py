
class TriNode:
    """Base object for building the Tri data structure
    
    Attributes:
        children (dict): hash map to store current TriNode children, if any
        payload (list of tuples): if a given word ends a word, the payload stores 
            the word and its reference primary id in the city table. It is a list
            because a word could potentially have multiple references.
    """
    def __init__(self):
        self.children = {}
        self.payload = []

    def get_children(self):
        return self.children

    def add_child(self, char):
        self.children[char] = TriNode()

    def add_payload(self, element):
        if element not in self.payload:
            self.payload.append(element)

class Tri:
    """The tree-like data structure responsible for fast auto-completion"""
    def __init__(self):
        self.root = TriNode()

    def find_substring_node(self, substring):
        """Gets the node associated to a substring
        Args:
            substring (string): string to autocomplete
        Returns: 
            TriNode if any match, None if it does not exist.
        """
        current_node = self.root
        for char in substring:
            if char in current_node.get_children().keys():
                current_node = current_node.get_children()[char]
            else:
                return None
        return current_node
            
    def add_word(self, reference_id, word):
        """Adds word and its reference id to the tri
    
        Args:
            reference_id (int): city table primary key
            word (string): corresponding word
        """
        current_node = self.root
        last_char = False
        for char in word:
            if char not in current_node.get_children().keys():
                current_node.add_child(char)
            current_node = current_node.get_children()[char]
        current_node.add_payload((reference_id, word))

    def dps_print_from_root(self):
        """Debug method to examine the tri content."""
        def _print(current_node, layer):
            for char, node in current_node.get_children().items():
                print(layer, char, node.payload)
                _print(node, layer+1)
        _print(self.root, 0)

    def dps_traverse(self, node):
        """Given a node, gives all words and their references stored
        in itself and its successors.

        Args:
            node (TriNode)
        """ 
        def _dps_traverse(current_node, total_payload):
            for char, node in current_node.get_children().items():
                if node.payload:
                    total_payload.extend(node.payload)

                total_payload = _dps_traverse(node, total_payload)
            return total_payload
        total_payload = node.payload if node.payload else []
        total_payload = _dps_traverse(node, total_payload)
        return total_payload

    def autocomplete(self, substring):
        """Interface for searching the tri

        Args:
            substring (string)
        """
        node = self.find_substring_node(substring)
        if node:
            return self.dps_traverse(node)
        return []


    def add_words(self, content):
        """Interfarce for populating the tri

        Iteratively adds many words and their reference ids to the tri

        Args:
            content (list): list of tuples with words and reference ids
        """
        for reference_id, word in content:
            self.add_word(reference_id, word)

