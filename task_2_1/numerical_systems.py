class NumericalSystemsConverter:
    def __init__(self, source_system, target_system, number):
        self.target_number = None

        if source_system == "ROM" and target_system == "DEC":
            self.target_number = self.rom_to_dec(number)


    def rom_to_dec(self, number):
        return 1