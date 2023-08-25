import textwrap
import graphviz

ORANGE = '#ff9966'
RED = '#ffad99'
GREEN = '#99ff99'
BLUE = '#ccd9ff'

def create_dot_graph(root):
    # Create a Graphviz Digraph
    dot = graphviz.Digraph(format='png')

    # Set the rankdir attribute for the whole graph (default is TB)
    create_main_graph(None, root, dot)
    add_attributes_recurse(root, dot)

    # Render the tree to a file
    dot.render('icon_tree_custom_layout', view=True)


def create_main_graph(parent, node, dot):
    add_do(parent, node,dot)

    for child in node.children:
        create_main_graph(node, child, dot)


def add_persona(issue_id, persona, dot):
    # Create a subgraph for nodes 2 and 3 to be positioned to the right
    with dot.subgraph() as s:
        s.attr(rank='same')  # Set layout direction for this subgraph
        s.node(persona + issue_id, label=persona, image='./person.png', shape='none', imagescale='true', fixedsize='true', width='1', height='1', labelloc='b')
        s.node(issue_id)
        s.edge(persona + issue_id, issue_id, style='invis')

def add_be(issue_id, be, dot):
    # Create a subgraph for nodes 2 and 3 to be positioned to the right
    with dot.subgraph() as s:
        s.attr(rank='same')  # Set layout direction for this subgraph
        s.attr(rankdir='RL')
        s.node(issue_id)
        s.node(be + issue_id, label=be, image='./cloud.png', shape='none', imagescale='true', fixedsize='true', width='1', height='1')
        s.edge(be + issue_id, issue_id, style='invis')

def add_feel(issue_id, feel, dot):
    # Create a subgraph for nodes 2 and 3 to be positioned to the right
    with dot.subgraph() as s:
        s.attr(rank='same')  # Set layout direction for this subgraph
        s.node(issue_id)
        s.node(feel + issue_id, label=feel, image='./heart.png', shape='none', imagescale='true', fixedsize='true', width='1', height='1')
        s.edge(feel + issue_id, issue_id, style='invis')

def add_do(parent, node, dot):
    issue_id = node.name
    issue = node.issue
    label = textwrap.fill(node.label, 15)    
    dot.node(issue_id, label=label, shape='parallelogram', style='filled', fillcolor=getColour(issue), height='1.2', width='2', fixedsize='true')
    if parent is not None:
        dot.edge(parent.name, issue_id)

def add_attributes_recurse(node, dot): 
    children = node.children
    for child in children:
        add_attributes_recurse(child, dot)

    for attribute in node.attributes:
        if attribute.attribute_type == 'persona':
            add_persona(node.name, attribute.name, dot)
        elif attribute.attribute_type == 'be':
            add_be(node.name, attribute.name, dot)
        elif attribute.attribute_type == 'feel':
            add_feel(node.name, attribute.name, dot)
        


def getColour(issue):
    if issue is None: 
        return BLUE
    elif issue['Priority'] == "High":
        return RED
    elif issue['Priority'] == "Medium":
        return ORANGE
    elif issue['Priority'] == "Low":
        return GREEN