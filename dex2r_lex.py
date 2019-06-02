import os
import sys

import ply.lex as lex
from ply.lex import TOKEN
import re

debug = False
line_pos = 0
pos = 0

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
	 'RECORD' 		: 'struct',
	 'DATA'			: 'info',
	 
	 'CONVERSION' 	: 'convert',
	 'TO' 			: 'to',
	 'FROM'	 		: 'from',
	 
	 'BLOCK' 		: 'start',
	 'UNBLOCK' 		: 'end',
	 
	 'PROC' 			: 'def',
	 
	 'MOVEUP' 		: 'up',
	 'MOVEDOWN' 		: 'down',
	 'MOVELEFT' 		: 'left',
	 'MOVERIGHT' 	: 'right',
	 
	 'PINGUP' 		: 'knockup',
	 'PINGDOWN'		: 'knockdown',
	 'PINGRIGHT' 	: 'knockright',
	 'PINGLEFT' 		: 'knockleft',
	 
	 'VISION' 		: 'vision',
	 'VOICE' 		: 'input'
	}
	
tokens = ['ID', 'QUOTE', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 
		'EQ', 'PLUS', 'MINUS', 'TIMES', 'POWER', 'DIVIDE', 'LT',
		'GT', 'EX', 'AND', 'DEQ', 'NUMBER', 'COMMA', 'STR', 'PLL', 'PLR', 
		'DVL', 'DVR', 'TML', 'TMR', 'MNL', 'MNR', 'PWL', 'PWR', 'LTL', 'LTR', 'GTR', 'GTL', 
		'DEQL', 'DEQR', 'EXL', 'EXR'] + list(reserved.values())

t_QUOTE = '\"'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_EQ = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\^'
t_DIVIDE = r'/'
t_LT = r'<'
t_GT = r'>'
t_DEQ = r'\?'
t_EX = r'\!'
t_AND = r'\&'
t_COMMA = r'\,'
t_STR = r'\".*?\"'
t_NUMBER = r'\d+'
t_PLL = r'\.\+'
t_PLR = r'\+\.'
t_DVL = r'\.\/'
t_DVR = r'\/\.'
t_TML = r'\.\*'
t_TMR = r'\*\.'
t_MNL = r'\.\-'
t_MNR = r'\-\.'
t_PWL = r'\.\^'
t_PWR = r'\^\.'
t_LTL = r'\.<'
t_LTR = r'<\.'
t_GTL = r'\.>'
t_GTR = r'>\.'
t_DEQL= r'\.\?'
t_DEQR= r'\?\.'
t_EXL = r'\.\!'
t_EXR = r'\!\.'



def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'ID')    # Check for reserved words
     return t

def t_newline(t):
	r'\n'
	#log('HERE')
	global line_pos
	t.lexer.lineno += 1
	line_pos += 1
	log('LINE: ' + str(line_pos))
	 
def t_error(t):
	return print("Illegal character '%s' at line '%s'" % (t.value[0], t.lexer.lineno))	 

#def t_NUMBER(t):
#	r'\d+'
#	t.value = int(t.value)    
#	return t	
	
t_ignore = ' \r\t\f'
	
#data = "VOICE ddd \n RECORD X"
	
if __name__ == '__main__':
	file = open('simple_test.dex2r', 'r')
	lexer = lex.lex(reflags=re.UNICODE | re.DOTALL)
	
	for line in file:
		lexer.input(line)
		while True:
					tok = lexer.token() # читаем следующий токен
					if not tok: break	# закончились печеньки		
					log (tok)