#!/usr/bin/env python3

'''
    @author:  pratyush ranjan (netid: pranjan, 112675752)
    @program: expression evaluator for a  
              awesome language called SBML
    @output:  evaluates an expression,
              ouputs result or error
'''

import re
import sys, os
import ply.lex as lex

error_semantic = 0;
error_syntax  = 0;

reserved = ('IF', 'ELSE', 'WHILE', 'PRINT', 'ANDALSO', 'ORELSE', 'NOT', 'IN', 'MOD')
tokens = reserved + (
    # >, >=, <>, ==, <=, <, andalso, orelse, ~, ::, member
    'ID', 'GREATER', 'GREATEREQUAL', 'NOTEQUAL', 'EQUAL',         
    'LESSEQUAL', 'LESSTHAN',   
     'CONS', 
    #+, -, %, /, int div, *, **
    'MINUS', 'PLUS', 'INTDIV', 'DIV', 
    'MUL', 'EXPONENT', 

    #[ ], #, ( )
    'LBRACKET', 'RBRACKET', 'TUPLINDEX', 'LPAREN','RPAREN', 'LCURLY', 'RCURLY',     

    #data types
    'INT', 'REAL', 'STRING', 'BOOL',
    #;
    'SEMI', 'COMMA',
    'ASSIGN',
)

t_ASSIGN           = r'='
t_COMMA            = r','
t_GREATER          = r'>'   #22
t_GREATEREQUAL     = r'>='    #21 
t_NOTEQUAL         = r'<>'  #20 
t_EQUAL            = r'==' #19
t_LESSEQUAL        = r'<=' #18
t_LESSTHAN         = r'<' #17
t_CONS             = r'::' #13
t_MINUS            = r'-' #11
t_PLUS             = r'\+' #10
t_INTDIV           = r'div' #8
t_DIV              = r'/' #7
t_MUL              = r'\*' #6
t_EXPONENT         = r'\*\*' #5
t_LBRACKET         = r'\[' #4
t_RBRACKET         = r'\]' #4
t_LCURLY           = r'\{'
t_RCURLY           = r'\}'
t_TUPLINDEX        = r'\#' #3
t_LPAREN           = r'\('  #1,2
t_RPAREN           = r'\)' #1,2
t_SEMI             = r';'
t_ignore           = ' \t'


def t_REAL(t):
    r'[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'[0-9]+'
    #r'[-+]?[0-9]+'
    t.value = int(t.value)
    return t

def t_STRING(t):
     r'(\"([^\"]|(\\.))*\")|((\'([^\"]|(\\.))*\'))'
     #r'(?:\'|\").*(?:\'|\")'
     return t

def t_BOOL(t):
    r'True|False'
    return t;

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

reserved_map = {}
for r in reserved:
    reserved_map[r.lower()] = r

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved_map.get(t.value, "ID")
    return t
    
def t_error(t):
    #print("SYNTAX ERROR: %s at %d" % (t.value[0], t.lexer.lineno))
    error_syntax = 1;
    return
    #t.lexer.skip(1)

lex.lex(debug = 0);

if __name__ == '__main__':
    lex.runmain()


