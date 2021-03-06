"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import unittest

from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration


class RedisStorageConfigurationTests(unittest.TestCase):

    def test_initial_creation(self):
        config = RedisStorageConfiguration()
        self.assertIsNotNone(config)
        self.assertEqual(config.host, "localhost")
        self.assertEqual(config.port, 6379)
        self.assertEqual(config.password, None)
        self.assertEqual(config.db, 0)
        self.assertEqual(config.prefix, "programy")
        self.assertEqual(config.drop_all_first, True)

    def test_initialise_with_config(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
            redis:
                type:   redis
                config:
                    host: localhost
                    port: 6379
                    password: passwordX
                    db: 0
                    prefix: programy
                    drop_all_first: True
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("redis")

        config = RedisStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        self.assertEqual(config.host, "localhost")
        self.assertEqual(config.port, 6379)
        self.assertEqual(config.password, "passwordX")
        self.assertEqual(config.db, 0)
        self.assertEqual(config.prefix, "programy")
        self.assertEqual(config.drop_all_first, True)
