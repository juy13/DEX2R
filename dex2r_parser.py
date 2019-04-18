import ply.lex  as lex
import ply.yacc as yacc

import dex2r_lex

tokens = dex2r_lex.tokens

def p_program(p):
	'''program : program EQ
			   | EQ'''
	dex2r_lex.log(p[0])
	
def p_error(p):
	pass

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
	data = open('simple_test.dex2r').read()
	lexx(lexer, data)
	#dex2r_lex.log()
	prog = parse(data, 1)