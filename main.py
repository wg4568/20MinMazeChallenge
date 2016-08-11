from base64 import b64decode
import pygame, zlib

class player:
	x = 1
	y = 1
	movespeed = 1

def load_maze(file):
	lines = zlib.decompress(b64decode(open(file, "r").read())).split(",")
	maze = {}
	for line,y in zip(lines, xrange(len(lines))):
		for point,x in zip(list(line), xrange(len(line))):
			if point == "#":
				maze[x, y] = 1
			elif point == "$":
				maze[x, y] = 2
			else:
				maze[x, y] = 0
	for x in xrange(50):
		for y in xrange(50):
			try: maze[x, y]
			except KeyError: maze[x, y] = 0
	return maze

def gen_blank_maze(l, w):
	maze = {}
	for x in xrange(l):
		for y in xrange(w):
			maze[x, y] = 0
	return maze

class Game:
	def __init__(self, maze):
		pygame.init()

		self.title = "Maze Challenge"
		self.rate = 15
		self.size = [500, 500]
		self.background = (0, 0, 0)
		self.wall_color = (0, 0, 200)
		self.end_color = (255, 128, 0)
		self.player_color = (255, 0, 0)

		self.running = False
		self.has_won = False
		self.frame = 0
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode(self.size)
		self.font = pygame.font.Font('freesansbold.ttf', 100)

		self.maze = maze

		pygame.display.set_caption(self.title)

	def get_color(self, val):
		if val == 0:
			return self.background
		if val == 1:
			return self.wall_color
		if val == 2:
			return self.end_color

	def allow_up(self):
		try: return not self.maze[player.x, player.y-1] == 1
		except KeyError: return False
	def allow_down(self):
		try: return not self.maze[player.x, player.y+1] == 1
		except KeyError: return False
	def allow_left(self):
		try: return not self.maze[player.x-1, player.y] == 1
		except KeyError: return False
	def allow_right(self):
		try: return not self.maze[player.x+1, player.y] == 1
		except KeyError: return False

	def check_win(self):
		if self.has_won:
			return True
		else:
			self.has_won = self.maze[player.x, player.y] == 2
			return self.has_won

	def movement(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP] and self.allow_up():
			player.y -= player.movespeed
		if keys[pygame.K_DOWN] and self.allow_down():
			player.y += player.movespeed
		if keys[pygame.K_LEFT] and self.allow_left():
			player.x -= player.movespeed
		if keys[pygame.K_RIGHT] and self.allow_right():
			player.x += player.movespeed

	def draw(self):

		for x in xrange(self.size[0]/10):
			for y in xrange(self.size[1]/10):
				pygame.draw.rect(self.screen, self.get_color(self.maze[x, y]), [x*10, y*10, 10, 10])

		pygame.draw.rect(self.screen, self.player_color, [player.x*10, player.y*10, 10, 10])

		if self.check_win():
			self.screen.fill([255, 255, 255])
			text = self.font.render("You Win!", True, (0, 0, 0))
			self.screen.blit(text, [10, 10])

	def start(self):
		self.running = True
		while self.running:
			self.frame += 1
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			self.movement()
			self.draw()

			pygame.display.update()
			self.clock.tick(self.rate)

maze = load_maze("test_maze.maze")

game = Game(maze)
game.start()