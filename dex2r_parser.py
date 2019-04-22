import ply.lex  as lex
import ply.yacc as yacc

import dex2r_lex

tokens = dex2r_lex.tokens

#def p_program(p):
#	'''program : program EQ
#			   | EQ'''
#	dex2r_lex.log(p[0])
	
def p_logic(p):
	'''logic : LBRACE ID DEQ ID RBRACE sentence'''
	p[0] = p[1]
	
def p_error(p):
	pass
	
#def p_sentgroup(p):
#	'''sentgroup : start sentencess end'''
#	p[0] = ('SENTGROUP', p[2])
#	dex2r_lex.log(p[0])
#
#def p_sentencess(p):
#	'''sentencess : sentencess sentence
#				  | sentence end'''
#	if len(p) == 3:
#		p[0] = p[1]
#		p[0].append(p[2])
#	else:
#		p[0] = [p[1]]
#		 start ID EQ ID PLUS ID end
#
def p_sentence(p):
		'''sentence : start expr end'''
		p[0] = p[1]
		
def p_expr(p):
	'''expr : ID EQ ID PLUS ID '''
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