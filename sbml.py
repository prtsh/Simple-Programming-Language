#!/usr/local/bin/env python

'''
    @author:  pratyush ranjan 
              netid: pranjan
              SBU ID: 112675752
    @program: expression evaluator for a  
              awesome language called SBML
    @output:  evaluates an expression,
              ouputs result or error
'''

#extending SBML to include variables, assignment, conditionals, loops, and output

import sys
from sbmlparser import *

if __name__ == "__main__":
    arguments = len(sys.argv)
    if arguments != 2:
        print("usage: sbml.py <input_file_name> ")
        exit();
    filepath = sys.argv[1];
    mainHW4(filepath)
    