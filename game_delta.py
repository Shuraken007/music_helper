import random

import tone_calc
from tone import Tone
from guitar_board import GuitarBoard
from piano_board import PianoBoard

def generate_tone():
   num = random.randint(0, 11)
   return Tone(num)

def run_test(img_boards):
   first_tone = generate_tone()
   second_tone = generate_tone()

   while first_tone == second_tone:
      second_tone = generate_tone()

   msg = '{}  ->  {}'.format(first_tone.as_str(), second_tone.as_str())
   print(msg + "\n\n")

   for board in img_boards:
      board.reset_highlight()
      board.highlight_tone(first_tone, 'yellow')
      board.highlight_tone(second_tone, 'cyan')
      board.print()
      print('\n')

   input()
   delta = tone_calc.calc_delta(first_tone.tone, second_tone.tone)
   print('{} <--- {} ---> {}'.format(second_tone.as_str(), first_tone.as_str(), second_tone.as_str()))
   print('    {}     {}'.format(delta['down'], delta['up']))

if __name__ == '__main__':
   piano_board = PianoBoard(Tone(3), 12, 12)
   guitar_board = GuitarBoard(Tone(7), [5, 5, 5, 4, 5], 19)
   img_boards = [piano_board, guitar_board]
   while(1):
      run_test(img_boards)
      input()
      print('\n\n\n----------------')
      for board in img_boards:
         board.reset_highlight()
