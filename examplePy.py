#!/usr/bin/env python3

# Example code for development of a commandline Python tool.

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--foo', help = 'foo help')
args = parser.parse_args()

print(args)