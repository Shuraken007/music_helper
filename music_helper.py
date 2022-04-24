import random
import time

map_note_to_tone = {
   0: 'A',
   2: 'B',
   3: 'C',
   5: 'D',
   7: 'E',
   8: 'F',
   10: 'G',
}

modes = {
   -1: '#',
   0: '',
   1: '♭',
}

class Tone:
   def __init__(self, num):
      self.tone = num % 12

      if self.tone in map_note_to_tone:
         self.mode = 0
      else:
         self.mode = random.choice([-1, 1])

      self.note = map_note_to_tone[(self.tone + self.mode) % 12]

   def __eq__(self, o):
      return self.tone==o.tone

   def __add__(self, o):
      new_tone = None
      if isinstance(o, int):
         new_tone = Tone(self.tone + o)
      elif isinstance(o, Tone):
         new_tone = Tone(self.tone + o.tone)
      else:
         raise NameError('unknown type "{}" on "+" operation with Tone'.format(type(o)))

      return new_tone

   def calc_upwards_delta(self, o):
      substracting_tone = None
      if isinstance(o, int):
         substracting_tone = o
      elif isinstance(o, Tone):
         substracting_tone = o.tone
      else:
         raise NameError('unknown type "{}" on "-" operation with Tone'.format(type(o)))

      delta = self.tone - substracting_tone
      if delta < 0:
         delta = 12 - abs(delta)
      return delta

   def as_str(self):
      return '{}{}'.format(self.note, modes[self.mode])

class PianoBoardAscii:
   color_alias = {
      'black': 0,
      'white': 47,
      'first': 43,
      'second': 46,
   }

   def __init__(self, central_tone, sh_left, sh_right):
      self.length = sh_left + sh_right + 1
      self.start_tone_num = (central_tone.tone - sh_left) % 12
      self.colored_tones = {}

      self.black_height = 4
      self.black_width = 1
      self.white_height = 7
      self.white_width = 3

   def highlight_tone(self, tone, color):
      self.colored_tones[tone.tone] = color

   def print(self):
      img = []
      for i in range(0, self.white_height + 2):
         img.append("")

      current_tone = self.start_tone_num
      self.add_left_board(img, current_tone)

      for i in range(0, self.length):
         self.add_inner(img, current_tone)
         self.add_right_board(img, current_tone)
         current_tone = (current_tone + 1) % 12

      for i in range(0, self.white_height + 2):
         print(img[i])

   def add_left_board(self, img, tone):
      if self.is_white(tone):
         self.add_white_left_board(img, tone)
      else:
         self.add_black_left_board(img, tone)

   def is_white(self, tone):
      tone = tone % 12
      return True if tone in map_note_to_tone else False

   def is_black(self, tone):
      tone = tone % 12
      return True if not tone in map_note_to_tone else False

   def add_black_left_board(self, img, tone):
      for i in range(1, self.black_height+1):
         img[i] += "|"
      for i in range(self.black_height+1, self.white_height+1):
         img[i] += " |"

      img[self.white_height+1] += " " * (1 + self.black_width)
      img[0] += " " * (1 + self.black_width)

   def add_white_left_board(self, img, tone):
      for i in range(1, self.black_height+1):
         if self.is_white(tone - 1):
            img[i] += "|"
         else:
            if i == self.black_height:
               img[i] += "_|" * self.black_width
            else:
               img[i] += " |"

      for i in range(self.black_height+1, self.white_height+1):
         img[i] += "|"

      img[self.white_height+1] += " "
      img[0] += " "

   def get_color(self, alias):
      return self.color_alias[alias]

   def open_color(self, img, tone):
      color_num = None
      if tone in self.colored_tones:
         color_num = self.get_color(self.colored_tones[tone])
      elif self.is_white(tone):
         color_num = self.get_color('white')
      else:
         color_num = self.get_color('black')

      for i in range(1, self.white_height+1):
         img[i] += u"\u001b[" + str(color_num) + "m"


   def close_color(self, img, tone):
      for i in range(1, self.white_height+1):
         img[i] += u"\u001b[0m"

   def add_inner(self, img, tone):
      self.open_color(img, tone)
      if self.is_white(tone):
         self.add_white_inner(img, tone)
      else:
         self.add_black_inner(img, tone)
      self.close_color(img, tone)

   def add_black_inner(self, img, tone):
      for i in range(1, self.black_height):
         img[i] += " " * self.black_width
      img[self.black_height] += "_"

   def add_white_inner(self, img, tone):
      width_during_black = self.white_width
      if self.is_black(tone - 1):
         width_during_black -= 1
      if self.is_black(tone + 1):
         width_during_black -= 1

      for i in range(1, self.black_height+1):
         img[i] += " " * width_during_black
      for i in range(self.black_height+1, self.white_height):
         img[i] += " " * self.white_width

      img[self.white_height] += "_" * self.white_width

   def add_right_board(self, img, tone):
      if self.is_white(tone):
         self.add_white_right_board(img, tone)
      else:
         self.add_black_right_board(img, tone)

   def add_black_right_board(self, img, tone):
      for i in range(1, self.black_height+1):
         img[i] += "|"

   def add_white_right_board(self, img, tone):

      for i in range(1, self.white_height+1):
         img[i] += "|"

      note_str = " " * (self.white_width // 2) + map_note_to_tone[tone] + " " * (self.white_width - self.white_width // 2)
      img[self.white_height+1] += note_str

      note_num = "{:^3} ".format(tone)
      img[0] += note_num

class GuitarBoard():
   def __init__(self, start_tone, shift_arr, lads_display_num):
      self.open_lads = self.build_open_lads(start_tone, shift_arr)
      self.height = lads_display_num
      self.colored_tones = {}

   def build_open_lads(self, start_tone, shift_arr):
      open_lads = [start_tone]
      last_tone = start_tone
      for shift in shift_arr:
         new_tone = last_tone + shift
         open_lads.append(new_tone)
         last_tone = new_tone
      return open_lads

   color_alias = {
      'first': 33,
      'second': 36,
   }

   def get_color(self, alias):
      return self.color_alias[alias]

   def color_tone(self, x, y, color):
      if not x in self.colored_tones:
         self.colored_tones[x] = {}
      self.colored_tones[x][y] = color

   def highlight_tone(self, tone, color):
      for i, open_lad in enumerate(self.open_lads):
         upward_delta = tone.calc_upwards_delta(open_lad)
         for j in range(0, self.height // 12 + 1):
            if upward_delta <= self.height:
               self.color_tone(i, upward_delta, color)
               upward_delta += 12

   def build_grief_img(self, lads_display_num):
      img = []
      for i in range(0, lads_display_num + 2):
         img.append("")
      self.add_left_board(img, lads_display_num)
      self.add_inner(img, len(self.open_lads), lads_display_num)
      self.add_right_board(img, lads_display_num)
      return img

   def add_left_board(self, img, height):
      for i in range(2, height + 2):
         img[i] += " _"
      img[1] += "░░"
      img[0] += "  "

   def check_color(self, x, y):
      if not x in self.colored_tones:
         return
      if not y in self.colored_tones[x]:
         return
      return self.colored_tones[x][y]

   def open_color(self, img, x, color_alias):
      color_num = self.get_color(color_alias)
      img[x] += u"\u001b[" + str(color_num) + "m"

   def close_color(self, img, x):
      img[x] += u"\u001b[0m"

   def add_inner(self, img, width, height):
      for i in range(1, height + 2):
         for j in range(0, width):
            color_alias = self.check_color(j, i-1)
            if color_alias:
               self.open_color(img, i, color_alias)
            img[i] += "▇"
            if color_alias:
               self.close_color(img, i)
            img[i] += "░"
      for tone in self.open_lads:
         img[0] += "{:<2}".format(tone.as_str())

   def add_right_board(self, img, height):
      for i in range(2, height + 2):
         img[i] += "_ "
      img[1] += "░░ "
      img[0] += "   "
      for i in range(1, height + 2):
         img[i] += str(i-1)

   def print(self):
      img = self.build_grief_img(self.height)
      for row in img:
         print(row)

def generate_tone():
   num = random.randint(0, 11)
   return Tone(num)

def run_test():
   first_tone = generate_tone()
   second_tone = generate_tone()

   while first_tone == second_tone:
      second_tone = generate_tone()

   msg = '{}  ->  {}'.format(first_tone.as_str(), second_tone.as_str())
   print(msg + "\n\n")

   delta = second_tone.calc_upwards_delta(first_tone)
   inversed_delta = delta - 12

   time.sleep(1)
   board = PianoBoardAscii(first_tone, 11, 11)
   board.highlight_tone(first_tone, 'first')
   board.highlight_tone(second_tone, 'second')
   board.print()
   grief = GuitarBoard(Tone(7), [5, 5, 5, 4, 5], 19)
   grief.highlight_tone(first_tone, 'first')
   grief.highlight_tone(second_tone, 'second')
   grief.print()

   input()
   result_msg = '↑: {}\n↓: {}'.format(delta, inversed_delta)
   print(result_msg)

if __name__ == '__main__':
   while(1):
      run_test()
      input()
      print('\n\n\n----------------')
