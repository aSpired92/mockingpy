import unittest

from fastapi.openapi import models

from generator import dynamic

TEST_CASES = 10

class TestDataGeneration(unittest.TestCase):

    # FLOATS
    def test_float(self):
        for exclusive_minimum in [True, False]:
            for exclusive_maximum in [True, False]:
                for maximum in [-5, 0, 5, -2.31, 2.31]:
                    for minimum in [-5, 0, 5, -2.31, 2.31]:
                        for multiple_of in [5, 0.2]:
                            schema = models.Schema(**{
                              "type": "number",
                              "minimum": minimum,
                              "maximum": maximum,
                              "exclusiveMinimum": exclusive_minimum,
                              "exclusiveMaximum": exclusive_maximum,
                              "multipleOf": multiple_of,
                              "format": "float"
                            })

                            error_message = (
                                f'\n\n'
                                f'Minimum: {minimum}\n'
                                f'Maximum: {maximum}\n'
                                f'Excl. minimum: {exclusive_minimum}\n'
                                f'Excl. maximum: {exclusive_maximum}\n'
                                f'Multiple of: {multiple_of}\n'
                            )

                            for _ in range(TEST_CASES):
                                if (
                                        schema.minimum is not None and schema.maximum is not None and
                                        schema.minimum == schema.minimum and (
                                        schema.exclusiveMaximum or schema.exclusiveMinimum)
                                ):
                                    self.assertRaises(RuntimeError)
                                    continue

                                result = dynamic._generate_numeric(schema)

                                if exclusive_maximum:
                                    self.assertLess(result, maximum, error_message)
                                else:
                                    self.assertLessEqual(result, maximum, error_message)
                                if exclusive_minimum:
                                    self.assertGreater(result, minimum, error_message)
                                else:
                                    self.assertGreaterEqual(result, minimum, error_message)

if __name__ == '__main__':
    unittest.main()