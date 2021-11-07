import unittest
from ..utils import generate_address, signature_generator


class TestGenerateAddress(unittest.TestCase):

    def test_address_is_length_is_42(self):
        address = generate_address(1)
        self.assertEqual(len(address), 42)

    def test_address_type_is_string(self):
        address = generate_address(1)
        self.assertEqual(type(address), str)


class TestGenerateSignature(unittest.TestCase):

    def test_signature_generator_returns_string(self):
        signature = signature_generator("mosaic_dev", "tsvbdlsfshs", 45000)
        self.assertEqual(type(signature), str)