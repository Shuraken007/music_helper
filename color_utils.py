color_aliases = {
   "black": 30,
   "red": 31,
   "green": 32,
   "yellow": 33,
   "blue": 34,
   "magenta": 35,
   "cyan": 36,
   "white": 37,
}

def get_open_code(alias, is_background, is_bright):
   if not alias in color_aliases:
      raise NameError("unknown color alias {}".format(alias))
   color_num = color_aliases[alias]
   if is_background:
      color_num += 10
   color_as_str = str(color_num)
   if is_bright:
      color_as_str += ";1"
   return u"\u001b[" + color_as_str + "m"

def get_close_code():
   return u"\u001b[0m"
