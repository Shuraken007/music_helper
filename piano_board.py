from tone_calc import map_note_to_tone
import color_utils
import tone_calc

class PianoBoard:

   def __init__(self, central_tone, sh_left, sh_right):
      self.length = sh_left + sh_right + 1
      self.start_tone = central_tone.shift_left(sh_left)
      self.highlight_map = {}

      self.black_height = 4
      self.black_width = 1
      self.white_height = 7
      self.white_width = 3

   def highlight_tone(self, tone, color_alias):
      self.highlight_map[tone.tone] = color_alias

   def remove_highlight(self, tone):
      del self.highlight_map[tone.tone]

   def reset_highlight(self):
      self.highlight_map.clear()

   def print(self):
      img = []
      for i in range(0, self.white_height + 2):
         img.append("")

      current_tone = self.start_tone.tone
      self.add_left_board(img, current_tone)

      for i in range(0, self.length):
         self.add_inner(img, current_tone)
         self.add_right_board(img, current_tone)
         current_tone = tone_calc.shift_right(current_tone, 1)

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

   def open_color(self, img, tone):
      color_alias = None
      if tone in self.highlight_map:
         color_alias = self.highlight_map[tone]
      elif self.is_white(tone):
         color_alias = 'white'
      else:
         color_alias = 'black'

      for i in range(1, self.white_height+1):
         img[i] += color_utils.get_open_code(color_alias, True, False)

   def close_color(self, img):
      for i in range(1, self.white_height+1):
         img[i] += color_utils.get_close_code()

   def add_inner(self, img, tone):
      self.open_color(img, tone)
      if self.is_white(tone):
         self.add_white_inner(img, tone)
      else:
         self.add_black_inner(img, tone)
      self.close_color(img)

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
