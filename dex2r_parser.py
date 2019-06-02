import ply.lex  as lex
import ply.yacc as yacc
import pickle

import dex2r_lex

debug = True
def log(came_log):
	if debug:
		print(came_log)
	if not debug:
		return 0

tokens = dex2r_lex.tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'POWER'),
    ('right', 'UMINUS')
)
	
def p_program(p):
	'''program : program statement
				| statement'''
	
	if len(p) == 2 and p[1]:
		p[0] = {}
		log('HEREHEHRHRHHRHREHHREHREHRHHREHRHRHRHHRHREHRHRHRHHRHRHRHHERHRH' + p[1][1][0])
		log(p[1])
		if p[1][1][0] == 'FUNCERROR':
			if 0 not in p[0]:
				p[0][0] = [p[1][1]]
			else:
				p[0][0].append(p[1][1])

		if p[1][1][0] == 'SENTGROUP':
			if 1 not in p[0]:
				p[0][1] = [p[1]]
			else:
				p[0][1].append(p[1])

		if p[1][1][0] == 'RECORDS':
			if 2 not in p[0]:
				p[0][2] = [p[1]]
			else:
				p[0][2].append(p[1])

		if p[1][1][0] == 'FUNC':
			if p[1][1][1] not in p[0]:
				p[0][p[1][1][1]] = p[1]
			else:
				if 0 not in p[0]:
					p[0][0] = [('FUNCERROR', 'FUNCTION WITH THAT ID "%s" ALREADY EXIST at line %s' % (p[2][1][1], p.lineno(2)))]
				else:
					p[0][0].append([('FUNCERROR', 'FUNCTION WITH THAT ID "%s" ALREADY EXIST at line %s'
				            % (p[2][1][1], p.lineno(2)))])

		if p[1][1][0] != 'FUNCERROR' and p[1][1][0] != 'SENTGROUP' and p[1][1][0] != 'FUNC' :
			if 0 not in p[0]:
				p[0][0] = [p[1][1]]
			else:
				p[0][0].append(p[1][1])
		
	elif len(p) == 3:
		p[0] = p[1]
		log(p[2])
		if p[2][1][0] == 'FUNC':
			log('HEREHEHRHRHHRHREHHREHREHRHHREHRHRHRHHRHREHRHRHRHHRHRHRHHERHRH')
			if p[2][1][1] not in p[1]:
				p[0][p[2][1][1]] = p[2]
			else:
				if 0 not in p[0]:
					p[0][0] = [('FUNCERROR', 'FUNCTION WITH THAT ID "%s" ALREADY EXIST at line %s' % (p[2][1][1], p.lineno(2)))]
				else:
					p[0][0].append([('FUNCERROR', 'FUNCTION WITH THAT ID "%s" ALREADY EXIST at line %s'
				            % (p[2][1][1], p.lineno(2)))])
		
		if p[2][1][0] == 'SENTGROUP':
			log('HEREHEHRHRHHRHREHHREHREHRHHREHRHRHRHHRHREHRHRHRHHRHRHRHHERHRH')
			if 1 not in p[0]:
				p[0][1] = [p[2]]
			else:
				p[0][1].append(p[2]) 

		if p[2][1][0] == 'RECORDS':
			log('HEREHEHRHRHHRHREHHREHREHRHHREHRHRHRHHRHREHRHRHRHHRHRHRHHERHRH')
			if 2 not in p[0]:
				p[0][2] = [p[2]]
			else:
				p[0][2].append(p[2]) 
			
		if p[2][1][0] == 'FUNCERROR':
			log('HEREHEHRHRHHRHREHHREHREHRHHREHRHRHRHHRHREHRHRHRHHRHRHRHHERHRH' + str(p[2]))
			if 0 not in p[0]:
				p[0][0] = [p[2][1]]
			else:
				p[0][0].append(p[2][1])
			
		#else:
		#	# error
		#	if 0 in p[0]:
		#		p[0][0] += p[2]
		#	else:
		#		p[0][0] = p[2]
		#	p.parser.error += 1

def p_statement(p):
	'''statement : records
				 | sentgroup
				 | func'''
	log(p[1])
	p[0] = ('STatement', p[1])
	log(p[0])
	
	
def p_program_error(p):
	'''program : error'''
	if len(p) == 2:
		p[0] = {}
	else:
		p[0] = p[1]
	p[0][0].append(('FUNCERROR', 'NOT FUNC at line %s' % p.lineno(1)))
	log('NOT FUNC SENTENCE at line %s' % p.lineno(1))
	p.parser.error += 1
	
#
	
def p_func(p):
	'''func : def ids LBRACKET list RBRACKET sentgroup'''
	p[0] = ('FUNC', p[2][1], 'LIST', p[4], 'SENTGROUP', p[6])
	
	
def p_func_error1(p):
	'''func : def error LBRACKET list RBRACKET sentgroup'''
	p[0] = ('FUNCERROR', 'BAD FUNC ID at line %s' %p.lineno(1))
	p.parser.error += 1


def p_func_error2(p):
	'''func : def ids LBRACKET error RBRACKET sentgroup'''
	p[0] = ('FUNCERROR', 'BAD FUNC PARAMS at line %s' % p.lineno(1))
	p.parser.error += 1
	
	
def p_func_error3(p):
	'''func : def ids LBRACKET error RBRACKET error'''
	p[0] = ('FUNCERROR', 'BAD FUNC SENTGROUP at line %s' % p.lineno(1))
	log(p[0])
	p.parser.error += 1
	
	
def p_func_error4(p):
	'''func : def error'''
	p[0] = ('FUNCERROR', 'TERRIBLE FUNC ERRORS at line %s' % p.lineno(1))
	
	
def p_ids(p):
	'''ids : ID'''
	p[0] = ('ID', p[1])

			
def p_list(p):
	'''list : type ids AND COMMA list
			| ID ids AND COMMA list
			| type ids COMMA list
			| ID ids COMMA list
			| type ids AND
			| type ids
			| ID ids
			| '''
	if len(p) == 6:
		p[0] = (p[1], p[2], p[3], p[5])
	
	if len(p) == 5:
		p[0] = (p[1], p[2], p[4])
		
	if len(p) == 4:
		p[0] = (p[1], p[2], p[3])
		
	if len(p) == 3:
		p[0] = (p[1], p[2])
	
	
def p_type(p):
	'''type : bool
			| int
			| string
			| struct'''
	p[0] = p[1]

	
def p_sentgroup(p):
	'''sentgroup : start sentencess end'''
	p[0] = ('SENTGROUP', p[2])
	dex2r_lex.log(p[0])		
	
	
def p_define(p):
	'''define : int ids
				| bool ids
				| string ids
				| ID ids
				| int ids LBRACKET NUMBER RBRACKET
				| boolean ids LBRACKET NUMBER RBRACKET
				| string ids LBRACKET NUMBER RBRACKET'''
	if len(p) == 3:
		p[0] = ('DEFINE', p[1], p[2])
	if len(p) == 6:
		p[0] = ('DEFINE', p[1], p[2], 'LEN', p[4])
	
	
def p_sentencess(p):
	'''sentencess : sentencess sentence
				  | sentence'''
	if len(p) == 3:
			p[0] = p[1]
			p[0].append(p[2])
	else:
		p[0] = [p[1]]
	
	
def p_sentence(p):
	'''sentence : cfunc
				| expression
				| logic
				| define
				| assignment
				| move
				| ping
				| sensor'''
	p[0] = ('SENTENCE', p[1])
	
	
def p_sentence_error(p):
	'''sentence : error'''
	p.parser.error += 1
	p[0] = ('SENTENCE', ('ERR', 'SYNT: SOME TERRIBLE SENTENCE ERROR at line %s' % p.lineno(1)))

	
#как записать и понять запись	

def p_records(p):
	'''records : record records
			   | record '''
	if len(p) == 3:
		p[0] = ('RECORDS', p[1], p[2])
		log(p[0])
	if len(p) == 2:
		p[0] = ('RECORDS', p[1])
		log(p[0])
	
def p_record(p):
	'''record : struct ID info deflst
			  | struct ID info deflst convert to deflst
			  | struct ID info deflst convert from deflst
			  | struct ID info deflst convert to deflst convert from deflst'''
	if len(p) == 5:
		p[0] = ('RECORD', p[2], 'INFO', p[4])
	if len(p) == 8:
		p[0] = ('RECORD', p[2], 'INFO', p[4], 'CONVERT', p[6], p[7])
	if len(p) == 11:
		p[0] = ('RECORD', p[2], 'INFO', p[4], 'CONVERT TO', p[7], 'CONVERSION FROM', p[10])
	

def p_deflst(p):
	'''deflst : type ids deflst
			  | type ids'''
	if len(p) == 4:
		p[0] = (p[1], p[2], p[3])
	if len(p) == 3:
		p[0] = (p[1], p[2])


def p_logic(p):
	'''logic : LBRACE lexp RBRACE sentgroup'''
	p[0] = ('LOGIC', p[2], p[4])
		
		
def p_lexp(p):
	'''lexp : expression lt expression
            | expression gt expression
            | expression deg expression
            | expression ex expression'''
	p[0] = ('LEXP', p[2], p[1], p[3])
		
def p_lt(p):
	'''lt : LTR
		  | LTL
		  | LT'''
	if len(p) == 2:	
		p[0] = (p[1])
	#if len(p) == 3:
	#	p[0] (p[1], p[2])	


def p_gt(p):
	'''gt : GTR
		  | GTL
		  | GT'''
	if len(p) == 2:	
		p[0] = (p[1])
	if len(p) == 3:
		p[0] (p[1], p[2])	

def p_deg(p):
	'''deg : DEQR
		   | DEQL
		   | DEQ'''
	if len(p) == 2:	
		p[0] = (p[1])
	if len(p) == 3:
		p[0] = (p[1], p[2])	

def p_ex(p):
	'''ex : EXR
		  | EXL
		  | EX'''
	if len(p) == 2:	
		p[0] = (p[1])
	if len(p) == 3:
		p[0] (p[1], p[2])	



def p_expr(p):
	'''expression : expression plus expression
					| expression minus expression
					| expression times expression
					| expression divide expression
					| expression power expression
					|'''
	if len(p) == 2:
		p[0] = p[1]
	if len(p) == 3:
		p[0] = (p[1], p[2])
	if len(p) == 1:
		p[0] = ('BINOP')
	else:
		p[0] = ('BINOP', p[2], p[1], p[3])

def p_plus(p):
	'''plus : PLR
			| PLL
			| PLUS'''
	if len(p) == 2:	
		p[0] = (p[1])
	#if len(p) == 3:
	#	p[0] (p[1], p[2])	


def p_minus(p):
	'''minus : MNR
			 | MNL
			 | MINUS'''
	if len(p) == 2:	
		p[0] = (p[1])
	if len(p) == 3:
		p[0] (p[1], p[2])	

def p_times(p):
	'''times : TMR
			 | TML
			 | TIMES'''
	if len(p) == 2:	
		p[0] = (p[1])
	if len(p) == 3:
		p[0] = (p[1], p[2])	

def p_divide(p):
	'''divide : DVR
			  | DVL
			  | DIVIDE'''
	if len(p) == 2:	
		p[0] = (p[1])
	if len(p) == 3:
		p[0] (p[1], p[2])	

def p_power(p):
	'''power : PWR
			 | PWL
			 | POWER'''
	if len(p) == 2:	
		p[0] = (p[1])
	if len(p) == 3:
		p[0] (p[1], p[2])	

	
def p_str(p):
	'''str : STR'''
	p[0] = ('STR', p[1])

def p_expr_str(p):
	'''expression : str'''
	p[0] = p[1]
	
def p_expr_num(p):
	'''expression : num'''
	p[0] = p[1]
	
def p_num(p):
	'''num : NUMBER'''
	p[0] = ('NUM', p[1])
	
def p_exp_ids(p):
	'''expression : ids'''
	p[0] = p[1]
	
	
def p_expr_var(p):
	'''expression : boolean'''
	p[0] = p[1]
	
	
def p_expr_unary(p):
	'''expression : MINUS expression %prec UMINUS'''
	p[0] = ('UNARY', '-', p[2])
	
	
def p_callfunc(p):
	'''cfunc : ids LBRACKET exprgroup RBRACKET
			 | ids LBRACKET ids RBRACKET
			 | ids LBRACKET RBRACKET'''
	if len(p) == 4:
		p[0] = ('CALL', p[1])
	if len(p) == 5:
		p[0] = ('CALL', p[1], 'PARAMS', p[3])
	
	
def p_exprgroup(p):
	'''exprgroup : expression COMMA exprgroup
					| expression'''
	if len(p) == 4:
		p[0] = (p[1], p[3])
	if len(p) == 2:
		p[0] = p[1]
	
#index or id	

def p_assigment(p):
	'''assignment : ids EQ var
				  | ids EQ expression
				  | ids EQ str
				  | ids EQ ID LBRACKET ids RBRACKET
				  | ids LBRACKET expression RBRACKET EQ expression 
				  | ids LBRACKET ids RBRACKET EQ expression'''
	if len(p) == 4:
		p[0] = ('ASSIGMENT', p[1], p[3])
	if len(p) == 7:
		log(p[2])
		if p[2] == '[':
			p[0] = ('ASSIGMENT', p[1], 'PLACE', p[3], p[6])
		else:
			p[0] = ('ASSIGMENT', p[1], p[3], 'PLACE', p[5])
	
	
	
#def p_acs(p):
#	'''access : ids LBRACKET expression RBRACKET EQ expression
#				| ids LBRACKET ids RBRACKET EQ expression'''
#	p[0] = ('ACS', p[1], p[3], p[6])
	
	
def p_move(p):
	'''move : up LBRACKET steps RBRACKET
			| down LBRACKET steps RBRACKET
			| left LBRACKET steps RBRACKET
			| right LBRACKET steps RBRACKET'''
	p[0] = ('MOVE', p[1], p[3])

	
def p_steps(p):
	'''steps : expression
			 | ids'''
	p[0] = p[1]
	
	
def p_ping(p):
	'''ping : knockup LBRACKET steps RBRACKET
			| knockdown LBRACKET steps RBRACKET
			| knockright LBRACKET steps RBRACKET
			| knockleft LBRACKET steps RBRACKET'''
	p[0] = ('PING', p[1], p[3])
	
	
def p_boolean(p):
	'''boolean : false
			   | true
			   | var'''
	p[0] = ('boolean', p[1])	  
	
	
def p_sensor(p):
	'''sensor : vision LBRACKET ids RBRACKET
			  | input LBRACKET ids RBRACKET'''
	p[0] = ('SENSE', p[1], p[3]) 


parser = yacc.yacc()	
	
def parse(data, debug=0):
	parser.error = 0
	parser.lineno = 1
	try:
		p = parser.parse(data, debug=debug)
	except lex.LexError:
		p = None
	return p


def run_parser(data):
    def lexx(lexer, data):
        lexer.input(data)
        dex2r_lex.log(data)
        while True:
        	tok = lexer.token()
        	if not tok:
        		break
        	dex2r_lex.log(tok)
        lexer.lineno = 1

    lexer = lex.lex(module=dex2r_lex)
    lexx(lexer, data)
    dex2r_lex.line_pos = 0
    prog = parse(data, 1)
    print(prog)
    return prog

if __name__ == '__main__':

	def lexx(lexer, data):
		lexer.input(data)
		dex2r_lex.log(data)
		while True:
			tok = lexer.token()
			if not tok:
				break
			dex2r_lex.log(tok)
		lexer.lineno = 1
				
	lexer = lex.lex(module=dex2r_lex)
	#dex2r_lex.log()
	data = open('try1.dex2r').read()
	lexx(lexer, data)
	dex2r_lex.line_pos = 0
	#dex2r_lex.log()
	prog = parse(data, 1)
	
	print(prog)
	if not prog:
	 	print('not prog')
	else:
		with open('parseresult.out', 'wb') as f:
			pickle.dump(prog, f)
		file = open('parseout', 'w')
		for key in prog:
			print('%s : %s' % (key, prog[key]))
			if key == 0:
				file.write('FUNC ERRORS : ' + str(prog[key]) + '\n')
			else:
				file.write('%s : %s' % (key, prog[key]) + '\n')
		f.close()