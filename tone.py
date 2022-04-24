import random
from tone_calc import map_note_to_tone

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

   def shift_left(self, num):
      return Tone(self.tone - num)

   def shift_right(self, num):
      return Tone(self.tone + num)

   def as_str(self):
      return '{}{}'.format(self.note, modes[self.mode])
