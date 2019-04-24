import ply.lex  as lex
import ply.yacc as yacc

import dex2r_lex

tokens = dex2r_lex.tokens

def p_program(p):
	'''program : def ID LBRACKET list sentgroup'''
	
def p_list(p):
	'''list : type ID AND COMMA list
			| type ID COMMA list
			| type ID AND RBRACKET
			| type ID RBRACKET
			| RBRACKET'''
	
def p_type(p):
	'''type : bool
			| var
			| int
			| string
			| struct'''

def p_sentgroup(p):
	'''sentgroup : start sentencess'''
	p[0] = ('SENTGROUP', p[2])
	dex2r_lex.log(p[0])		
	
def p_error(p):
	pass

def p_sentencess(p):
	'''sentencess : sentencess sentence
				  | sentence end'''
	
def p_sentence(p):
		'''sentence : expression
					| logic'''
		p[0] = p[1]
	
def p_logic(p):
	'''logic : LBRACE ID DEQ ID RBRACE sentgroup'''
	p[0] = p[1]
		
def p_expr(p):
	'''expression : expression PLUS expression
					| expression MINUS expression
					| expression TIMES expression
					| expression DIVIDE expression
					| ID EQ expression
					| ID expression
					| ID'''
	p[0] = p[1]
	
parser = yacc.yacc()	
	
def parse(data, debug=0):
	parser.error = 0
	try:
		p = parser.parse(data, debug=debug)
	except lex.LexError:
		p = None
	return p


if __name__ == '__main__':
	def lexx(lexer, data):
		lexer.input(data)
		dex2r_lex.log(data)
		while True:
			tok = lexer.token()
			if not tok:
				break
			dex2r_lex.log (tok)
				
	lexer = lex.lex(module=dex2r_lex)
	#dex2r_lex.log()
	data = open('try1.dex2r').read()
	lexx(lexer, data)
	#dex2r_lex.log()
	prog = parse(data, 1)