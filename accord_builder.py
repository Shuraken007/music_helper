map_accord_type_to_shifts = {
   "min": [3, 4],
   "maj": [4, 3],
}

class AccordBuilder():

   def build_tones(self, tone, accord_type):
      if accord_type not in map_accord_type_to_shifts:
         msg = "unknown accord type {}".format(accord_type)
         raise NameError(msg)

      res_tones = [tone]
      cur_tone = tone
      for shift in map_accord_type_to_shifts[accord_type]:
         cur_tone = cur_tone.shift_right(shift)
         res_tones.append(cur_tone)

      return res_tones
