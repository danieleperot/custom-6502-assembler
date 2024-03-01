class AddressResolver:
    _parameters: str
    _line_number: int
    _type: str
    _value: list[str | int]

    def __init__(self, parameters: str, line_number: int):
        self._parameters = parameters
        self._line_number = line_number

        self._value = []
        self._type = ''
        modes = [
            self._as_immediate,
            self._as_absolute,
            self._as_label,
        ]

        for mode in modes:
            resolved = mode()
            if (resolved):
                break

    def value(self) -> list:
        return self._value

    def is_absolute(self) -> bool:
        return self._type == 'absolute' and len(self._value) == 2

    def is_zero_page(self) -> bool:
        return self._type == 'absolute' and len(self._value) == 1

    def is_immediate(self) -> bool:
        return self._type == 'immediate'

    def is_label(self) -> bool:
        return self._type == 'label'

    def is_missing(self):
        return len(self._value) == 0 and len(self._type) == 0

    def relative_label(self) -> list[str | int]:
        if not self.is_label():
            return self.value()

        return ['REL|' + str(self._value[0])]

    def absolute_label(self) -> list[str | int | None]:
        if not self.is_label():
            return self.value()

        return ['ABS|' + str(self._value[0]), None]

    def _as_absolute(self):
        if len(self._parameters) == 0 or self._parameters[0] != "$":
            return False

        self._assert(len(self._parameters) <= 5, 'Bad parameter length')

        self._type = 'absolute'
        high_byte = self._parameters[1:3]

        if len(self._parameters) == 3:
            self._value = [int(high_byte, 16)]
            return True

        low_byte = self._parameters[3:]
        self._value = [int(low_byte, 16), int(high_byte, 16)]

        return True

    def _as_immediate(self):
        if len(self._parameters) == 0 or self._parameters[0] != "#":
            return False

        self._assert(len(self._parameters) <= 4, 'Bad parameter length')

        self._assert(self._parameters[1] == '$', 'Only hex values supported')

        self._type = 'immediate'
        self._value = [int(self._parameters[2:], 16)]

        return True

    def _as_label(self):
        if len(self._parameters) == 0:
            return False

        self._type = 'label'
        self._value = [self._parameters]

        return True

    def _assert(self, condition, error):
        assert condition, f'[ERROR] Line {self._line_number}: {error}'
