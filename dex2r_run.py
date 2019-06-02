import dex2r_interpreter as interp
import dex2r_parser as parser
import pickle

filename1 = 'try1.dex2r'
filename12 = 'try2.dex2r'
filename2 = 'escape.dex2r'
filename3 = 'simple_factorial.i2'
filename0 = 'laby_algo.i2'
filename11 = 'parseresult.out'

data = open(filename12).read()

with open('parseresult.out', 'rb') as f:
	parsed = pickle.load(f)

#parsed = parser.run_parser(data)
#if not parsed:
#	print('Что-то пошло не так, распарсить не удалось.')
#	raise SystemExit

program = interp.DexInterp(parsed)
try:
	program.run()
	raise SystemExit
except RuntimeError:
	print('Программа завершилась с ошибкой')
except SystemExit:
	print('FINISH')