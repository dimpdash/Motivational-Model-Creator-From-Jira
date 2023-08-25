import pandas as pd
from node import Node, Attibute
from dot_graph import create_dot_graph

def create_motivational_model_controller(project_name, filepath):
    data = pd.read_csv(filepath)

    root = Node("root", None, project_name)
    nodes = {}
    nodes['root'] = root

    # Add nodes and edges
    #from data filter rows where Issue Type = Epic
    epics = data[data['Issue Type'] == 'Epic']
    for index, epic in epics.iterrows():
        node_id = str(epic["Issue id"])
        label = epic["Summary"]
        node = Node(node_id, epic, label=label)
        root.add_child(node)
        nodes[node_id] = node

    #user stories
    user_stories = data[data['Issue Type'] == 'Story']
    for index, user_story in user_stories.iterrows():
        summary = user_story["Summary"]
        parent_id = str(int(user_story["Parent"]))
        node_id = str(user_story["Issue id"])

        
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
            node = Node(node_id, user_story, label=description)
            nodes[parent_id].add_child(node)
            nodes[node_id] = node
            node.add_attribute(Attibute(persona, "persona"))
        elif I_WANT_IT_TO_BE == i_want:
            # be stories are attributes of parent
            node = nodes[parent_id]
            node.add_attribute(Attibute(description, "be"))
        else:
            # feel stories are attributes of parent
            node = nodes[parent_id]
            node.add_attribute(Attibute(description, "feel"))
        

    root.bubble_up_attributes()

    create_dot_graph(root)