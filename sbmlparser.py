#!/usr/bin/env python3

'''
    @author:  pratyush ranjan (netid: pranjan, 112675752)
    @program: expr evaluator for a  
              awesome language called SBML
    @output:  evaluates an expr,
              ouputs result or error
'''

import re
import sys, os
import ply.yacc as yacc
from sbmllexer import *

import logging
logging.basicConfig(
     level = logging.INFO,
     filename = "parselog.txt",
     filemode = "w",
     format = "%(filename)10s:%(lineno)4d:%(message)s"
 )
log = logging.getLogger()

variable = {};
stack = [True];

# Get's a symbol from variables dictionary and shows error if not exists
def getsymbol(p, i):
    # Get symbol's value form variables dictionary
    symbol_val = variable.get(p[i], None)
    if symbol_val is None:
       #pass;
       return
    else:
        return symbol_val

def boolexpr(expr):
    if expr == True:
        return True
    return False;

precedence = (
    ('right', 'ASSIGN'),
    ('left','ORELSE'),
    ('left','ANDALSO'),
    ('left','NOT'),
    ('left','LESSTHAN', 'LESSEQUAL', 'EQUAL', 'NOTEQUAL', 'GREATEREQUAL', 'GREATER'),
    ('right', 'CONS'),
    ('right','UMINUS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV', 'INTDIV', 'MOD'),
    ('right', 'EXPONENT'),
    )

# Program's starting point

def p_start(p):
    '''
    start : LCURLY program RCURLY
    '''
    pass

def p_program(p):
    ''' 
    program : stmt program
            | expr SEMI program
            | boolexpr SEMI program
            |
    '''
    pass

def p_print_stmt(p):
    """
    stmt : PRINT LPAREN print_arguments RPAREN SEMI
    """
    if not stack[-1]:
        return

    if p[3] is not None:
        print(p[3])

def p_printargs(p):
    """
    print_arguments : expr COMMA print_arguments
                    | boolexpr COMMA print_arguments
                    | boolexpr
                    | expr
    """
    global error_semantic
    if not stack[-1]:
        return

    if p[1] is None:
        pass
        return

    if len(p) == 2:
        p[0] = str(p[1])
    else:
        if p[3] is not None and p[1] is not None:
            p[0] = str(p[1]) + str(p[3])

def p_ifstmt(p):
    """
    stmt : IF LPAREN boolexpr RPAREN LCURLY ifStart program ifEnd RCURLY
         | IF LPAREN boolexpr RPAREN LCURLY ifStart program ifEnd RCURLY ELSE LCURLY ifElseStart program ifEnd RCURLY
    """
    pass

def p_ifStart(p):
    """
    ifStart :
    """
    global stack
    # If current state is not running
    if not stack[-1]:
        stack.append(False)
    # Push evaluated value as running state
    else:
        stack.append(p[-3])
        
def p_ifEnd(p):
    """
    ifEnd :
    """
    global stack
    stack.pop()

def p_ifElseStart(p):
    """
    ifElseStart :
    """
    global stack
    # If current state is not running
    if not stack[-1]:
        stack.append(False)
    # Push not(evaluated value) as running state
    else:
        stack.append(not p[-9])

def p_whilestmt(p):
    """
    stmt : WHILE LPAREN boolexpr RPAREN LCURLY whileStart program whileEnd RCURLY
    """
    pass

def p_whileStart(p):
    """
    whileStart :
    """
    global stack
    # If current state is not running
    if not stack[-1]:
        stack.append(False)
    # Push evaluated value as running state
    else:
        stack.append(p[-3])

def p_whileEnd(p):
    """
    whileEnd :
    """
    global stack
    stack.pop()

    if stack[-1] and p[-5]:
        p.lexer.lexpos = parser.symstack[-7].lexpos

def p_boolexpr_andornot(p):
    '''
        boolexpr :   NOT boolexpr
                   | boolexpr ANDALSO boolexpr
                   | boolexpr ORELSE boolexpr
    '''
    if not stack[-1]:
        return
    
    global error_semantic
    try:
        if len(p) == 3 and p[1] is not None and p[3] is not None:
            if p[2] == 'andalso':
                p[0] = p[1] and p[3]
            elif p[2] == 'orelse':
                p[0] = p[1] or p[3]

        if len(p) == 2 and p[1] == 'not' and p[2] is not None:
            p[0] = not p[2]
    except:
            pass;
            
def p_boolexpr_paran(p):
    """
    boolexpr : LPAREN boolexpr RPAREN
              | LCURLY boolexpr RCURLY
              | LBRACKET boolexpr RBRACKET
    """
    if not stack[-1]:
        return

    if p[2] is not None:
        p[0] = p[2]

def p_boolexpr_bool(p):
    '''
    boolexpr : BOOL
    '''
    p[0] = p[1]
        
def p_boolexpr_comparison(p):
    '''
    boolexpr : expr LESSTHAN expr
               | expr LESSEQUAL expr
               | expr EQUAL expr
               | expr NOTEQUAL expr
               | expr GREATEREQUAL expr
               | expr GREATER expr
    '''
    global error_semantic
    try:
            if  p[2] == '<':
                p[0] = p[1] < p[2]
            elif p[2] == '<=':
                p[0] = p[1] <= p[2]
            elif p[2] == '==':
                p[0] = p[1] == p[3]
            elif p[2] == '<>':
                p[0] = p[1] != p[3]
            elif p[2] == '>=':
                p[0] = p[1] >= p[3]
            elif p[2] == '>':
                p[0] = p[1] > p[3]
    except:
            pass

        
def p_expr_binop(p):
    '''
    expr :           expr PLUS expr
                   | expr MINUS expr
                   | expr MUL expr
                   | expr DIV expr
                   | expr EXPONENT expr
                   | expr INTDIV expr
                   | expr MOD expr  
    '''
    global error_semantic
    try:
                if p[2] == '+':
                    p[0] = p[1] + p[3]
                elif p[2] == '-':
                    p[0] = p[1] - p[3]
                elif p[2] == '*':
                   p[0] = p[1] * p[3]
                elif p[2] == '/':
                    p[0] = p[1] / p[3]
                elif p[2] == '**':
                    p[0] = p[1] ** p[3]
                elif p[2] == 'mod':
                    p[0] = p[1] % p[3]
                elif p[2] == 'div':
                    p[0] = int(p[1]/p[3])
    except:
                pass;

def p_boolexpr_ID(p):
    """
    boolexpr : ID
    """
    global error_semantic
    if not stack[-1]:
        return

    if p[1] == True or p[1] == False: 
        return p[1]
    else:
        pass
        
def p_expr_boolexpr(p):
    """
    expr : boolexpr
    """
    global error_semantic

    if p[1] == True or p[1] == False: 
        return p[1]
      
def p_expr_id(p):
    """
    expr : ID
    """
    if not stack[-1]:
        return

    # Get symbol's value
    symbol = getsymbol(p, 1)
    # If symbol does not exist
    if symbol is not None:
        p[0] = symbol

def p_expr(p):
    '''
    expr : INT
           | REAL
           | BOOL
           | SEMI
           |
    '''
    p[0] = p[1]

def p_expr_ID_assign_expr(p):
    """
    expr : ID ASSIGN expr
    """
    if not stack[-1]:
        return

    if p[3] is not None:
        variable[p[1]] = p[3]
        p[0] = p[3]

def p_expr_assign_expr(p):
    """
    expr : expr ASSIGN expr
    """
    if not stack[-1]:
        return

    if p[3] is not None:
        p[1] = p[3]
        p[0] = p[3]

def p_expr_string(p):
    '''
    expr : STRING
    '''
    p[0] = p[1]#p[1][1:-1]

def p_expr_paran(p):
    """
    expr : LPAREN expr RPAREN
    """
    p[0] = p[2]
    
def p_expr_uminus(p):
    """
    expr : MINUS expr %prec UMINUS
    """
    if not stack[-1]:
        return

    if p[2] is not None:
        p[0] = -p[2]

def p_expr_list(p):
    '''
    plist  : LBRACKET RBRACKET
           | LBRACKET listitem RBRACKET
    '''
    if len(p) == 3:
        p[0] = []

    if len(p) > 3:
        p[0] = p[2]

def p_expr_listitem(p):
    '''
    listitem : listitem COMMA expr
            | expr
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]] 

def p_expr_tuple(p):
    '''
    ptuple  : LPAREN RPAREN
            | LPAREN tupleitem RPAREN
    '''
    if len(p) == 3:
        p[0] = ()

    if len(p) > 3:
        p[0] = p[2]

def p_expr_tupleitem(p):
    '''
    tupleitem : tupleitem COMMA expr
            | expr
    '''
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = p[1] + (p[3],) 

def p_expr_listindex(p):
    '''
    expr : expr LBRACKET expr RBRACKET
    '''
    global error_semantic
    if p[1] is None or p[2] is None:
            pass
        
    try:
        if p[3] > len(p[1]):
            pass
            return;
        
        if isinstance(p[1], str) == False and isinstance(p[1], list) == False \
            or isinstance(p[3], int) == False:
            pass
        else:
            p[0] = p[1][p[3]];
    except:
        pass;

def p_expr_listindexid(p):
    '''
     expr : expr LBRACKET ID RBRACKET
    '''
    global error_semantic
    if p[1] is None or p[2] is None:
            pass
            return
        
    p[0] = p[1][variable[p[3]]];

def p_expr_linear(p):
    '''
    expr : plist
         | ptuple
    '''
    p[0] = p[1]

def p_expr_membership(p):
   '''
   expr : expr IN expr
   ''' 
   global error_semantic
   try:
       if isinstance(p[3], str) == False and isinstance(p[3], list) == False:
           pass
       else:    
            try:
                if p[1] in p[3]:
                    p[0] = True
                else:
                    p[0] = False
            except:
                pass
   except:
       pass

def p_expr_cons(p):
    '''
    expr : expr CONS expr
    '''
    global error_semantic
    try:
        if isinstance(p[3], list):
            p[0] = [p[1]] + p[3];
    except:
        pass

def p_expr_tupleindex(p):
    '''
    expr : TUPLINDEX INT expr 
    '''
    global error_semantic
    try:
        if isinstance(p[2], int) == False or isinstance(p[3], tuple) == False:
            pass
        else:
            p[0] = p[3][p[1] + 1];
    except:
        pass

def p_expr_or_empty(p):
    """
    expr_or_empty : expr
                  |
    """
    if not stack[-1]:
        return

    if len(p) == 2:
        p[0] = p[1]  

def p_error(p):
    global error_semantic;
    error_semantic = 1;


'''
support for assignment to variables must be added

support must be added for variables used in exprs. 
For example, if x was assigned 1, then "print(x);" will print 1.

If the variable has had a value assigned to it, then the value 
should be returned. Otherwise, a "Semantic Error" should be reported and your program should stop

  If the variable is not a list (or a string), or the index is not an integer, then a Semantic 
  Error should be reported.  If the index is outside the bounds of the list, then a Semantic 
  Error should be reported

  If Statements: Consist of a keyword "if", a left parenthesis, an expr, 
  a right parenthesis, and a block statement as the body of the If statement.
'''

parser = yacc.yacc(debuglog=log)
def mainHW3(filepath):
    global error_semantic
    global error_syntax
    for line in open('inputfile.txt','r').readlines():
            #print(line)
            try:
                result = parser.parse(line, debug = 0)
                if error_semantic == 1:
                    print("SEMANTIC ERROR")
                    error_semantic = 0
                elif error_syntax == 1:
                    print("SYNTAX ERROR")
                    error_syntax = 0
                elif result != None:
                    print(result);
                elif result == None:
                    print("SYNTAX ERROR")
            except:
                pass
                #print("SYNTAX ERROR")

def mainHW4(filepath):
    global parser
    global error_semantic
    global error_syntax
    with open(filepath, 'r') as file:
       program = file.read().replace('\n', ' ')
     
    #print(program)
    parser.parse(program, debug = log );
    #print(error_semantic)
    if error_semantic > 0:
        print('SEMANTIC ERROR')
    if error_syntax > 0:
        print('SYNTAX ERROR')
    


