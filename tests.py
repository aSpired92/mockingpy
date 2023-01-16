import unittest
import connexion

import dynamic
from openapi import loaders, resolvers


class TestResolver(unittest.TestCase):

    def test_resolve(self):
        app = connexion.FlaskApp(__name__, specification_dir='openapi/')
        app.add_api('my_api.yaml')
        app.run(port=8080)


if __name__ == '__main__':
    unittest.main()
