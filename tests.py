import unittest

import dynamic
from openapi import loaders, resolvers


class TestResolver(unittest.TestCase):

    def test_resolve(self):
        document = loaders.DocumentLoader.load('/home/kobayashi/Documents/repos/mockingpy/openapi.yaml')
        print(resolvers.result)


if __name__ == '__main__':
    unittest.main()
