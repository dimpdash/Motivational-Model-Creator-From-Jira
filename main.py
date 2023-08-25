import graphviz
import pandas as pd
from node import Node, Attibute 
from dot_graph import create_dot_graph

from app_controller import create_motivational_model_controller
from argparse import ArgumentParser

if __name__ == '__main__':
    argParser = ArgumentParser()
    argParser.add_argument("--project_name", help="project name", default="Project Name")
    argParser.add_argument("--filepath", help="filepath", required=True)

    args = argParser.parse_args()
    project_name = args.project_name
    filepath = args.filepath

    create_motivational_model_controller(project_name, filepath)