import sys

# https://www.w3schools.com/colors/colors_wheels.asp
color_wheel_ryb = [
   [254, 39, 18 ], #"red"
   [252, 96, 10 ], #"red_orange"
   [251, 153, 2 ], #"orange"
   [252, 204, 26], #"yellow_orange"
   [254, 254, 51], #"yellow"
   [154, 205, 50], #"yellow_green"
   [102, 176, 50], #"green"
   [52, 124, 152], #"blue_green"
   [2, 71, 254  ], #"blue"
   [68, 36, 214 ], #"blue_purple"
   [134, 1, 175 ], #"purple"
   [194, 20, 96 ], #"red_purple"
]

wheel_start_pointer = 5 # (G = yellow)

color_aliases = {
   "black": 0,
   "white": 7,
}

def get_open_code_by_tone(tone_num, is_background):
   wheel_index = (tone_num + wheel_start_pointer) % 12
   rgb = color_wheel_ryb[wheel_index]
   fill_type = 38
   if is_background:
      fill_type += 10
   open_code = u"\u001b[{};2;{};{};{}m".format(str(fill_type), str(rgb[0]), str(rgb[1]), str(rgb[2]))
   return open_code


def get_open_code(alias, is_background):
   if not alias in color_aliases:
      raise NameError("unknown color alias {}".format(alias))
   color_num = color_aliases[alias]
   fill_type = 38
   if is_background:
      fill_type += 10
   open_code = u"\u001b[{};5;{}m".format(str(fill_type), str(color_num))
   return open_code

def get_close_code():
   return u"\u001b[0m"

def print_color_table():
   for i in range(0, 16):
      for j in range(0, 16):
         num = i * 16 + j
         code = str(num)
         sys.stdout.write(u"\u001b[48;5;" + code + "m " + code.ljust(4))
         if ( ((num + 1) % 8 == 0 and num < 16 and num > 0) or
            ((num - 15) % 6 == 0 and num > 15)
         ):
            print(u"\u001b[0m")

if __name__ == '__main__':
   print_color_table()
