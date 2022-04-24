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

   def add_tone_to_highlight_map(self, string_num, lad_num, color_alias):
      if not string_num in self.highligt_map:
         self.highligt_map[string_num] = {}
      self.highligt_map[string_num][lad_num] = color_alias

   def highlight_tone(self, tone, color_alias):
      for string_num, open_lad in enumerate(self.open_lads):
         up_delta = tone_calc.calc_delta(tone.tone, open_lad.tone)['up']
         for j in range(0, self.height // 12 + 1):
            if up_delta <= self.height:
               self.add_tone_to_highlight_map(string_num, up_delta, color_alias)
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

   def is_tone_highlighted(self, string_num, lad_num):
      if not string_num in self.highligt_map:
         return
      if not lad_num in self.highligt_map[string_num]:
         return
      return self.highligt_map[string_num][lad_num]

   def add_inner(self, img, width, height):
      for i in range(1, height + 2):
         for string_num in range(0, width):
            color_alias = self.is_tone_highlighted(string_num, i-1)
            if color_alias:
               img[i] += color_utils.get_open_code(color_alias, False, False)
            img[i] += "▇"
            if color_alias:
               img[i] += color_utils.get_close_code()
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
