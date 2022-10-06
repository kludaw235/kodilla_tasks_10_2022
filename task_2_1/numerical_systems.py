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

    def validate_rom(self, rom_list):
        if rom_list.count("D") > 1:
            raise ValueError()
        if rom_list.count("L") > 1:
            raise ValueError()
        if rom_list.count("V") > 1:
            raise ValueError()

    def rom_to_dec(self, number):
        rom_number_list = list(number)
        self.validate_rom(rom_number_list)
        temp_number = 0
        for r in reversed(rom_number_list):
            prev_temp_number = temp_number
            temp_number = rom_to_dec_dict[r]
            if temp_number >= prev_temp_number:
                self.target_number += temp_number
            else:
                self.target_number -= temp_number

if __name__ == '__main__':
    x = NumericalSystemsConverter('ROM', 'DEC', 'XXXVI').target_number
