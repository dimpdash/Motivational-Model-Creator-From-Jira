import graphviz
import pandas as pd
import textwrap

data = pd.read_csv("C:\\Users\\dimpd\Downloads\\Jira.csv")

# Create a Graphviz Digraph
dot = graphviz.Digraph(format='png')

# Set the rankdir attribute for the whole graph (default is TB)
dot.attr(rankdir='TB')

class Node:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.persona = None

    def add_child(self, obj):
        print(self.name, obj.name)
        self.children.append(obj)

root = Node("root")
nodes = {}
nodes['root'] = root

def add_persona(issue_id, persona):
    # Create a subgraph for nodes 2 and 3 to be positioned to the right
    with dot.subgraph() as s:
        s.attr(rank='same')  # Set layout direction for this subgraph
        s.node(issue_id)
        s.node(persona + issue_id, label=persona, image='./person.png', shape='none', imagescale='true', fixedsize='true', width='1', height='0.8', labelloc='t')
        s.edge(persona, issue_id, style='invis')

def add_person_recurse(node): 
    children = node.children
    for child in children:
        add_person_recurse(child)

    if node.persona is not None:
        add_persona(node.name, node.persona)

def getColour(issue):
    if issue['Priority'] == "High":
        return "red1"
    elif issue['Priority'] == "Medium":
        return "orange1"
    elif issue['Priority'] == "Low":
        return "green1"
    
# Add nodes and edges
dot.node('1', label='1 (Root)', shape='none', image='path/to/root_icon.png')
#from data filter rows where Issue Type = Epic
epics = data[data['Issue Type'] == 'Epic']
for index, epic in epics.iterrows():
    dot.node(str(epic["Issue id"]), label=epic["Summary"], shape='parallelogram', style='filled', fillcolor=getColour(epic))
    dot.edge('1', str(epic["Issue id"]))
    
    node = Node(str(epic["Issue id"]))
    root.add_child(node)
    nodes[str(epic["Issue id"])] = node

    
#user stories
user_stories = data[data['Issue Type'] == 'Story']
for index, user_story in user_stories.iterrows():
    summary = user_story["Summary"]
    description = summary.split("I want to")[1]
    description = description.split("so that")[0]
    persona = summary.split("As a")[1]
    persona = persona.split("I want to")[0]
    
    dot.node(str(user_story["Issue id"]), label=textwrap.fill(description, 15), shape='parallelogram', style='filled', fillcolor=getColour(user_story))

    node = Node(str(user_story["Issue id"]))
    nodes[str(int(user_story["Parent"]))].add_child(node)
    nodes[str(user_story["Issue id"])] = node
    node.persona = persona
    
    print(str(user_story["Parent"]))
    dot.edge(str(int(user_story["Parent"])), str(user_story["Issue id"]))

def bubble_up_persona(node):
    children = node.children
    for child in children:
        bubble_up_persona(child)

    # once bubbled up consider at this level
    personas = set()
    for child in children:
        personas.add(child.persona)
    
    if len(personas) == 1:
        node.persona = persona
    
        for child in children:
            child.persona = None

bubble_up_persona(root)
# add persona
add_person_recurse(root)

# Render the tree to a file
dot.render('icon_tree_custom_layout', view=True)
