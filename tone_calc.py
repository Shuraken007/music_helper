map_note_to_tone = {
   0: 'A',
   2: 'B',
   3: 'C',
   5: 'D',
   7: 'E',
   8: 'F',
   10: 'G',
}

def calc_delta(tone1_num, tone2_num):
   up_delta = tone1_num - tone2_num
   if up_delta < 0:
      up_delta = 12 - abs(up_delta)

   down_delta = 12 - up_delta

   return {'up': up_delta, 'down': down_delta}

def shift_left(tone_num, shift_num):
   return (tone_num - shift_num) % 12

def shift_right(tone_num, shift_num):
   return (tone_num + shift_num) % 12
