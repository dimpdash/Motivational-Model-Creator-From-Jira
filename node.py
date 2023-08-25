from dataclasses import dataclass

@dataclass
class Attibute:
    name : str
    attribute_type : str

    def __hash__(self) -> int:
        return hash((self.name, self.attribute_type))

    
class Node:
    def __init__(self, name, issue=None, label=None):
        if label is None:
            self.label = name
        self.name = name
        self.children = []
        self.attributes = set()
        self.issue = issue
        self.label = label

    def add_child(self, obj):
        self.children.append(obj)

    def add_attribute(self, attribute):
        self.attributes.add(attribute)

    def bubble_up_attributes(self):
        children = self.children
        for child in children:
            child.bubble_up_attributes()

        # once bubbled up consider at this level
        if len(children) == 0:
            common_attributes = set()
        else:
            common_attributes = children[0].attributes
        for child in children:
            common_attributes = common_attributes.intersection(child.attributes)
        
        # remove common attributes from children
        for child in children:
            child.attributes = child.attributes.difference(common_attributes)

        self.attributes = self.attributes.union(common_attributes) 