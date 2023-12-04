#!/usr/bin/env python3
import random

from tone import Tone
from guitar_board import GuitarBoard

def generate_tone():
   num = random.randint(0, 11)
   return Tone(num)

def run_game_guitar_tone(board):
   tones = []
   msg = ''
   for i in range(0, 11):
      tone = Tone(i)
      board.highlight_tone(tone)
      msg = '{} {}'.format(msg, tone.as_colored_str())


   print(msg + "\n\n")

   board.print()

   print('\n')

if __name__ == '__main__':
   guitar_board = GuitarBoard(Tone(7), [5, 5, 5, 4, 5], 19)
   
   run_game_guitar_tone(guitar_board)