import graphviz
import pandas as pd
import textwrap
from dataclasses import dataclass

ORANGE = '#ff9966'
RED = '#ffad99'
GREEN = '#99ff99'
BLUE = '#ccd9ff'

data = pd.read_csv("C:\\Users\\dimpd\Downloads\\Jira.csv")

# Create a Graphviz Digraph
dot = graphviz.Digraph(format='png')

# Set the rankdir attribute for the whole graph (default is TB)
dot.attr(rankdir='TB')

@dataclass
class Attibute:
    name : str
    attribute_type : str

    def __hash__(self) -> int:
        return hash((self.name, self.attribute_type))

    
class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.attributes = set()

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

root = Node("root")
nodes = {}
nodes['root'] = root

def add_persona(issue_id, persona):
    # Create a subgraph for nodes 2 and 3 to be positioned to the right
    with dot.subgraph() as s:
        s.attr(rank='same')  # Set layout direction for this subgraph
        s.node(persona + issue_id, label=persona, image='./person.png', shape='none', imagescale='true', fixedsize='true', width='1', height='1', labelloc='b')
        s.node(issue_id)
        s.edge(persona + issue_id, issue_id, style='invis')

def add_be(issue_id, be):
    # Create a subgraph for nodes 2 and 3 to be positioned to the right
    with dot.subgraph() as s:
        s.attr(rank='same')  # Set layout direction for this subgraph
        s.attr(rankdir='RL')
        s.node(issue_id)
        s.node(be + issue_id, label=be, image='./cloud.png', shape='none', imagescale='true', fixedsize='true', width='1', height='1')
        s.edge(be + issue_id, issue_id, style='invis')

def add_feel(issue_id, feel):
    # Create a subgraph for nodes 2 and 3 to be positioned to the right
    with dot.subgraph() as s:
        s.attr(rank='same')  # Set layout direction for this subgraph
        s.node(issue_id)
        s.node(feel + issue_id, label=feel, image='./heart.png', shape='none', imagescale='true', fixedsize='true', width='1', height='1')
        s.edge(feel + issue_id, issue_id, style='invis')

def add_attributes_recurse(node): 
    children = node.children
    for child in children:
        add_attributes_recurse(child)

    for attribute in node.attributes:
        if attribute.attribute_type == 'persona':
            add_persona(node.name, attribute.name)
        elif attribute.attribute_type == 'be':
            add_be(node.name, attribute.name)
        elif attribute.attribute_type == 'feel':
            add_feel(node.name, attribute.name)
        


def getColour(issue):
    if issue['Priority'] == "High":
        return RED
    elif issue['Priority'] == "Medium":
        return ORANGE
    elif issue['Priority'] == "Low":
        return GREEN
    

# Add nodes and edges
dot.node('root', shape='parallelogram', label="Distributed Agent\nSimulator", color=BLUE, style='filled', fixedsize='true', width='2', height='1.2')
#from data filter rows where Issue Type = Epic
epics = data[data['Issue Type'] == 'Epic']
for index, epic in epics.iterrows():
    dot.node(str(epic["Issue id"]), label=epic["Summary"], shape='parallelogram', style='filled', fillcolor=getColour(epic))
    dot.edge('root', str(epic["Issue id"]))
    
    node = Node(str(epic["Issue id"]))
    root.add_child(node)
    nodes[str(epic["Issue id"])] = node

    
#user stories
user_stories = data[data['Issue Type'] == 'Story']
for index, user_story in user_stories.iterrows():
    summary = user_story["Summary"]
    
    I_WANT_TO = 'I want to'
    I_WANT_IT_TO_BE = 'I want it to be'
    I_WANT_TO_FEEL = 'I want to feel'
    
    SO_THAT = 'so that'
    AS_A = 'As a'

    if I_WANT_TO_FEEL in summary:
        i_want = I_WANT_TO_FEEL
    elif I_WANT_TO in summary:
        i_want = I_WANT_TO
    elif I_WANT_IT_TO_BE in summary:
        i_want = I_WANT_IT_TO_BE

    description = summary.split(i_want)[1]
    description = description.split(SO_THAT)[0]
    persona = summary.split(AS_A)[1]
    persona = persona.split(i_want)[0].strip()

    if I_WANT_TO == i_want:
        label = textwrap.fill(description, 15)    
        dot.node(str(user_story["Issue id"]), label=label, shape='parallelogram', style='filled', fillcolor=getColour(user_story), height='1.2', width='2', fixedsize='true')
        node = Node(str(user_story["Issue id"]))
        nodes[str(int(user_story["Parent"]))].add_child(node)
        nodes[str(user_story["Issue id"])] = node
        node.add_attribute(Attibute(persona, "persona"))
        dot.edge(str(int(user_story["Parent"])), str(user_story["Issue id"]))
    elif I_WANT_IT_TO_BE == i_want:
        # be stories are attributes of parent
        node = nodes[str(int(user_story["Parent"]))]
        node.add_attribute(Attibute(description, "be"))
    else:
        # feel stories are attributes of parent
        node = nodes[str(int(user_story["Parent"]))]
        node.add_attribute(Attibute(description, "feel"))
    

root.bubble_up_attributes()
# add persona
add_attributes_recurse(root)

# Render the tree to a file
dot.render('icon_tree_custom_layout', view=True)
