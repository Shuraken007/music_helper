import random

from accord_builder import AccordBuilder, map_accord_type_to_shifts
from tone import Tone
from guitar_board import GuitarBoard
from piano_board import PianoBoard
import color_utils
import tone_calc

color_aliases_by_priority = ['red', 'blue', 'yellow', 'green', 'cyan', 'magenta']

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
   for i, accord_tone in enumerate(accord_tones):
      color_alias = color_aliases_by_priority[i]
      accord_chain += color_utils.get_open_code(color_alias, True)
      accord_chain += accord_tone.as_str()
      accord_chain += color_utils.get_close_code()

      shift = None
      if i < len(accord_tones) - 1:
         shift = map_accord_type_to_shifts[accord_type][i]
      else:
         shift = tone_calc.calc_delta(accord_tones[0].tone, accord_tone.tone)['up']
      accord_chain += " ──{}──> ".format(shift)

   color_alias = color_aliases_by_priority[0]
   accord_chain += color_utils.get_open_code(color_alias, True)
   accord_chain += accord_tones[0].as_str()
   accord_chain += color_utils.get_close_code()

   print(accord_chain + "\n")

   for board in img_boards:
      for i, tone in enumerate(accord_tones):
         board.highlight_tone(tone, color_aliases_by_priority[i])
      board.print()
      print('\n')

if __name__ == '__main__':
   piano_board = PianoBoard(Tone(3), 12, 12)
   guitar_board = GuitarBoard(Tone(7), [5, 5, 5, 4, 5], 19)
   img_boards = [
      # piano_board,
      guitar_board
   ]
   accord_builder = AccordBuilder()
   while(1):
      run_accord_game(img_boards, accord_builder)
      input()
      print('\n\n\n----------------')
      for board in img_boards:
         board.reset_highlight()
