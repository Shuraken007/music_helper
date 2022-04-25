import random

from tone import Tone
from guitar_board import GuitarBoard

def generate_tone():
   num = random.randint(0, 11)
   return Tone(num)

def run_game_guitar_tone(img_boards):
   tone = generate_tone()

   msg = '{}'.format(tone.as_str())
   print(msg + "\n\n")

   for board in img_boards:
      board.highlight_tone(tone, 'cyan')
      board.print()

   print('\n')

if __name__ == '__main__':
   guitar_board = GuitarBoard(Tone(7), [5, 5, 5, 4, 5], 19)
   img_boards = [guitar_board]
   while(1):
      run_game_guitar_tone(img_boards)
      input()
      print('\n\n\n----------------')
      for board in img_boards:
         board.reset_highlight()
