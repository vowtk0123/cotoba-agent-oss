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
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.authorise import TemplateAuthoriseNode
from programy.config.brain.brain import BrainConfiguration

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphAuthoriseTests(TemplateGraphTestClient):

    def get_brain_config(self):
        return BrainConfiguration()

    def test_authorise_with_role_as_attrib(self):
        template = ET.fromstring("""
            <template>
                <authorise role="root">
                Hello
                </authorise>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        auth_node = ast.children[0]
        self.assertIsNotNone(auth_node)
        self.assertIsInstance(auth_node, TemplateAuthoriseNode)
        self.assertIsNotNone(auth_node.role)
        self.assertEqual("root", auth_node.role)

        result = auth_node.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)

    def test_authorise_with_role_as_attrib_and_optional_srai(self):
        template = ET.fromstring("""
            <template>
                <authorise role="root" denied_srai="ACCESS_DENIED">
                Hello
                </authorise>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        auth_node = ast.children[0]
        self.assertIsNotNone(auth_node)
        self.assertIsInstance(auth_node, TemplateAuthoriseNode)
        self.assertIsNotNone(auth_node.role)
        self.assertEqual("root", auth_node.role)

        result = auth_node.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("Hello", result)
