import os
import pandas as pd

#cwd = os.getcwd()
def read_personas(path_to_file: str = os.path.join(os.getcwd(), "src", "data", "persona.txt")):
    personas = open(path_to_file, "r")
    personas = personas.readlines()
    personas = [x.rstrip() for x in personas]
    return personas