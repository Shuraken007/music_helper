import sys

color_aliases = {
   "black": 0,
   "red": 1,
   "green": 22,
   "yellow": 3,
   "blue": 4,
   "magenta": 5,
   "cyan": 6,
   "white": 7,
   "brown": 94,
}

def get_open_code(alias, is_background):
   if not alias in color_aliases:
      raise NameError("unknown color alias {}".format(alias))
   color_num = color_aliases[alias]
   fill_type = 38
   if is_background:
      fill_type += 10
   color_num
   open_code = u"\u001b[{};5;{}m".format(str(fill_type), str(color_num))
   return open_code

def get_close_code():
   return u"\u001b[0m"

def print_color_table():
   for i in range(0, 16):
      for j in range(0, 16):
         code = str(i * 16 + j)
         sys.stdout.write(u"\u001b[48;5;" + code + "m " + code.ljust(4))
      print(u"\u001b[0m")

if __name__ == '__main__':
   print_color_table()
