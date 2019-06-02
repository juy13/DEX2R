import os
import sys


file = 'traceP.txt'

class LabirynthClass:
	
	def __init__(self, fname='LabMap.dex'):
		self.filename = fname
		self.labymap = []
		self.password = {}
		self.traceRb = []
		self.coordOut = []
		self.robotPosI = None
		self.robotPosJ = None
		self.OutPosI = None
		self.OutPosJ = None
		self.inited = False
		self.ended = False
		self.first = 0
		self.lines = 0
		self.elems = 0
		self.vert  = 0
		self.file = file
		self.init_labyrinth()

	def init_trace(self, file_came):
		self.file = file_came
		return 0

	def close_trace(self):
		#self.handle.close()
		return 0

	def trace(self, came):
		with open(self.file, 'a') as handle:
			handle.write(came)
		self.traceRb.append(came)


	def init_labyrinth(self):
		try:
			file = open(self.filename, 'r')
		except FileNotFoundError:
			self.inited = False
			return
	
		flag = False
		i = 0
		for line in file:
			if flag == True:
				self.password[self.coordOut[i][0]] = line
			if line == 'MATRIXX\n':
				flag = True
				i = 0
			if flag == False:
				if (line.find('7') != -1):
					j = line.find('7')
					self.coordOut.append((i, j))
				self.labymap.append(line)
				i += 1
			
				
		file.close()
		self.lines = len(self.labymap)
		self.vert = len(self.labymap[0])
		for i in range(len(self.labymap)):
			for j in range(len(self.labymap[0])):
				if self.labymap[i][j] == '2':
					self.robotPosI = i
					self.robotPosJ = j
				if self.labymap[i][j] == '7':
					self.OutPosI = i
					self.OutPosJ = j
		self.inited = True

	
	def vision(self):
		i = self.robotPosI
		return self.password[i]
	
	def voice(self, str):
		if str in self.password.values():
			return True
		else:
			return False


	def move(self, steps, direct):
		flag = False
		if direct == 'up':
			before = steps
			for st in range(steps):
				if self.labymap[self.robotPosI][self.robotPosJ] == '1' or self.labymap[self.robotPosI][self.robotPosJ] == '7':
					self.robotPosI = self.robotPosI + 1
					flag = True
					break
				self.robotPosI = self.robotPosI - 1
				before = before - 1
				if (flag != True) and (self.labymap[self.robotPosI][self.robotPosJ] == '1' or self.labymap[self.robotPosI][self.robotPosJ] == '7'):
					self.robotPosI = self.robotPosI + 1
			self.trace('MOVEUP: ' + 'robPos:' + '[' + str(self.robotPosI) + '][' + str(self.robotPosJ) + ']' + '\n')
			return before

		if direct == 'down':
			before = steps
			for st in range(steps):
				if self.labymap[self.robotPosI][self.robotPosJ] == '1' or self.labymap[self.robotPosI][self.robotPosJ] == '7':
					self.robotPosI = self.robotPosI - 1
					flag = True
					break
				self.robotPosI = self.robotPosI + 1
				before = before - 1
				if (flag != True) and (self.labymap[self.robotPosI][self.robotPosJ] == '1' or self.labymap[self.robotPosI][self.robotPosJ] == '7'):
					self.robotPosI = self.robotPosI - 1
			self.trace('MOVEDOWN: ' + 'robPos:' + '[' + str(self.robotPosI) + '][' + str(self.robotPosJ) + ']' + '\n')
			return before

		if direct == 'right':
			before = steps
			for st in range(steps):
				if self.labymap[self.robotPosI][self.robotPosJ] == '1' or self.labymap[self.robotPosI][self.robotPosJ] == '7':
					self.robotPosJ = self.robotPosJ - 1
					flag = True
					break
				self.robotPosJ = self.robotPosJ + 1
				before = before - 1
				if (flag != True) and (self.labymap[self.robotPosI][self.robotPosJ] == '1' or self.labymap[self.robotPosI][self.robotPosJ] == '7'):
					self.robotPosJ = self.robotPosJ - 1
			self.trace('MOVERIGHT: ' + 'robPos:' + '[' + str(self.robotPosI) + '][' + str(self.robotPosJ) + ']' + '\n')
			return before

		if direct == 'left':
			before = steps
			for st in range(steps):
				if self.labymap[self.robotPosI][self.robotPosJ] == '1' or self.labymap[self.robotPosI][self.robotPosJ] == '7':
					self.robotPosJ = self.robotPosJ + 1
					flag = True
					break
				self.robotPosJ = self.robotPosJ - 1
				before = before - 1
			if (flag != True) and (self.labymap[self.robotPosI][self.robotPosJ] == '1' or self.labymap[self.robotPosI][self.robotPosJ] == '7'):
					self.robotPosJ = self.robotPosJ + 1
			self.trace('MOVELEFT: ' + 'robPos:' + '[' + str(self.robotPosI) + '][' + str(self.robotPosJ) + ']' + '\n')
			return before


	def ping(self, flag, direct):
		if direct == 'up':
			start = self.robotPosI
			steps = 0
			if flag == 'TRUE':
				for st in range(self.lines):
					if steps < 0:
						self.trace('PINGUP' + '[' + '0' + ']' + '\n')
						return 0
					if self.labymap[start][self.robotPosJ] == '1':
						steps = steps - 1
						self.trace('PINGUP' + '[' + str(steps) + ']' + '\n')
						return steps
					if self.labymap[start][self.robotPosJ] == '7':
						self.trace('PINGUP' + '[' + 'UNDEF' + ']' + '\n')
						return 'UNDEF'
					start = start - 1
					steps = steps + 1

			if flag == 'FALSE':
				for st in range(self.lines):
					if steps < 0:
						self.trace('PINGUP' + '[' + '0' + ']' + '\n')
						return 0
					if self.labymap[start][self.robotPosJ] == '7':
						steps = steps - 1
						self.trace('PINGUP' + '[' + str(steps) + ']' + '\n')
						return steps
					if self.labymap[start][self.robotPosJ] == '1':
						self.trace('PINGUP' + '[' + 'UNDEF' + ']' + '\n')
						return 'UNDEF'
					start = start - 1
					steps = steps + 1

			if flag == 'UNDEF':
				for st in range(self.lines):
					if steps < 0:
						self.trace('PINGUP' + '[' + '0' + ']' + '\n')
						return 0
					if self.labymap[start][self.robotPosJ] == '7' or self.labymap[start][self.robotPosJ] == '1':
						steps = steps - 1
						self.trace('PINGUP' + '[' + str(steps) + ']' + '\n')
						return steps
					start = start - 1
					steps = steps + 1



		if direct == 'down':
			start = self.robotPosI
			steps = 0
			if flag == 'TRUE':
				for st in range(self.lines):
					if steps < 0:
						self.trace('PINGDOWN' + '[' + '0' + ']' + '\n')
						return 0
					if self.labymap[start][self.robotPosJ] == '1':
						steps = steps - 1
						self.trace('PINGDOWN' + '[' + str(steps) + ']' + '\n')
						return steps
					if self.labymap[start][self.robotPosJ] == '7':
						self.trace('PINGDOWN' + '[' + 'UNDEF' + ']' + '\n')
						return 'UNDEF'
					start = start + 1
					steps = steps + 1

			if flag == 'FALSE':
				for st in range(self.lines):
					if steps < 0:
						self.trace('PINGDOWN' + '[' + '0' + ']' + '\n')
						return 0
					if self.labymap[start][self.robotPosJ] == '7':
						steps = steps - 1
						self.trace('PINGDOWN' + '[' + str(steps) + ']' + '\n')
						return steps
					if self.labymap[start][self.robotPosJ] == '1':
						self.trace('PINGDOWN' + '[' + 'UNDEF' + ']' + '\n')
						return 'UNDEF'
					start = start + 1
					steps = steps + 1

			if flag == 'UNDEF':
				for st in range(self.lines):
					if steps < 0:
						self.trace('PINGDOWN' + '[' + '0' + ']' + '\n')
						return 0
					if self.labymap[start][self.robotPosJ] == '7' or self.labymap[start][self.robotPosJ] == '1':
						steps = steps - 1
						self.trace('PINGDOWN' + '[' + str(steps) + ']' + '\n')
						return steps
					start = start + 1
					steps = steps + 1


		if direct == 'right':
			start = self.robotPosJ
			steps = 0
			if flag == 'TRUE':
				for st in range(self.vert):
					if steps < 0:
						self.trace('PINGRIGHT' + '[' + '0' + ']' + '\n')
						return 0
					if self.labymap[self.robotPosI][start] == '1':
						steps = steps - 1
						self.trace('PINGRIGHT' + '[' + str(steps) + ']' + '\n')
						return steps							
					if self.labymap[self.robotPosI][start] == '7':
						self.trace('PINGRIGHT' + '[' + 'UNDEF' + ']' + '\n')
						return 'UNDEF'
					start = start + 1
					steps = steps + 1

			if flag == 'FALSE':
				for st in range(self.vert):
					if steps < 0:
						self.trace('PINGRIGHT' + '[' + '0' + ']' + '\n')
						return 0
					if self.labymap[self.robotPosI][start] == '7':
						steps = steps - 1
						self.trace('PINGRIGHT' + '[' + str(steps) + ']' + '\n')
						return steps						
					if self.labymap[self.robotPosI][start]== '1':
						self.trace('PINGRIGHT' + '[' + 'UNDEF' + ']' + '\n')
						return 'UNDEF'
					start = start + 1
					steps = steps + 1

			if flag == 'UNDEF':
				for st in range(self.vert):
					if steps < 0:
						self.trace('PINGRIGHT' + '[' + '0' + ']' + '\n') 
						return 0
					if self.labymap[self.robotPosI][start] == '7' or self.labymap[self.robotPosI][start] == '1':
						steps = steps - 1
						self.trace('PINGRIGHT' + '[' + str(steps) + ']' + '\n')
						return steps
					start = start + 1
					steps = steps + 1


		if direct == 'left':
			start = self.robotPosJ
			steps = 0
			if flag == 'TRUE':
				for st in range(self.vert):
					if steps < 0:
						self.trace('PINGLEFT' + '[' + '0' + ']' + '\n')
						return 0
					if self.labymap[self.robotPosI][start] == '1':
						steps = steps - 1
						self.trace('PINGLEFT' + '[' + str(steps) + ']' + '\n')
						return steps
					start= start - 1
					steps = steps + 1

			if flag == 'FALSE':
				for st in range(self.vert):
					if steps < 0:
						self.trace('PINGLEFT' + '[' + '0' + ']' + '\n')
						return 0
					if self.labymap[self.robotPosI][start] == '7':
						steps = steps - 1
						self.trace('PINGLEFT' + '[' + str(steps) + ']' + '\n')
						return steps
					if self.labymap[self.robotPosI][start] == '1':
						self.trace('PINGLEFT' + '[' + 'UNDEF' + ']' + '\n')
						return 'UNDEF'
					start = start - 1
					steps = steps + 1

			if flag == 'UNDEF':
				for st in range(self.vert):
					if steps < 0:
						self.trace('PINGLEFT' + '[' + '0' + ']' + '\n')
						return 0
					if self.labymap[self.robotPosI][start] == '7' or self.labymap[self.robotPosI][start] == '1':
						steps = steps - 1
						self.trace('PINGLEFT' + '[' + str(steps) + ']' + '\n')
						return steps
					start = start - 1
					steps = steps + 1

	def turn(self, arrow, dist):
		if dist == 'right':
			if arrow == 'right':
				return 'down'
			if arrow == 'down':
				return 'left'
			if arrow == 'left':
				return 'up'
			if arrow == 'up':
				return 'right'
		if dist == 'left':
			if arrow == 'right':
				return 'up'
			if arrow == 'down':
				return 'right'
			if arrow == 'left':
				return 'down'
			if arrow == 'up':
				return 'left'
		if dist == 'back':
			if arrow == 'right':
				return 'left'
			if arrow == 'down':
				return 'up'
			if arrow == 'left':
				return 'right'
			if arrow == 'up':
				return 'down'


	def out(self):
		right = True
		left = False
		up = False
		down = False
		arrow = 'right'
		res = None

		it = 0
		while True:
			res = self.ping('UNDEF', arrow)
			while res != 0:
				self.move(1, arrow)
				res = self.ping('UNDEF', arrow)
			arrow = self.turn(arrow, 'right')
			self.move(1, arrow)
			res = self.ping('FALSE', arrow)
			if res == 'UNDEF':
				res = self.ping('UNDEF', arrow)
				if res > 0:
					continue
				else:
					arrow_bk = self.turn(arrow, 'back')
					self.move(1, arrow_bk)
					arrow = self.turn(arrow, 'left')
					self.move(1, arrow)
					res = self.ping('UNDEF', arrow)
					if res > 0:
						continue
					else:
						arrow_bk = self.turn(arrow, 'back')
						self.move(1, arrow_bk)
						arrow = self.turn(arrow, 'left')
					continue
			if res > 0:
				self.move(res, arrow)
				str = self.vision()
				bl = self.voice(str)
				print('OUT')
				break

			
	def print_laby(self, lab):
		print('--- Labyrinth ---')
		for line in lab:
			print(line, end='')
				

if __name__ == '__main__':
	l = LabirynthClass()
	print('robPos:', '[', l.robotPosI, '][', l.robotPosJ, ']', '\n')
	l.print_laby(l.labymap)
	l.init_trace(file)
	#l.move(1, 'right')
	#l.move(3, 'up')
	#print('robPos:', '[', l.robotPosI, '][', l.robotPosJ, ']', '\n')
	#steps = l.ping('TRUE', 'up')
	#print(steps)
	l.out()
	#l.handle.close()
	#print()
	#try:
	#	algo_(l)
	#except RecursionError:
	#	print('\n\nINF RECURSION!!!')
	#except EOFError:
	#	print('Alles gut')

	