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
        self.target_number = 0

        if source_system == "ROM" and target_system == "DEC":
            self.rom_to_dec(number)


    def rom_to_dec(self, number):
        rom_number_list = list(number)
        temp_number = 0
        for r in reversed(rom_number_list):
            prev_temp_number = temp_number
            temp_number = rom_to_dec_dict[r]
            print("P ", prev_temp_number)
            print("T ", temp_number)
            if temp_number >= prev_temp_number:
                self.target_number += temp_number
            else:
                self.target_number -= temp_number
            print(self.target_number)


if __name__ == '__main__':
    x = NumericalSystemsConverter('ROM', 'DEC', 'XXXVI').target_number
