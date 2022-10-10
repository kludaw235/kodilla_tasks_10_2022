rom_to_dec_dict = \
    {'I': 1,
     'V': 5,
     'X': 10,
     'L': 50,
     'C': 100,
     'D': 500,
     'M': 1000,
     }


class NumericalSystemsConverter:
    def __init__(self, source_system, target_system, number):
        self.number = number
        self.target_number = 0

        if source_system == "ROM" and target_system == "DEC":
            self.rom_to_dec()

    def validate_rom(self):

        def is_appearing_once(num):
            if rom_list.count(num) > 1:
                raise ValueError()

        def is_valid_denomination(num):
            if rom_list.count(num) >= 10:
                raise ValueError()

        rom_list = list(self.number)
        for i in ("D", "L", "V"):
            is_appearing_once(i)

        for i in ("C", "X", "I"):
            is_valid_denomination(i)

        for idx, value in enumerate(rom_list[:-1]):
            if value == "I":
                if rom_list[idx + 1] in ['M', 'D', 'C', 'L']:
                    raise ValueError()
                elif rom_list[idx + 1] == 'I':
                    try:
                        if rom_list[idx + 2] in ['M', 'D', 'C', 'L', 'X', 'V']:
                            raise ValueError()
                    except IndexError:
                        pass
            elif value == "X":
                if rom_list[idx + 1] in ['M', 'D']:
                    raise ValueError()
                elif rom_list[idx + 1] == 'X':
                    try:
                        if rom_list[idx + 2] in ['M', 'D', 'C', 'L']:
                            raise ValueError()
                    except IndexError:
                        pass
            elif value == "C":
                if rom_list[idx + 1] == 'C':
                    try:
                        if rom_list[idx + 2] in ['M', 'D']:
                            raise ValueError()
                    except IndexError:
                        pass







    def rom_to_dec(self):
        rom_number_list = list(self.number)
        self.validate_rom()
        temp_number = 0
        for r in reversed(rom_number_list):
            prev_temp_number = temp_number
            temp_number = rom_to_dec_dict[r]
            if temp_number >= prev_temp_number:
                self.target_number += temp_number
            else:
                self.target_number -= temp_number

if __name__ == '__main__':
    x = NumericalSystemsConverter('ROM', 'DEC', 'IIV').target_number
    print(x)
