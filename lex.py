import os
import sys

import ply.lex as lex
from ply.lex import TOKEN
import re

debug = True

def log(came_log):
	if debug:
		print(came_log)
	if not debug:
		return 0

reserved = {
	 'TRUE' 		: 'true',
	 'FALSE' 		: 'false', 
	 'LOGIC' 		: 'bool',
	 'UNDEF' 		: 'var',
	 'NUMERIC' 		: 'int',
	 'STRING' 		: 'string',
	 'RECORD' 		: 'stuct',
	 'CONVERSION' 	: 'convert',
	 'TO' 			: 'to',
	 'FROM' 		: 'from',
	 'BLOCK' 		: 'start',
	 'UNBLOCK' 		: 'end',
	 'PROC' 		: 'def',
	 'MOVEUP' 		: 'up',
	 'MOVEDOWN' 	: 'down',
	 'MOVELEFT' 	: 'left',
	 'MOVERIGHT' 	: 'right',
	 'PINGUP' 		: 'knockup',
	 'PINGDOWN'		: 'knockdown',
	 'PINGRIGHT' 	: 'knockright',
	 'PINGLEFT' 	: 'knockleft',
	 'VISION' 		: 'vision',
	 'VOICE' 		: 'input'
	}
	
tokens = ['ID'] + list(reserved.values())

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'ID')    # Check for reserved words
     return t
	 
def t_newline(t):
	r'\n+'
	log('HERE')
	t.lexer.lineno += len(t.value)
	t.lexer.
	
	 
def t_error(t):
	log("Illegal character '%s'" % t.value[0])	 

t_ignore = ' \r\t\f'
	
data = "VOICE ddd \n RECORD X"
	
lexer = lex.lex(reflags=re.UNICODE | re.DOTALL)
lexer.input(data)
while True:
			tok = lexer.token() # читаем следующий токен
			if not tok: break	# закончились печеньки		
			log (tok)