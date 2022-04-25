import random

from accord_builder import AccordBuilder, map_accord_type_to_shifts
from tone import Tone
from guitar_board import GuitarBoard
from piano_board import PianoBoard

color_aliases_by_priority = ['red', 'yellow', 'cyan', 'green', 'magenta', 'blue']

def generate_tone():
   num = random.randint(0, 11)
   return Tone(num)

def run_accord_game(img_boards, accord_builder):
   tone = generate_tone()
   accord_type = random.choice(list(map_accord_type_to_shifts.keys()))

   msg = '{} {}'.format(tone.as_str(), accord_type)
   print(msg + "\n\n")

   accord_tones = accord_builder.build_tones(tone, accord_type)

   accord_chain = ""
   for accord_tone in accord_tones:
      accord_chain += accord_tone.as_str() + " -> "
   print(accord_chain + tone.as_str() + "\n")

   for board in img_boards:
      for i, tone in enumerate(accord_tones):
         board.highlight_tone(tone, color_aliases_by_priority[i])
      board.print()
      print('\n')

if __name__ == '__main__':
   piano_board = PianoBoard(Tone(3), 12, 12)
   guitar_board = GuitarBoard(Tone(7), [5, 5, 5, 4, 5], 19)
   img_boards = [piano_board, guitar_board]
   accord_builder = AccordBuilder()
   while(1):
      run_accord_game(img_boards, accord_builder)
      input()
      print('\n\n\n----------------')
      for board in img_boards:
         board.reset_highlight()
