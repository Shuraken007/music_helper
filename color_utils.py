import sys

# https://www.w3schools.com/colors/colors_wheels.asp
# https://sashamaps.net/docs/resources/20-colors/
color_wheel_ryb = [
   [230, 25, 75], #Red
   [128, 0, 0], #Maroon
   # [170, 110, 40], #Brown
   [245, 130, 48], #Orange
   [255, 225, 25], #Yellow
   # [255, 250, 200], #Beige
   # [170, 255, 195], #Mint
   [210, 245, 60], #Mint
   [60, 180, 75], #Green
   [47,79,79], # darkslategray
   # [128, 128, 0], #Olive
   # [0, 128, 128], #Teal
   [0, 0, 128], #Navy
   # [0, 130, 200], #Blue
   [30,144,255], #DodgerBlue
   [145,93,241], #Cyan
   [240, 50, 230], #Purple
   [220, 190, 255], #Lavender
   # [240, 50, 230], #Purple
   # [250, 190, 212], #Pink
]

# wheel_start_pointer = 5 # (G = yellow)
# wheel_start_pointer = 0 # (A = red)
wheel_start_pointer = 0

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
