import color_utils
import tone_calc

class GuitarBoard():
   def __init__(self, start_tone, shift_arr, lads_display_num):
      self.open_lads = self.build_open_lads(start_tone, shift_arr)
      self.height = lads_display_num
      self.highligt_map = {}

   def build_open_lads(self, start_tone, shift_arr):
      open_lads = [start_tone]
      cur_tone = start_tone
      for shift in shift_arr:
         cur_tone = cur_tone.shift_right(shift)
         open_lads.append(cur_tone)
      return open_lads

   def add_tone_to_highlight_map(self, string_num, lad_num, tone):
      if not string_num in self.highligt_map:
         self.highligt_map[string_num] = {}
      self.highligt_map[string_num][lad_num] = tone.tone

   def is_tone_highlighted(self, string_num, lad_num):
      if not string_num in self.highligt_map:
         return
      if not lad_num in self.highligt_map[string_num]:
         return
      return self.highligt_map[string_num][lad_num]

   def highlight_tone(self, tone):
      for string_num, open_lad in enumerate(self.open_lads):
         up_delta = tone_calc.calc_delta(tone.tone, open_lad.tone)['up']
         for j in range(0, self.height // 12 + 1):
            if up_delta <= self.height:
               self.add_tone_to_highlight_map(string_num, up_delta, tone)
               up_delta += 12

   def remove_highlight(self, tone):
      for string_num, open_lad in enumerate(self.open_lads):
         up_delta = tone.calc_delta(open_lad)['up']
         for j in range(0, self.height // 12 + 1):
            if up_delta <= self.height:
               if not string_num in self.highligt_map:
                  continue
               if not up_delta in self.highligt_map[string_num]:
                  continue
               del self.highligt_map[string_num][up_delta]

               up_delta += 12

   def reset_highlight(self):
      self.highligt_map.clear()

   def build_open_lads_img(self):
      img = []
      for i in range(0, 3):
         img.append('')
      self.add_open_lads_left_board(img)
      self.add_open_lads_inner(img, len(self.open_lads))
      self.add_open_lads_right_board(img)
      return img

   def build_grief_img(self, height):
      img = []
      for i in range(0, height):
         img.append("")
      self.add_grief_left_board(img, height)
      self.add_grief_inner(img, len(self.open_lads), height)
      self.add_grief_right_board(img, height)
      return img

   def add_open_lads_left_board(self, img):
      img[0] += "  "
      img[1] += "░░"
      img[2] += "══"

   def build_lad(self, img, string_num, lad_num):
      tone_num = self.is_tone_highlighted(string_num, lad_num)
      lad = ""
      if tone_num is not None:
         lad += color_utils.get_open_code_by_tone(tone_num, False)
      lad += "▇"
      if tone_num is not None:
         lad += color_utils.get_close_code()
      return lad

   def build_string_space(self, lad_num):
      space = ""
      is_underline = lad_num % 5 == 0
      if is_underline:
         space += color_utils.get_open_code('black', False)
      space += "░"
      if is_underline:
         space += color_utils.get_close_code()
      return space

   def add_open_lads_inner(self, img, width):
      for string_num in range(0, width):
         img[1] += self.build_lad(img, string_num, 0)
         if string_num != width - 1:
            img[1] += "░"
      for tone in self.open_lads:
         img[0] += "{:<2}".format(tone.as_str())
      img[2] += "══" * width

   def add_open_lads_right_board(self, img):
      img[0] += "  "
      img[1] += "░░ 0"
      img[2] += "══"

   def add_grief_left_board(self, img, height):
      for i in range(0, height):
         img[i] += " _"

   def add_grief_inner(self, img, width, height):
      for i in range(0, height):
         for string_num in range(0, width):
            img[i] += self.build_lad(img, string_num, i+1)
            if string_num < width - 1:
               img[i] += self.build_string_space(i+1)

   def add_grief_right_board(self, img, height):
      for i in range(0, height):
         img[i] += "_  "
      for i in range(0, height):
         img[i] += str(i+1)

   def print(self):
      open_lads_img = self.build_open_lads_img()
      grief_img = self.build_grief_img(self.height)
      for row in open_lads_img:
         print(row)
      for row in grief_img:
         print(row)
