rom_to_dec_dict = \
    {'I': 1,
     'V': 5,
     'X': 10,
     'L': 50,
     'C': 100,
     'D': 500,
     'M': 1000,
     }


def get_key_by_value(wanted_value):
    return [key for key, value in rom_to_dec_dict.items() if value == wanted_value]


class NumericalSystemsConverter:
    def __init__(self, source_system='ROM', target_system='DEC'):
        self.source_system = source_system
        self.target_system = target_system

    def convert(self, number):
        if self.source_system == "ROM" and self.target_system == "DEC":
            return self.rom_to_dec(number)
        elif self.source_system == "DEC" and self.target_system == "ROM":
            return self.dec_to_rom(number)

    def validate_rom(self, number):
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

        number = number.upper()
        rom_list = list(number)
        for letter in ("D", "L", "V"):
            if rom_list.count(letter) > 1:
                raise ValueError()
        for letter in ("C", "X", "I"):
            if rom_list.count(letter) >= 10:
                raise ValueError()
        is_valid_substraction("I", ['M', 'D', 'C', 'L', 'X', 'V'])
        is_valid_substraction("X", ['M', 'D', 'C', 'L'])
        is_valid_substraction("C", ['M', 'D'])
        is_valid_substraction("V", ['M', 'D', 'C', 'L', 'X', None, None])
        is_valid_substraction("L", ['M', 'D', 'C', None, None])
        is_valid_substraction("D", ['M', None, None])
        return rom_list

    def rom_to_dec(self, number):
        rom_number_list = self.validate_rom(number)
        temp_number = 0
        target_number = 0
        for r in reversed(rom_number_list):
            prev_temp_number = temp_number
            temp_number = rom_to_dec_dict[r]
            if temp_number >= prev_temp_number:
                target_number += temp_number
            else:
                target_number -= temp_number
        return target_number

    def validate_dec(self, number):
        if number == 0:
            raise ValueError()
        return True

    def dec_to_rom(self, number):
        self.validate_dec(number)
        temp_list = []
        temp = list(str(number))
        for idx, i in enumerate(reversed(temp)):
            multiplier = 10 ** idx
            i = int(i)

            if i == 9:
                temp_list.insert(0, get_key_by_value(multiplier)[0])
                multiplier = 10 ** (idx + 1)
                temp_list.insert(1, get_key_by_value(multiplier)[0])
            elif i >= 5:
                temp_list.insert(0, get_key_by_value(multiplier * 5)[0])
                for x in range(i - 5):
                    temp_list.insert(1, get_key_by_value(multiplier)[0])
            elif i == 4 and multiplier != 1000:
                temp_list.insert(0, get_key_by_value(multiplier * 5)[0])
                temp_list.insert(0, get_key_by_value(multiplier)[0])
            else:
                for x in range(i):
                    temp_list.insert(0, get_key_by_value(multiplier)[0])

        return ''.join(temp_list)


if __name__ == '__main__':
    x = NumericalSystemsConverter('DEC', 'ROM').convert(59)
    print(x)
