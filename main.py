import subprocess

def get_formula(n: int):
	constraints = []

	# генерируем клозы, отвечающие за то, что никакие два ферзя не стоят в одном столбце или одной строке
	for i in range(n):
		for j in range(n):
			for k in range(j + 1, n):
				constraints.append(((i, j), (i, k)))
				constraints.append(((j, i), (k, i)))

	# генерируем клозы, отвечающие за то, что никакие два ферзя не стоят на одной диагонали
	for summ in range(2 * n - 1):
		for i in range(max(summ - n + 1, 0), min(summ + 1, n)):
			for j in range(i + 1, min(summ + 1, n)):
				constraints.append(((i, summ - i), (j, summ - j)))
	for diff in range(-n + 1, n):
		for i in range(max(-diff, 0), min(n - diff, n)):
			for j in range(i + 1, min(n - diff, n)):
				constraints.append(((i, i + diff), (j, j + diff)))
	
	# генирируем клозы, отвечающие за то, что в любой строке стоит хотя бы один ферзь
	clauses = []
	for i in range(n):
		disjunction = [(i, j) for j in range(n)]
		clauses.append(disjunction)

	return constraints, clauses

def main():
	n = int(input())
	def num(p):
		fst, snd = p
		return fst * n + snd + 1 

	constraints, clauses = get_formula(n)

	# заполняем входной файл для sat-solvera
	input_solver_file = open('input.dimacs', 'w')
	input_solver_file.write('p cnf ' + str(n * n) + ' ' + str(len(constraints) + len(clauses)) + '\n')
	for fst, snd in constraints:
		input_solver_file.write('-' + str(num(fst)) + ' ' + '-' + str(num(snd)) + ' 0\n')
	for clause in clauses:
		clause_str = [str(num(p)) for p in clause]
		clause_str.append('0')
		s = " ".join(clause_str)
		input_solver_file.write(s + '\n')
	input_solver_file.close()

	# запускаем sat-solver
	subprocess.run(['minisat', 'input.dimacs', 'solution.txt'])

	# парсим результат работы sat-solvera и выдаём ответ
	output_solver_file = open('solution.txt', 'r')
	lines = output_solver_file.readlines()
	if lines[0] == 'SAT\n':
		model = list(map(lambda x: max(int(x) // abs(int(x)), 0), lines[1].split(' ')[:-1]))
		for i, x in enumerate(model):
			print(x, end="")
			if i % n == n - 1:
				print()
	output_solver_file.close()
	subprocess.run(['rm', 'input.dimacs'])
	result = subprocess.run(['rm', 'solution.txt'])

if __name__ == "__main__":
	main()

