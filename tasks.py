#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import signal
import sys


def handler(signum):
	print('Signal handler called with signal', signum)
	raise IOError('Interrupted!')


class Tasks:
	def __init__(self):
		self.DEBUG = False

	def first(self, values):
		"""
		Usage: tasks.py -t 1 and type input data by row \n
		tasks.py -t 1 -v 4 1.5 3 6 1.5 \n
		echo "4 1.5 3 6 1.5" | tasks.py -t 1 \n
		cat ./data_in | tasks.py -t 1

		<<<Долевое строительство>>>
		Дан набор из N долей,
		представленных в виде N рациональных. Необходимо представить эти доли в процентном выражении c точностью до трех знаков после запятой.

		Входные данные
		Первая строка содержит значение N - число долей, каждая последующая содержит числовое выражение доли.
		4
		1.5
		3
		6
		1.5

		Выходные данные N строк с процентным выражением долей. Значение в строке k является процентным выражение доли
		из строки k+1 входных данных 0.125 0.250 0.500 0.125

		:return:
		"""

		def execute(N, data):
			from fractions import Fraction
			if self.DEBUG:
				print('Input data:', '\nN={0}'.format(N), 'data={0}'.format(data), '\n')

			summary = sum(data)
			if summary == 0:
				summary = 1

			if self.DEBUG:
				print('Output:')

			for val in data:
				fr_num = Fraction(val) / Fraction(summary)
				print(format(round(fr_num.numerator / fr_num.denominator, 3), '.3f'))

			if self.DEBUG:
				print('\n')

		def check_type(data):
			try:
				data = float(data)
			except ValueError:
				print('Instance "{}" is not correct type.\nAborted!'.format(data))
				exit(1)
			else:
				if data < 0:
					print('Instance "{}" is < 0.\nAborted!'.format(data))
					exit(1)
			return data

		def get_data_from_kwrags(data):
			N = int(data[0])
			if N > len(data) - 1:
				print('Missing argument. Waiting: "{0}", received: {1}\nAborted!'.format(N, len(data) - 1))
				exit(1)

			execute(N, [check_type(i) for i in data[1:N + 1]])

			if self.DEBUG:
				print('Done.')


		def get_input_from_keyboard():
			data = []
			N = None
			for line in sys.stdin:

				for elem in line.split():
					if N:
						data.append(check_type(elem))
					else:
						N = int(check_type(elem))

				if N <= len(data):
					execute(N, data[:N])
					if self.DEBUG:
						print('N=', N, 'Data=', data)
					N = None
					data = []
					break  # for stopping read next data

		if values:
			get_data_from_kwrags(values)
		else:
			get_input_from_keyboard()

	def second(self, values):
		"""
		Usage: tasks.py -t 2 and type input data by row \n
		cat ./data_in.txt | tasks.py -t 2 \n
		<<<Мегатрейдер>>>
		Допустим, что на рынке существует некое множество облигаций с номиналом 1000 условных
		единиц, по которым каждый день выплачивается купон размером 1 уе. Погашение номинала облигации (то есть
		выплата 1000 условных единиц) происходит в конце срока. Каждая облигация на рынке характеризуется названием (
		некая строка) и ценой, цена выражается в виде процентов от номинала, то есть цена 98.5 соответствует цене 98,
		5% * 1000 = 985 условных единиц. У некоего трейдера есть информация о том какие предложения по облигациям
		будут на рынке в ближайшие N дней. По каждому дню он знает, какие лоты будут представлены на бирже: название
		облигации, цену и количество в штуках. Каждый день на рынке может быть от 0 до M лотов. Трейдер располагает
		суммой денежных средств в количестве S. Необходимо определить какие лоты в какие дни нужно купить,
		чтобы получить максимальный доход с учетом следующих условий: 1.	Трейдер может только покупать облигации.
		Купленные облигации не продаются. 2.	Трейдер может купить только весь лот целиком при наличии доступных
		денежных средств. 3.	Выплаченные купоны по купленным облигациям не реинвестируются, то есть не увеличивают
		сумму доступных денежных средств. 4.	Все купленные облигации будут погашены в день N+30. 5.	Доход
		рассчитывается на день N+30, то есть после погашения облигаций. Входные данные На первой строке будут даны
		числа N, M и S. Далее будет идти k строк вида “<день> <название облигации в виде строки без пробелов> <цена>
		<количество>”. Ввод будет завершен пустой строкой.

		2 2 8000
		1 alfa-05 100.2 2
		2 gazprom-17 100.0 2
		2 alfa-05 101.5 5


		Выходные данные В первой строке необходимо указать сумму дохода, полученного трейдером на день N+30. В
		последующих строках привести купленные лоты в таком же формате, который используется во входных данных.
		Последняя строка должна быть пустой.

		135
		2 gazprom-17 100.0 2
		2 alfa-05 101.5 5


		Программа реализована с использованием хэш-таблицы (Matrix),
		т. е. для каждого веса, если существует набор с таким весом, а также храниться максимальная стоимость. Начиная с
		пустого множества частичных наборов {0:}, и добавляя по одному, предметы, в каждый момент мы имеем
		«лучшие» частичные наборы, укладывающихся в сумму. В конце остается только выбрать самый дорогой из них с большим
		выигрышем. Таким образом, сложность этого алгоритма — O(nS) является экспоненциальной от длины входа, при ограниченных
		размерах бюджета S

		"""

		def knapsack(S, Sizes, Weights):
			Matrix = {0: 0}
			Solutions = {0: []}
			for i in range(0, len(Sizes)):
				Matrix_old = dict(Matrix)
				for x in Matrix_old:
					if (x + Sizes[i]) <= S:
						if (not x + Sizes[i] in Matrix) or (Matrix[x + Sizes[i]] < Matrix_old[x] + Weights[i]):
							Matrix[x + Sizes[i]] = Matrix_old[x] + Weights[i]
							Solutions[x + Sizes[i]] = Solutions[x] + [i]

			indexes = Solutions[
				(list(Matrix.keys())[
					 list(Matrix.values()).index(max(Matrix.values()))])]  # python3 get val from key by max(value)
			return indexes, max(Matrix.values())

		def get_ye(val):
			return float(format((val / 100) * 1000, '.3f'))

		def get_profit(N, day, price, count):
			res = (((N - day) + 30) * count) - ((get_ye(price) - 1000) * count)
			return float(format(res, '.3f'))

		def get_input_from_stdin():
			data = []
			sizes = []
			weights = []

			if self.DEBUG:
				print('Waiting input data in one line: N M S ')
			N, M, S = sys.stdin.readline().split()  # N = day S = money
			N = int(N)  # day
			M = int(M)  # lot
			S = float(S)  # money

			if self.DEBUG:
				print('Input data:\nN = {0} M = {1} S = {2}'.format(N, M, S))
				print('Waiting input data in one line:  Day, Name, Price, Count')
			for line in sys.stdin:
				if line == '\n':
					if self.DEBUG:
						print('Aborted!')
					break
				day, name, price, count = line.split()
				day = int(day)
				name = str(name)
				price = float(price)
				count = int(count)
				d = [day, name, price, count]
				data.append(d)
				sizes.append(get_ye(price) * count)
				weights.append(get_profit(N, day, price, count))

			if self.DEBUG:
				print('Data = ', data)

			index, res = knapsack(S, sizes, weights)
			print(('%.15f' % res).rstrip('0').rstrip('.'))
			for i in index:
				print(data[i][0], data[i][1], data[i][2], data[i][3])
			print('\n')

			if self.DEBUG:
				print('Done.')

		get_input_from_stdin()


if __name__ == '__main__':

	tasks = Tasks()
	signal.signal(signal.SIGALRM, handler)

	parser = argparse.ArgumentParser(
		description='The package is a solution of some algorithmic problems.')

	parser.add_argument('-t', '--task', help='Number of task: 1 or 2', type=int, required=True)
	parser.add_argument('-v', '--values', help='Input data', nargs='+')
	parser.add_argument('-d', '--debug', help="Debug: 1 or 0", type=int, default=0)
	parser.add_argument('-i', '--info', help="Show task description: 1 or 0", type=int, default=0)

	args = parser.parse_args()

	if len(sys.argv) < 1:
		parser.print_usage()
		sys.exit(1)

	if args.debug == 1:
		print("[Debug]: ON")
		tasks.DEBUG = True

	if args.info == 1:
		if args.task == 1:
			help(tasks.first)
		if args.task == 2:
			help(tasks.second)
		exit(0)
	if args.task == 1:
		tasks.first(args.values)

	if args.task == 2:
		tasks.second(args.values)
