import sys
import math
import random
from LabyrinthClass import LabirynthClass as lb

ERROR_LIST = (
	'Предупреждение: Лабиринт неинициализирован! Попытки вызова методов работы с лабиринтом вызовут ошибку.',
	'Ошибка # 1: Отсутствует точка входа в программу.',
	'Ошибка # 2: Несовпадение типов.',
	'Ошибка # 3: Необъявленная переменная.',
	'Ошибка # 4: Несовпадение размерностей vector.',
	'Ошибка # 5: Некорректные параметры вызова функции.',
	'Ошибка # 6: Вызов неизвестной функции.',
	'Ошибка # 7: По миниальной лексеме найдено несколько переменных.',
	'Ошибка # 8: Обращение к вектору как к переменной.',
	'Ошибка # 9: Обращение к неинициализированной переменной.',
	'Ошибка # 10: Переполнение.',
	'Ошибка # 11: Дистигнута максимальная глубина рекурсии.',
	'Ошибка # 12: Вызванная функция ничего не вернула.',
	'Ошибка # 13: Видимо бесконечный цикл.',
	'Ошибка # 14: Объявляемая переменная уже существует.'
)

def leng(obj):
	try:
		q1 = len(obj)
	except:
		q1 = 0
	return q1

debug = True
def log(came_log):
	if debug:
		print(came_log)
	if not debug:
		return 0

class DexInterp:

	def __init__(self, prog):
		self.prog = prog
		self.recDict = {}
		self.labyrinth = lb()
		self.labyrinth.init_trace('traceI.txt')
		self.password = None
	#	self.isLabyrinthInit = self.labyrinth.inited
		self.syntErrors = 0
		
		
	def run(self):
		self._check_SyntaxError()
		if self.syntErrors:
			print()
			print('Total syntax errors have found: ' + str(self.syntErrors))
			raise RuntimeError

		if 1 not in self.prog:
			print(ERROR_LIST[1])
			self.syntErrors = 1
			raise RuntimeError

		if 2 in self.prog:
			self._make_records(self.prog[2])

		#if not self.isLabyrinthInit:
		#	print(ERROR_LIST[0])
		val = self._start()
		self.labyrinth.close_trace()
		return val
	
	
	def _start(self):
		localVariables = {}
		val = self._sentencess(self.prog[1][0][1],
		                       localVariables, 1)  # ('SENTGROUP', p[2]) -> sentencess = [ ('SENTENCE', p[1]), ... ]
		
	
	
	def _sentencess(self, sentencess, varsDict, funcID):
		sentencess = sentencess[1]
		for sentence in sentencess:
			if sentence[1] is not None:
				sent = sentence[1]

				if sent[0] == 'DEFINE':
					self._define_variables(sent, varsDict, funcID)

				if sent[0] == 'LOGIC':
					self._logic(sent, varsDict, funcID)

				elif sent[0] == 'ASSIGMENT':
					self._assigment(sent, varsDict, funcID)

				elif sent[0] == 'CALL':
					paramsLst = []
					if len(sent) == 4:
						paramsLst = self._get_fromDict(sent[3], paramsLst, varsDict, funcID)
					val = self._call_func(sent[1][1], paramsLst)
					for i in range(len(paramsLst)):
						if val[i][1] == '&':
							item = val[i][2]
							id = paramsLst[i][0]
							varsDict[id] = (item[0], item[1])
							paramsLst[i] = (id, (item[0], item[1]))

				elif sent[0] == 'MOVE':
					self._move(sent, varsDict, funcID)

				elif sent[0] == 'PING':
					self._ping(sent, varsDict, funcID)

				elif sent[0] == 'SENSE':
					if sent[1] == 'VISION':
						self._vision(sent, varsDict, funcID)
					if sent[1] == 'VOICE':
						self._voice(sent, varsDict, funcID)

				elif sent[0] == 'EMPTY':
					pass
	

	def _vision(self, sent, varsDict, funcID):
		str = self.labyrinth.vision()
		varsDict[sent[2][1]] = (varsDict[sent[2][1]][0], str)

	def _voice(self, sent, varsDict, funcID):
		id1 = sent[2]
		id1, id1 = self._get_var(id1, id1, varsDict, funcID)
		bl = self.labyrinth.voice(id1[1])


	def _make_records(self, sentence):
		log(sentence)
		for sent in sentence:
			record = sent[1]
			if len(record[1]) == 7:
				id = record[1][1]
				info = record[1][3]
				cn = record[1][6]
				if record[1][5] == 'FROM':
					cn = ('CF', cn)
				if record[1][5] == 'TO':
					cn = ('CT', cn)
				self.recDict[id] = (info, cn)
			if len(record[1]) == 4:
				id = record[1][1]
				info = record[1][3]
				self.recDict[id] = (info)
			if len(record[1]) == 8:
				id = record[1][1]
				info = record[1][3]
				cnt = record[1][5]
				cnf = record[1][7]
				self.recDict[id] = (info, ('CT', cnt), ('CF', cnf))
			log(sent)
		
		

	def _get_fromDict(self, params, paramsLst, varsDict, funcID):
		if isinstance(params[1], tuple):
			paramsLst.append((params[0][1], varsDict[params[0][1]]))
			return self._get_fromDict(params[1], paramsLst, varsDict, funcID)
		else:
			params2 = params
			try:
				id = varsDict[params[1]][0]
				params2 = varsDict[params[1]]
				id = params[1]
			except BaseException:
				id = params[0]
				params2 = params
			paramsLst.append((id, params2))
			return paramsLst
		
	def _move(self, sent, varsDict, funcID):
		direct = sent[1]
		steps = sent[2]
		if steps[0] == 'ID':
			steps, steps = self._get_var(steps, steps, varsDict, funcID)
		if steps[0] == 'BINOP':
			steps = self._binop(steps, varsDict, funcID)
		if direct == 'MOVEUP':
			self.labyrinth.move(int(steps[1]), 'up')
		if direct == 'MOVEDOWN':
			self.labyrinth.move(int(steps[1]), 'down')
		if direct == 'MOVELEFT':
			self.labyrinth.move(int(steps[1]), 'left')
		if direct == 'MOVERIGHT':
			self.labyrinth.move(int(steps[1]), 'right')
		log(sent)

	def _ping(self, sent, varsDict, funcID):
		direct = sent[1]
		steps = sent[2]
		save_id = steps[1]
		if steps[0] == 'BINOP':
			res = steps = self._binop(steps, varsDict, funcID)
		steps, steps = self._get_var(steps, steps, varsDict, funcID)
		if steps is not None:
			steps = self._cast(steps, 'boolean', varsDict, funcID)
		if steps is None:
			steps = (0, 'UNDEF')
		#steps = self._cast
		if direct == 'PINGUP':
			res = self.labyrinth.ping(str(steps[1]).upper(), 'up')
		if direct == 'PINGDOWN':
			res = self.labyrinth.ping(str(steps[1]).upper(), 'down')
		if direct == 'PINGLEFT':
			res = self.labyrinth.ping(str(steps[1]).upper(), 'left')
		if direct == 'PINGRIGHT':
			res = self.labyrinth.ping(str(steps[1]).upper(), 'right')
		varsDict[save_id] = ('NUM', res)
		log(sent)

	

	def _assigment(self, sentence, varsDict, funcID):
		log(sentence)
		id = sentence[1][1]
		var = sentence[2]
		var2 = None
		if len(sentence) > 3:
			var2 = sentence[3]
		if var == 'UNDEF':
			varsDict[id] = (varsDict[id][0], var)
			return 0
		place = 0
		if var == 'PLACE':
			place = sentence[3]
			var = sentence[4]
			id = sentence[1]
			id_rem = sentence[1][1]
			id, id = self._get_var(id, id, varsDict, funcID)
			flagR = False
			if (id is not None) and (id[0] in self.recDict):
				if place[0] == 'ID':
					inplace = place[1]
					if inplace in varsDict[id_rem][1]:
						if varsDict[id_rem][1][inplace][0] == 'NUMERIC' or  varsDict[id_rem][1][inplace][0] == 'NUM':
							if var[0] == 'NUM':
								varsDict[id_rem][1][inplace] = var
							if var[0] == 'boolean':
								var = self._cast(var, 'NUM', varsDict, funcID)
						if varsDict[id_rem][1][inplace][0] == 'boolean':
							if var[0] == 'boolean':
								varsDict[id_rem][1][inplace] = var
							if var[0] == 'NUM':
								var = self._cast(var, 'boolean', varsDict, funcID)
					else:
						print(ERROR_LIST[3] + " В структуре : " + id[0])
						raise RuntimeError
				return 0
			if place[0] == 'BINOP':
				place = self._binop(place, varsDict, funcID)
			else:
				if place[0] != 'ID':
					var, var = self._get_var(var, var, varsDict, funcID)
					varsDict[id_rem][1][int(place[1])] = var
					lst = varsDict[id_rem][1]
					varsDict[id] = (sentence[4][0], lst, varsDict[id_rem][2])
				if place[0] == 'ID':
					place = varsDict[place[1]]
					var, var = self._get_var(var, var, varsDict, funcID)
					varsDict[id_rem][1][int(place[1])] = var
					lst = varsDict[id_rem][1]
					varsDict[id_rem] = (sentence[4][0], lst, varsDict[id_rem][2])
				return 0
		if var2 == 'PLACE':
			place = sentence[4][1]
			id = sentence[1]
			id1 = sentence[2]
			data = varsDict[id1]
			if data[0] in self.recDict:
				if place in data[1]:	
					inf = data[1][place]
					id, id = self._get_var(id, id, varsDict, funcID)
					if id[0] == inf[0]:
						varsDict[place] = inf
					if id[0] != inf[0]:
						inf = self._cast(inf, id[0], varsDict, funcID)
						varsDict[sentence[1][1]] = inf
			else:
				print(ERROR_LIST[3] + " В структуре : " + id[0])
				raise RuntimeError
				return 0
		log(var)
		if var[0] == 'BINOP':
			var = self._binop(var, varsDict, funcID)
		if var[0] == 'UNARY':
			log(var)
			var = self._unary(var, varsDict, funcID)
		if var[0] == 'ID':
			var = self._cast_var(var, varsDict, funcID)
		if len(varsDict[id]) == 3:
			log(varsDict[id])
		id_rem = varsDict[id]
		id_rem, id_rem = self._get_var(id_rem, id_rem, varsDict, funcID)
		if id_rem[0] != var[0]:
			var = self._cast(var, id_rem[0], varsDict, funcID)
		if var[0] == 'boolean':
			if var[1] == 'TRUE':
				var = (var[0], True)
			if var[1] == 'FALSE':
				var = (var[0], False)
		varsDict[id] = (var[0], var[1])
		
	def _unary(self, sentence, varsDict, funcID):
		return (sentence[2][0], '-' + sentence[2][1])

############## Write an error check for future #####################
	def _call_func(self, funcID, funcParams):
		localVariables = {}
		params = self.prog[funcID][1][3]
		paramLstP = []
		paramLstP = self._get_params(params, paramLstP)
		q1 = leng(paramLstP)
		q2 = leng(funcParams)
		if q1 != q2:
			print(ERROR_LIST[5] + " (кол-во принятых != кол-во принмаемых) : " + funcID)
			raise RuntimeError
		else:
			if paramLstP is not None:
				for i in range(len(paramLstP)):
					typ = paramLstP[i][0]
					typ2 = funcParams[i][1][0]
					log(typ2)
					if typ == 'NUMERIC':
						typ = 'NUM'
					if typ2 == 'NUMERIC':
						typ2 = 'NUM'
					if typ != typ2:
						if typ == 'UNDEF':
							typ = typ2
							if len(paramLstP[i]) == 3:
								ind = paramLstP[i][2]
							if len(paramLstP[i]) == 2:
								ind = paramLstP[i][1]
							data = funcParams[i][1][1]
							localVariables[ind] = (typ, data)
							continue
					if typ == typ2:
						if len(paramLstP[i]) == 3:
							ind = paramLstP[i][2]
						if len(paramLstP[i]) == 2:
							ind = paramLstP[i][1]
						data = funcParams[i][1][1]
						localVariables[ind] = (typ, data)
						continue
################## Think about casting ###################
					if typ != typ2:
						print(ERROR_LIST[2], 'In: ', funcID)
						raise RuntimeError
		
		val = self._sentencess(self.prog[funcID][1][5], localVariables, funcID) 
		val = []
		for i in range(len(paramLstP)):
			if paramLstP[i][1] == '&':
				id = paramLstP[i][2]
				item = localVariables[id]
				val.append((id, '&', (item[0], item[1])))
			else:
				id = paramLstP[i][1]
				item = localVariables[id]
				val.append((id, (item[0], item[1])))
		for item in localVariables:
			print("%s : %s" % (item, localVariables[item]))

		return val

	


	def _get_params(self, params, paramLst):
		if params is None:
			return []
		if len(params) == 3 and params[2] == '&':
			paramLst.append((params[0], params[2], params[1][1]))
			return paramLst
		if len(params) == 3:
			paramLst.append((params[0], params[1][1]))
			return self._get_params(params[2], paramLst)
		if len(params) == 4:
			paramLst.append((params[0], params[2], params[1][1]))
			return self._get_params(params[3], paramLst)
		if len(params) == 2:
			paramLst.append((params[0], params[1][1]))
			return paramLst
			
################# Try to catch a loop, if dict doesn't change #########################
	def _logic(self, sentence, varsDict, funcID):
		flag = self._lexps(sentence[1], varsDict, funcID)
		lstNow = varsDict.keys()
		while flag:
			localDict = varsDict.copy()
			if sentence[2][0] == 'SENTGROUP':
				self._sentencess(sentence[2], localDict, funcID)
				flag = self._lexps(sentence[1], localDict, funcID)
				lstVal1 = list(localDict.values())
				lstVal2 = list(varsDict.values())
				flagOut = False
				if len(lstVal1) != len(lstVal2):
					flagOut = True
				else:
					for i in range(len(lstVal1)):
						if lstVal1[i] != lstVal2[i]:
							flagOut = True
					
				if flagOut == True:
					updict = {}
					for key in lstNow:
						updict[key] = localDict[key]
					varsDict.update(updict)
					

			else:
				self._sentencess([sentence[2]], localDict, funcID)
				flag = self._lexps(sentence[1], localDict, funcID)
				lstVal1 = list(localDict.values())
				lstVal2 = list(varsDict.values())
				flagOut = False
				for i in range(len(lstVal1)):
					if lstVal1[i] != lstVal2[i]:
						flagOut = True
				
				if flagOut == True:
					updict = {}
					for key in lstNow:
						updict[key] = localDict[key]
					varsDict.update(updict)
		
		

	def _lexps(self, sentence, varsDict, funcID):
		log(sentence)
		zn = sentence[1]
		id1 = sentence[2]
		id2 = sentence[3]
		while True:
			if id1[0] == 'BINOP':
				id1 = self._binop(id1, varsDict, funcID)
				log(id1)
				continue
			if id2[0] == 'BINOP':
				id2 = self._binop(id2, varsDict, funcID)
				log(id2)
				continue
			if id1[0] == 'ID':
				id1 = self._cast_var(id1, varsDict, funcID)
				log(id1)
				continue
			if id2[0] == 'ID':
				id2 = self._cast_var(id2, varsDict, funcID)
				log(id2)
				continue

			if id1[0] == 'boolean':
				if id1[1] == 'TRUE':
					id1 = (id1[0], True)
				if id1[1] == 'FALSE':
					id1 = (id1[0], False)
			if id2[0] == 'boolean':
				if id2[1] == 'TRUE':
					id2 = (id2[0], True)
				if id2[1] == 'FALSE':
					id2 = (id2[0], False)

			flagCL = False
			flagCR = False
			zn = sentence[1]
			if len(zn) == 2:
				if zn[0] == '.':
					flagCL = True
					zn = zn[1]
				else:
					flagCR = True
					zn = zn[0]
			log(zn)

			id1, id2 = self._get_var(id1, id2, varsDict, funcID)

			if zn == '?':
				if (id1[1] == 'UNDEF')  or (id2[1] == 'UNDEF'):
					if (id1[1] == 'UNDEF') and (id2[1] == 'UNDEF'):
						flag = True
					else:
						flag = False
					return flag
				if flagCR:
					id1 = self._cast(id1, id2[0], varsDict, funcID)
				if flagCL:
					id2 = self._cast(id2, id1[0], varsDict, funcID)
				if id1[0] == 'STRING' or id2[0] == 'STRING':
					if (id1[0] == 'STRING') and (id2[0] == 'STRING'):
						if id1[1] == id2[1]:
							return True
						else:
							return False
					else:
						flag = False
					return flag
				if int(id1[1]) == int(id2[1]):
					flag = True
				else:
					flag = False
				log(flag)
				return flag
			if zn == '>':
				if (id1[1] == 'UNDEF')  or (id2[1] == 'UNDEF'):
					flag = False
					return flag
				if flagCR:
					id1 = self._cast(id1, id2[0], varsDict, funcID)
				if flagCL:
					id2 = self._cast(id2, id1[0], varsDict, funcID)
				if int(id1[1]) > int(id2[1]):
					flag = True
				else:
					flag = False
				log(flag)
				return flag
			if zn == '<':
				if (id1[1] == 'UNDEF')  or (id2[1] == 'UNDEF'):
					flag = False
					return flag
				if flagCR:
					id1 = self._cast(id1, id2[0], varsDict, funcID)
				if flagCL:
					id2 = self._cast(id2, id1[0], varsDict, funcID)
				if int(id1[1]) < int(id2[1]):
					flag = True
				else:
					flag = False
				log(flag)
				return flag
			if zn == '!':
				if (id1[1] == 'UNDEF')  or (id2[1] == 'UNDEF'):
					if (id1[1] == 'UNDEF') and (id2[1] == 'UNDEF'):
						flag = False
					else:
						flag = True
					return flag
				if flagCR:
					id1 = self._cast(id1, id2[0], varsDict, funcID)
				if flagCL:
					id2 = self._cast(id2, id1[0], varsDict, funcID)
				if int(id1[1]) != int(id2[1]):
					flag = True
				else:
					flag = False
				log(flag)
				return flag
		

	def _binop(self, sentence, varsDict, funcID):
		log(sentence)
		var = 0
		while True:
			if sentence[2][0] == 'BINOP':
				var = self._binop(sentence[2], varsDict, funcID)
				if len(sentence) == 4:
					sentence = (sentence[0], sentence[1], var, sentence[3])
				if len(sentence) == 3:
					sentence = (sentence[0], sentence[1], var)
				log(sentence)
				continue

			if sentence[2][0] == 'UNARY':
				var = self._unary(sentence[2], varsDict, funcID)
				if len(sentence) == 5:
					sentence = (sentence[0], sentence[1], var, sentence[3],  sentence[4])
					continue
				if len(sentence) == 4:
					sentence = (sentence[0], sentence[1], var, sentence[3])
					continue

			if len(sentence) >= 4 and sentence[3][0] == 'BINOP':
				var = self._binop(sentence[3], varsDict, funcID)
				sentence = (sentence[0], sentence[1], sentence[2], var)
				log(sentence)
				#return self._binop(sentence, varsDict, funcID)
				continue

			else:
				flagCL = False
				flagCR = False
				zn = sentence[1]
				if len(zn) == 2:
					if zn[0] == '.':
						flagCL = True
						zn = zn[1]
					else:
						flagCR = True
						zn = zn[0]
				log(zn)

				if zn == '+':
					id1 = sentence[2]
					id2 = sentence[3]
					id1, id2 = self._get_var(id1, id2, varsDict, funcID)
					if flagCR:
						id1 = self._cast(id1, id2[0], varsDict, funcID)
					if flagCL:
						id2 = self._cast(id2, id1[0], varsDict, funcID)
					if (id1[1] != 'UNDEF') and (id2[1] != 'UNDEF'):
						log(str(int(id1[1]) + int(id2[1])))	
					if id1[0] == 'NUM':
						if (id1[1] == 'UNDEF') or (id2[1] == 'UNDEF'):
							return ('NUM', 'UNDEF')
						return ('NUM', int(id1[1]) + int(id2[1]))
					if id1[0] == 'boolean':
						if (id1[1] == 'UNDEF') or (id2[1] == 'UNDEF'):
							return ('boolean', 'UNDEF')
						res = int(id1[1]) + int(id2[1])
						if res:
							res = True
						else:
							res = False
						return ('boolean', res)

				if zn == '-':
					id1 = sentence[2]
					id2 = sentence[3]
					id1, id2 = self._get_var(id1, id2, varsDict, funcID)
					if flagCR:
						id1 = self._cast(id1, id2[0], varsDict, funcID)
					if flagCL:
						id2 = self._cast(id2, id1[0], varsDict, funcID)
					if (id1[1] != 'UNDEF') and (id2[1] != 'UNDEF'):
						log(str(int(id1[1]) - int(id2[1])))	
					if id1[0] == 'NUM':
						if (id1[1] == 'UNDEF') or (id2[1] == 'UNDEF'):
							return ('NUM', 'UNDEF')
						return ('NUM', int(id1[1]) - int(id2[1]))
					if id1[0] == 'boolean':
						if (id1[1] == 'UNDEF') or (id2[1] == 'UNDEF'):
							return ('boolean', 'UNDEF')
						res = int(id1[1]) - int(id2[1])
						if res:
							res = True
						else:
							res = False
						return ('boolean', res)
				
				if zn == '*':
					id1 = sentence[2]
					id2 = sentence[3]
					id1, id2 = self._get_var(id1, id2, varsDict, funcID)
					if flagCR:
						id1 = self._cast(id1, id2[0], varsDict, funcID)
					if flagCL:
						id2 = self._cast(id2, id1[0], varsDict, funcID)
					if (id1[1] != 'UNDEF') and (id2[1] != 'UNDEF'):
						log(str(int(id1[1]) * int(id2[1])))						
					if id1[0] == 'NUM':
						if (id1[1] == 'UNDEF') or (id2[1] == 'UNDEF'):
							return ('NUM', 'UNDEF')
						return ('NUM', int(id1[1]) * int(id2[1]))
					if id1[0] == 'boolean':
						if (id1[1] == 'UNDEF') or (id2[1] == 'UNDEF'):
							if id1[1] == 'UNDEF' and id2[1] == True:
								return ('boolean', 'UNDEF')
							if id1[1] == 'UNDEF' and id2[1] == False:
								return ('boolean', False)
							if id2[1] == 'UNDEF' and id1[1] == True:
								return ('boolean', 'UNDEF')
							if id2[1] == 'UNDEF' and id1[1] == False:
								return ('boolean', False)
						res = int(id1[1]) * int(id2[1])
						if res:
							res = True
						else:
							res = False
						return ('boolean', res)
	
				if zn == '/':
					id1 = sentence[2]
					id2 = sentence[3]
					id1, id2 = self._get_var(id1, id2, varsDict, funcID)
					if flagCR:
						id1 = self._cast(id1, id2[0], varsDict, funcID)
					if flagCL:
						id2 = self._cast(id2, id1[0], varsDict, funcID)
					if (id1[1] != 'UNDEF') and (id2[1] != 'UNDEF'):
						log(str(int(id1[1]) / int(id2[1])))	
					if id1[0] == 'NUM':
						if (id1[1] == 'UNDEF') or (id2[1] == 'UNDEF'):
							return ('NUM', 'UNDEF')
						return ('NUM', int(id1[1]) / int(id2[1]))
					if id1[0] == 'boolean':
						if (id1[1] == 'UNDEF') or (id2[1] == 'UNDEF'):
							return ('boolean', 'UNDEF')
						res = int(id1[1]) / int(id2[1])
						if res:
							res = True
						else:
							res = False
						return ('boolean', res)

				if zn == '^':
					id1 = sentence[2]
					id2 = sentence[3]
					id1, id2 = self._get_var(id1, id2, varsDict, funcID)
					if flagCR:
						id1 = self._cast(id1, id2[0], varsDict, funcID)
					if flagCL:
						id2 = self._cast(id2, id1[0], varsDict, funcID)
					if (id1[1] != 'UNDEF') and (id2[1] != 'UNDEF'):
						log(str(int(id1[1]) ** int(id2[1])))	
					if id1[0] == 'NUM':
						if (id1[1] == 'UNDEF') or (id2[1] == 'UNDEF'):
							return ('NUM', 'UNDEF')
						return ('NUM', int(id1[1]) ** int(id2[1]))
					if id1[0] == 'boolean':
						if (id1[1] == 'UNDEF') or (id2[1] == 'UNDEF'):
							return ('boolean', 'UNDEF')
						res = int(id1[1]) ** int(id2[1])
						if res:
							res = True
						else:
							res = False
						return ('boolean', res)
		
	def _get_var(self, id1, id2, varsDict, funcID):
		ind1 = id1[0]
		ind2 = id2[0]
		if ind1 != ind2:
			if ind1 == 'ID':
				id1 = self._cast_var(id1, varsDict, funcID)	
				ind1 = id1[0]		
			if ind2 == 'ID':
				id2 = self._cast_var(id2, varsDict, funcID)
				ind2 = id2[0]	
			
			if ind1 == 'NUM' and ind2 == 'boolean':
				if (id2[1] == 'TRUE') or (id2[1] == True):
					id2 = ('NUM', 1)
					return id1, id2
				if (id2[1] == 'FALSE') or (id2[1] == False):
					id2 = ('NUM', 0)
					return id1, id2
				if id2[1] == 'UNDEF':
					id2 = ('NUM', 'UNDEF')
					return id1, id2

			if ind1 == 'boolean' and ind2 == 'NUM':
				if id2[1] == 0:
					id2 = ('boolean', False)
					return id1, id2
				else:
					id2 = ('boolean', True)
					return id1, id2
			
			else:
				return id1, id2			

		if ind1 == ind2 and ind1 == 'ID':
			id1 = self._cast_var(id1, varsDict, funcID)	
			id2 = self._cast_var(id2, varsDict, funcID)
			return id1, id2
		
		else:
			return id1, id2
			
	def _cast(self, id, to_cast, varsDict, funcID):
		if to_cast == 'boolean':
			if id[1] == 'UNDEF':
				id = ('boolean', 'UNDEF')
				return id
			if (id[1] == 0) or (id[1] == '0'):
				id = ('boolean', False)
			else:
				id = ('boolean', True)
		if to_cast == 'NUM':
			if id[1] == 'UNDEF':
				id = ('NUM', 'UNDEF')
				return id
			if (id[1] == False) or (id[1] == 'FALSE'):
				id = ('NUM', 0)
			else:
				id = ('NUM', 1)
		if to_cast == 'STRING':
			if id[0] == 'STR':
				id = ('STRING', id[1])
		return id

	def _cast_var(self, id, varsDict, funcID):
		if id[1] in varsDict:
			log(id[1])
			if varsDict[id[1]][0] == 'UNDEF' or varsDict[id[1]][0] == 'str':
				if funcID == 1:
					print(ERROR_LIST[9], 'In Main Body')
					raise RuntimeError
				else:
					print(ERROR_LIST[9], 'In ', funcID)
					raise RuntimeError
			if varsDict[id[1]][0] == 'STRING':
				return ('STRING', varsDict[id[1]][1])
			if varsDict[id[1]][0] == 'NUM' or varsDict[id[1]][0] == 'NUMERIC':
				return ('NUM', varsDict[id[1]][1])
			if varsDict[id[1]][0] == 'boolean':
				return ('boolean', varsDict[id[1]][1])
			else:
				typ = varsDict[id[1]][0]
				if typ in self.recDict:
					return (typ, varsDict[id[1]][1])
				

	def _define_variables(self, sentence, varsDict, funcID):
		expected_type = sentence[1]
		var = sentence[2][1]
		log(var)
		if var in varsDict:
			self.syntErrors += 1
			if funcID == 1:
				print(ERROR_LIST[14], 'In ', 'MAIN BODY')
			else:
				print(ERROR_LIST[14], 'In ', funcID)
			raise RuntimeError
		else:
			if expected_type in self.recDict:
				data = self.recDict[expected_type][0]
				val = {}
				self._get_fromRec(data, val)
				if expected_type == 'STR':
					expected_type = 'STRING'
				varsDict[var] = (expected_type, val)
			elif len(sentence) == 5:
				varsDict[var] = (expected_type, ['X' for i in range(int(sentence[4]))], sentence[4])
			else:
				if expected_type == 'STR':
					expected_type = 'STRING'
				varsDict[var] = (expected_type, 'UNDEF')
		#for var in sentence[2]:
		#	if var[2] is None:		
		#		varsDict[var[1]] = (expected_type, var[2])
		#	else:
		#		varsDict[var[1]] = self._exps(var[2], varsDict, expected_type)


	def _get_fromRec(self, data, val):
		if len(data) == 2:	
			val[data[1][1]] = (data[0], 'UNDEF')
			return val
		else:
			val[data[1][1]] = (data[0], 'UNDEF')
			return self._get_fromRec(data[2], val)

	def _check_SyntaxError(self):
		if 0 in self.prog:
			print('-----WRONG FUNCS------')
			self.syntErrors += len(self.prog[0])
			for it in self.prog[0]:
				print(it[1])
			print('-----SYNTAX ERRORS----')

		for func in self.prog:
			if (func != 0 and func != 1 and func != 2):
				print(str(self.prog[func][1][5]))
				for sent in self.prog[func][1][5][1]:
					print(sent)
					if sent[1] is None:
						continue
					if sent[1][0] == 'LOGIC':
						print(sent)
						sentL = sent[1][2]
						self._find_ERR(sentL)
					if sent[1][0] == 'ERR':
						print(sent[1][1])
						self.syntErrors += 1
			
			if func == 1:
				print(str(self.prog[func][0][1]))
				for sent in self.prog[func][0][1][1]:
					print(sent)
					if sent[1][0] == 'LOGIC':
						print(sent)
						sentL = sent[1][2]
						self._find_ERR(sentL)
					if sent[1][0] == 'ERR':
						print(sent[1][1])
						self.syntErrors += 1

	
	def _find_ERR(self, sent):
		for sentence in sent[1]:
			print(sentence)
			if sent[1][0] == 'LOGIC':
				sentL = sent[1][2]
				self._find_ERR(sentL)
			if sentence[1][0] == 'ERR':
				print(sentence[1][1])
				self.syntErrors += 1