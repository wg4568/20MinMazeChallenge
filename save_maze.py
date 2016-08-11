from base64 import b64encode
import zlib

file_name = "test_maze.maze.raw"
file_save = "test_maze.maze"

file = open(file_name, "r").read()

data = b64encode(zlib.compress(file.replace("\n","").replace("\t","....")))

open(file_save, "w").write(data)