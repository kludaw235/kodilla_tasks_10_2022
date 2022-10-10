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
        def validate_small_letters():
            self.number = self.number.upper()

        def is_appearing_once(num):
            if rom_list.count(num) > 1:
                raise ValueError()

        def is_valid_denomination(num):
            if rom_list.count(num) >= 10:
                raise ValueError()

        def is_valid_substraction(value_checked, forbidden_pre_values):
            counter = 0
            for idx, val in enumerate(rom_list[:-1]):
                if val == value_checked:
                    counter += 1
                    if (rom_list[idx + 1] in forbidden_pre_values[:-2]) or \
                            (counter > 1 and rom_list[idx + 1] in forbidden_pre_values):
                        raise ValueError()
                else:
                    counter = 0

        validate_small_letters()
        rom_list = list(self.number)

        for i in ("D", "L", "V"):
            is_appearing_once(i)

        for i in ("C", "X", "I"):
            is_valid_denomination(i)

        is_valid_substraction("I", ['M', 'D', 'C', 'L', 'X', 'V'])
        is_valid_substraction("X", ['M', 'D', 'C', 'L'])
        is_valid_substraction("C", ['M', 'D'])
        is_valid_substraction("V", ['M', 'D', 'C', 'L', 'X', None, None])
        is_valid_substraction("L", ['M', 'D', 'C', None, None])
        is_valid_substraction("D", ['M', None, None])

    def rom_to_dec(self):
        self.validate_rom()
        rom_number_list = list(self.number)
        temp_number = 0
        for r in reversed(rom_number_list):
            prev_temp_number = temp_number
            temp_number = rom_to_dec_dict[r]
            if temp_number >= prev_temp_number:
                self.target_number += temp_number
            else:
                self.target_number -= temp_number

if __name__ == '__main__':
    x = NumericalSystemsConverter('ROM', 'DEC', 'mdclxvi').target_number
    print(x)
