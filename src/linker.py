class Linker:
    _labels: dict[str, int]
    _start_pos: int

    def __init__(self, start_pos):
        self._labels = {}
        self._start_pos = start_pos

    def parse(self, labels, bytecode):
        self._labels = labels

        program_counter = 0
        new_bytecode = []

        for (bytes_list, instruction) in bytecode:
            new_bytes = []

            for byte in bytes_list:
                if not str(byte).isnumeric():
                    parsed = self._parse_label(
                        byte, program_counter, instruction)
                    new_bytes.extend(parsed)
                else:
                    new_bytes.append(byte)
                program_counter += 1

            new_bytecode.append((new_bytes, instruction))

        return new_bytecode

    def _parse_label(self, byte, program_counter, instruction) -> list[int]:
        reference = byte[:3]
        label = byte[4:]
        label_pos = self._labels.get(label)

        has_label = label_pos is not None
        assert has_label, f'[ERROR] Unknown label {label} in "{instruction}".'

        if reference == 'REL':
            # TODO: Assert range -128, +127
            if program_counter >= label_pos:
                return [255 - (program_counter - label_pos)]
            else:
                return [label_pos - program_counter]

        if reference == 'ABS':
            address = self._start_pos + label_pos

            in_range = address >= self._start_pos
            assert in_range, f'Address out of range: {address}'

            return [address & 0xFF, (address >> 8) & 0xFF]

        assert False, f'[ERROR] Reference mode "{reference}" unsupported.'
