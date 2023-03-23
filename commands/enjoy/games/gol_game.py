import discord.ext.commands as commands

class GameOfLife:			
	class Field:
		def __init__(self, size=5, loop=False):
			self.size = size
			self.cells = [[] for _ in range(self.size)]
			self.cur_x = 0
			self.cur_y = 0
			for y in range(self.size):
				for x in range(self.size):
					self.cells[y].append(self.Cell(x, y))
			self.update_neighbors()
		
		class Cell:
			def __init__(self, x, y, status=0, next_status=False):
				self.x = x
				self.y = y
				self.status = status
				self.next_status = next_status
				self.neighbors = []
			
			def is_me(self, cell):
				if self.x == cell.x and self.y == cell.y:
					return True
				else: return False
			
			@property
			def name(self):
				return str(self.x)+str(self.y)
			
			def is_neighbor(self, cell):
				if cell.x in (self.x-1, self.x, self.x+1,) and cell.y in (self.y-1, self.y, self.y+1,) and not self.is_me(cell):
					return True
				else: return False
		
		def update_neighbors(self):
			for layer in self.cells:
				for cell in layer:
					neighbors = []
					for n_layer in self.cells:
						for neighbor in n_layer:
							if cell.is_neighbor(neighbor) and not cell.is_me(neighbor):
								neighbors.append(neighbor)
					cell.neighbors = neighbors

		def move_cursor(self, x=0, y=0):
			if self.cur_x + x in range(self.size) and self.cur_y + y in range(self.size):
				self.cur_x += x
				self.cur_y += y
			
		def update(self):
			for layer in self.cells:
				for cell in layer:
					online = 0
					for neighbor in cell.neighbors:
						if neighbor.status in (1, 3,):
							online += 1
						elif neighbor.status in (4,):
							online -= 8
						
					if cell.status == 1:
						if online in (2, 3,):
							cell.next_status = 1
						else:
							cell.next_status = 0
					elif cell.status == 2:
						if online < 0:
							cell.next_status = 0
						else:
							cell.next_status = cell.status
					elif cell.status == 3:
						if online > 5 or online < 0:
							cell.next_status = 4
						else:
							cell.next_status = cell.status
					elif cell.status == 4:
						cell.next_status = 0
					else:
						if online in (3,):
							cell.next_status = 1
						else:
							cell.next_status = 0
						
			for layer in self.cells:
				for cell in layer:
					cell.status = cell.next_status
		
		def flip_cell(self, type=1):
			cell = self.cells[self.cur_y][self.cur_x]
			cell.status = 0 if cell.status else type
		
		def print_field(self):
			field = [[] for _ in range(self.size)]
			for y, layer in enumerate(self.cells):
				for cell in layer:
					field[y].append(str(cell.status))
			
			control = [["@"]]
			for x in range(self.size):
				control[0].append("↓" if self.cur_x == x else "+")
			control[0] = "".join(control[0])
			
			for y in range(self.size):
				control.append([])
				control[y+1].append("→" if self.cur_y == y else "+")
				control[y+1].extend("".join(field[y]))
				control[y+1] = "".join(control[y+1])
			
			return "\n".join(control)

			"""
			Cell status:
			0 - empty cell
			1 - basic cell
			2 - wall cell
			3 - explosive cell
			4 - explosion
			"""
			
if __name__ == "__main__":
	gol = GameOfLife.Field(5)
	print(gol.print_field())
	i = ""
	while i != "q":
		i = input(">>> ")
		if "w" in i:
			gol.move_cursor(0, -i.count("w"))
		if "a" in i:
			gol.move_cursor(-i.count("a"), 0)
		if "s" in i:
			gol.move_cursor(0, i.count("s"))
		if "d" in i:
			gol.move_cursor(i.count("d"), 0)
		if "f" in i:
			gol.flip_cell()
		if "r" in i:
			gol.flip_cell(2)
		if "x" in i:
			gol.flip_cell(3)
		if "c" in i:
			cell = gol.cells[gol.cur_y][gol.cur_x]
			online = 0
			for neighbor in cell.neighbors:
				online += neighbor.status
			print(f"""Cell: {cell.name} have {len(cell.neighbors)} neighbors
Neighbors: {[n.name for n in cell.neighbors]}
Online status = {online}""")
		if i == "":
			gol.update()
		print(gol.print_field())
