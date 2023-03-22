from discord.ext import commands
class Brainfuck:
	def check(self, code):
		return [char for char in code if char in "><+-.,[]%"]

	def bracket(self, code):
		map = {}
		stack = []
		for pos, char in enumerate(code):
			if char == '[':
				stack.append(pos)
			elif char == ']':
				last_pos = stack.pop()
				map[pos] = last_pos
				map[last_pos] = pos
		return map
	
	def cp1251(self, char):
		if type(char) is str:
			if ord(char) > 255:
				try:
					return char.encode("cp1251")
				except:
					return char
			else:
				return char
		elif type(char) is int:
			try:
				return chr(char).encode("cp1252").decode("cp1251")
			except:
				return chr(char)
		else:
			return 0
			
	def run(self, code, inp=None):
		if inp:
			inp = [ord(self.cp1251(i)) for i in inp]
		code = self.check(code)
		brackets = self.bracket(code)
		memory = [0 for _ in range(256)]
		cursor = 0
		i = 0
		out = []
		open_braces = 0
		timer = 30000
		while i < len(code):
			if code[i] == ">":
				cursor += 1
			elif code[i] == "<":
				cursor -= 1
			elif code[i] == "+":
				memory[cursor] += 1
			elif code[i] == "-":
				memory[cursor] -= 1
			elif code[i] == "%":
				memory = [0 for _ in range(256)]
			elif code[i] == ".":
				char = self.cp1251(memory[cursor])
				if char != "`":
					out.append(char)
			elif code[i] == ",":
				if inp:
					memory[cursor] = inp.pop(0)
				else:
					memory[cursor] = 0
			elif code[i] == '[':
				if not memory[cursor]:
					i = brackets[i]
			elif code[i] == ']':
				if memory[cursor]:
					i = brackets[i]
			if memory[cursor] < 0:
				memory[cursor] = 255
			elif memory[cursor] > 255:
				memory[cursor] = 0
			if timer < 0:
				return "".join(out)
			timer -= 1
			i += 1
		return "".join(out)

if __name__ == "__main__":
	code = ",.,.,."
	inp = "abc"
	bf=Brainfuck()
	print(bf.run(code, inp))
	input()