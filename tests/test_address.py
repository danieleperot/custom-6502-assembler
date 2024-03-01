import unittest

from src.address import AddressResolver


class TestAddressResolver(unittest.TestCase):
    def test_resolves_hex_absolute_address(self):
        address = AddressResolver('$AB41', 1)

        # Resolve as little endian
        self.assertEqual([0x41, 0xAB], address.value())

        self.assertEqual(True, address.is_absolute())
        self.assertEqual(False, address.is_immediate())
        self.assertEqual(False, address.is_zero_page())
        self.assertEqual(False, address.is_label())

    # TODO: fix this bug
    def BUG_test_resolves_hex_absolute_address_with_partial_value(self):
        address = AddressResolver('$140', 1)

        # Resolve as little endian
        self.assertEqual([0x40, 0x01], address.value())

        self.assertEqual(True, address.is_absolute())
        self.assertEqual(False, address.is_immediate())
        self.assertEqual(False, address.is_zero_page())
        self.assertEqual(False, address.is_label())

    def test_resolves_hex_immediate_address(self):
        address = AddressResolver('#$B4', 1)

        self.assertEqual([0xB4], address.value())

        self.assertEqual(False, address.is_absolute())
        self.assertEqual(True, address.is_immediate())
        self.assertEqual(False, address.is_zero_page())
        self.assertEqual(False, address.is_label())

    def test_resolves_hex_immediate_address_with_partial_value(self):
        address = AddressResolver('#$4', 1)

        self.assertEqual([0x04], address.value())

        self.assertEqual(False, address.is_absolute())
        self.assertEqual(True, address.is_immediate())
        self.assertEqual(False, address.is_zero_page())
        self.assertEqual(False, address.is_label())

    def test_resolves_hex_zero_page_address(self):
        address = AddressResolver('$AB', 1)

        self.assertEqual([0xAB], address.value())
        self.assertEqual(False, address.is_absolute())
        self.assertEqual(False, address.is_immediate())
        self.assertEqual(True, address.is_zero_page())
        self.assertEqual(False, address.is_label())

    # TODO: fix this bug
    def BUG_test_resolves_hex_zero_page_address_with_partial_value(self):
        address = AddressResolver('$8', 1)

        self.assertEqual([0x08], address.value())
        self.assertEqual(False, address.is_absolute())
        self.assertEqual(False, address.is_immediate())
        self.assertEqual(True, address.is_zero_page())
        self.assertEqual(False, address.is_label())

    def test_cannot_display_relative_label_for_non_label(self):
        address = AddressResolver('#$01', 1)

        self.assertEqual(False, address.is_label())
        self.assertEqual([0x01], address.relative_label())

    def test_displays_label_as_relative(self):
        address = AddressResolver('THIS_IS_A_LABEL', 1)

        self.assertEqual(True, address.is_label())
        self.assertEqual(['REL|THIS_IS_A_LABEL'], address.relative_label())

    def test_cannot_display_absolute_label_for_non_label(self):
        address = AddressResolver('#$01', 1)

        self.assertEqual(False, address.is_label())
        self.assertEqual([0x01], address.absolute_label())

    def test_displays_label_as_absolute(self):
        address = AddressResolver('THIS_IS_A_LABEL', 1)

        self.assertEqual(True, address.is_label())
        self.assertEqual([
            'ABS|THIS_IS_A_LABEL',
            None
        ], address.absolute_label())
