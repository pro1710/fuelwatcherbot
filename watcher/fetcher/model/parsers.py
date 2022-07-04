import logging

def parseWogStatus(obj:dict):

    # TODO: create function to vlidate expected dictionary structure aka FuelStation dict from types.py

    if 'STATUS' not in obj:
        return None
