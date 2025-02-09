"""Utility functions"""
import json

import yaml


def read_yaml(path):
    """Open YAML file and return as dict"""
    with open(path, 'rb') as fp:
        return yaml.safe_load(fp)


def decode_json(byte_array):
    try:
        return json.loads(byte_array.decode('utf-8'))
    except json.decoder.JSONDecodeError:
        return None
