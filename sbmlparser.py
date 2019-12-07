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

def boolexpr(expr):
    if expr is None:
        return None

    if type(expr) is str:
        if len(expr) > 0:
            return True
        else:
            return False

    if expr != 0:
        return True
    else:
        return False

precedence = (
    ('right', 'ASSIGN'),
    ('left','ORELSE'),
    ('left','ANDALSO'),
    ('left','NOT'),
    ('left','LESSTHAN', 'LESSEQUAL', 'EQUAL', 'NOTEQUAL', 'GREATEREQUAL', 'GREATER'),
    ('right', 'CONS', 'IN'),
    ('right','UMINUS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV', 'INTDIV', 'MOD'),
    ('right', 'EXPONENT'),
    #('right', 'LBRACKET','RBRACKET'),
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
    if not stack[-1]:
        stack.append(False)
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
                   | NOT expr
                   | expr ANDALSO expr
                   | expr ORELSE expr
    '''
    if not stack[-1]:
        return
    
    global error_semantic
    try:
        if p[1] == 'not' and p[2] is not None:
                p[0] = not p[2]
        elif p[1] is not None and p[3] is not None:
            if p[2] == 'andalso':
                p[0] = p[1] and p[3]
            elif p[2] == 'orelse':
                p[0] = p[1] or p[3]
        else:
            pass
    except:
            pass;
            
def p_boolexpr_paran(p):
    """
    boolexpr :  LPAREN boolexpr RPAREN
    """
    if not stack[-1]:
        return

    if p[2] is not None:
        p[0] = p[2]

def p_boolexpr_bool(p):
    '''
    boolexpr : BOOL
    '''
    if not stack[-1]:
            return
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
    if not stack[-1]:
            return
        
    if p[1] is None or p[3] is None:
        p[0] = None
        return
    
    try:
        #print(p[1], p[3])
        if  p[2] == '<':
            p[0] = p[1] < p[3]
        elif p[2] == '<=':
            p[0] = p[1] <= p[3]
        elif p[2] == '==':
            p[0] = p[1] == p[3]
        elif p[2] == '<>':
            p[0] = p[1] != p[3]
        elif p[2] == '>=':
            p[0] = p[1] >= p[3]
        elif p[2] == '>':
            p[0] = p[1] > p[3]
        else:
            p[0] = None
    except Exception as e: 
        #print(e);
        #pass
        global error_semantic
        error_semantic = error_semantic + 1

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
    if not stack[-1]:
            return
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
    except Exception  as e:
        #print(e)
        global error_semantic
        error_semantic = error_semantic + 1
        
def p_expr_boolexpr(p):
    """
    expr : boolexpr
    """
    if not stack[-1]:
            return
        
    global error_semantic
    result = boolexpr(p[1])
    p[0] = result;
    return p[1]

def p_expr_id(p):
    """
    expr : ID
    """
    if not stack[-1]:
            return
        
    global variable
    value = variable.get(p[1])
    #print(value)
    if value is not None:
        p[0] = value
        return value
    else:
        return None
    #print(p[1], value)

def p_boolexpr_id(p):
    """
    boolexpr : ID
    """
    if not stack[-1]:
            return
        
    global variable
    symbol_val = variable.get(p[1])
    if symbol_val is not None and symbol_val != 0:
        p[0] = True
    else:
        p[0] = False
    

def p_expr(p):
    '''
    expr : INT
           | REAL
           | BOOL
           | SEMI
           |
    '''
    if not stack[-1]:
            return
    p[0] = p[1]
    
def p_expr_string(p):
    '''
    expr : STRING
    '''
    if not stack[-1]:
            return
    p[0] = p[1][1:-1]

def p_expr_paran(p):
    """
    expr : LPAREN expr RPAREN
    """
    if not stack[-1]:
            return
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
    if not stack[-1]:
            return
    if len(p) == 3:
        p[0] = []

    if len(p) > 3:
        p[0] = p[2]

def p_expr_listitem(p):
    '''
    listitem : listitem COMMA expr
            | expr
    '''
    if not stack[-1]:
            return
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]] 

def p_expr_tuple(p):
    '''
    ptuple  : LPAREN RPAREN
            | LPAREN tupleitem RPAREN
    '''
    if not stack[-1]:
            return
    if len(p) == 3:
        p[0] = ()

    if len(p) > 3:
        p[0] = p[2]

def p_expr_tupleitem(p):
    '''
    tupleitem : tupleitem COMMA expr
            | expr
    '''
    if not stack[-1]:
            return
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = p[1] + (p[3],) 

def p_expr_membership(p):
   '''
   expr : expr IN expr
   ''' 
   if not stack[-1]:
            return
   global error_semantic
   try:
                if p[1] in p[3]:
                    p[0] = True
                else:
                    p[0] = False
   except:
       error_semantic = error_semantic + 1

def p_expr_cons(p):
    '''
    expr : expr CONS expr
    '''
    if not stack[-1]:
            return
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
    if not stack[-1]:
            return
    global error_semantic
    try:
        if isinstance(p[2], int) == False or isinstance(p[3], tuple) == False:
            pass
        else:
            p[0] = p[3][p[1] + 1];
    except:
        pass

def p_expr_ID_assign_expr(p):
    """
    expr :  ID ASSIGN expr
          | ID ASSIGN expr SEMI
    """
    if not stack[-1]:
            return 
          
    global variable
    if p[3] is not None:
        variable[p[1]] = p[3]
        p[0] = p[3]
    
def p_expr_list_assign_id(p):
    """
    expr : ID LBRACKET expr RBRACKET ASSIGN ID
    """
    if not stack[-1]:
            return
    if p[3] is None or p[1] is None:
        return
    
    global variable
    
    lval = variable.get(p[1])
    rval = variable.get(p[6])
    lval[p[3]] = rval;
    variable[p[1]] = lval;
    p[0] = rval

def p_expr_list_assign_list(p):
    """
    expr : ID LBRACKET expr RBRACKET ASSIGN listval
    """
    if not stack[-1]:
            return
    if p[1] is None or p[3] is None or p[6] is None:
        return 
    
    global variable
    #print(p[6])
    lval = variable.get(p[1])
    rval = p[6]
    lval[p[3]] = p[6];
    variable[p[1]] = lval;
    p[0] = p[6];
    
def p_expr_id_assign_list(p):
    """
    expr : ID ASSIGN listval
    """
    if not stack[-1]:
        return
    global variable
    lval = variable.get(p[1])
    rval = p[3]
    lval = rval
    variable[p[1]] = lval;
    p[0] = p[3]
    
def p_expr_listval(p):
    '''
    listval : ID LBRACKET expr RBRACKET
    '''
    if not stack[-1]:
            return
    global variable
    if p[1] == None or p[3] == None:
        return
    
    temp = variable.get(p[1])
    p[0] = temp[p[3]]
    
def p_expr_assign_expr(p):
    """
    expr : lvalue ASSIGN rvalue
          | lvalue ASSIGN rvalue SEMI
    """
    if not stack[-1]:
        return
    
    if p[3] is not None:
        p[1] = p[3]
        p[0] = p[3]
        
def p_exp_lvalue(p):
    """
    lvalue : expr
           | ID
           | expr '[' expr ']' 
           | expr '[' expr ']' '[' expr ']'
    """
    pass

def p_exp_rvalue(p):
    """
    rvalue : expr
           | ID
           | expr '[' expr ']' 
           | expr '[' expr ']' '[' expr ']'
    """
    pass

def p_expr_or_empty(p):
    """
    expr_or_empty : expr
                  | empty
    """
    if not stack[-1]:
        return
    
    if len(p) == 2:
        p[0] = p[1]  

def p_expr_linear(p):
    '''
    expr : plist
         | ptuple  
         | listval
    '''
    if not stack[-1]:
            return
    p[0] = p[1]

def p_expr_listindex(p):
    '''
    expr : expr LBRACKET expr RBRACKET
    '''
    if not stack[-1]:
            return
    global error_semantic
    if p[1] is None or p[3] is None:
            error_semantic = error_semantic + 1
            return None
        
    try:
        if p[3] > len(p[1]):
            error_semantic = error_semantic + 1
            return
        else:
            p[0] = p[1][p[3]]
            return p[1][p[3]]
    except:
        error_semantic = error_semantic + 1

def p_expr_listindexdouble(p):
    '''
    expr : ID LBRACKET expr RBRACKET LBRACKET expr RBRACKET
    '''
    if not stack[-1]:
            return
    global variable
    global error_semantic
    if p[1] is None or p[3] is None or p[6] is None:
            error_semantic = error_semantic + 1
            return None
        
    try: 
            temp = variable.get(p[1])
            p[0] = temp[p[3]][p[6]]
            return p[0]
    except:
        error_semantic = error_semantic + 1

def p_empty(p):
     '''
     empty :
     '''
     if not stack[-1]:
            return
     pass
 
def p_error(p):
    global error_semantic;
    error_semantic = 1;

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
    


