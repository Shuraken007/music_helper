import random
import sys

from tone import Tone
from guitar_board import GuitarBoard
from piano_board import PianoBoard

def generate_tone():
   num = random.randint(0, 11)
   return Tone(num)

def run_game_full_color(img_boards):
   for i in range(0, 12):
      tone = Tone(i)
      msg = '{}'.format(tone.as_colored_str())
      sys.stdout.write(tone.as_colored_str() + " ")
      for board in img_boards:
         board.highlight_tone(tone)

   print()
   for board in img_boards:
      board.highlight_tone(tone)
      board.print()

if __name__ == '__main__':
   piano_board = PianoBoard(Tone(3), 12, 12)
   guitar_board = GuitarBoard(Tone(7), [5, 5, 5, 4, 5], 19)
   img_boards = [piano_board, guitar_board]
   run_game_full_color(img_boards)
