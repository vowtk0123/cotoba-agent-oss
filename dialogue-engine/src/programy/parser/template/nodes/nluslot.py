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
"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.utils.logging.ylogger import YLogger

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils
import json


class TemplateNluSlotNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._slotName = None
        self._itemName = None
        self._index = None

    def resolve_children(self, client_context):
        if self._children:
            return self.resolve_children_to_string(client_context)
        return ""

    def resolve_to_string(self, client_context):
        resolved = ""
        conversation = client_context.bot.get_conversation(client_context)
        slotName = self._slotName.resolve(client_context)
        itemName = self._itemName.resolve(client_context)
        try:
            slotIndex = int(self._index.resolve(client_context))
        except Exception:
            slotIndex = 0

        slots = None
        try:
            value = conversation.current_question().property("__SYSTEM_NLUDATA__")
            json_dict = json.loads(value)
            slots = json_dict["slots"]
        except Exception:
            YLogger.error(self, "TemplateNluSlotNode failed to load __SYSTEM_NLUDATA__")
            return resolved

        slotsKeyName = "slot"

        slotKeys = [slot.get(slotsKeyName) for slot in slots]
        if itemName == "count":
            if slotName == "*":
                resolved = str(len(slotKeys))
            else:
                resolved = str(slotKeys.count(slotName))

            YLogger.debug(client_context, "nluslot [%s] resolved to [%s]", itemName, resolved)
            return resolved

        index = None
        try:
            if slotName == "*":
                index = 0
                if slotIndex != 0:
                    index = slotIndex
            else:
                if slotIndex != 0:
                    slotCounter = 0
                    targetCounter = 0
                    for name in slotKeys:
                        if name == slotName:
                            if targetCounter == slotIndex:
                                index = slotCounter
                                break
                            targetCounter += 1
                        slotCounter += 1
                else:
                    index = slotKeys.index(slotName)
        except Exception:
            YLogger.debug(client_context, "nluslot non search keys:%s", slotName)

        if index is not None:
            YLogger.debug(client_context, "nluintent index[%s]", index)
            try:
                if itemName in slots[index]:
                    resolved = str(slots[index].get(itemName))
            except Exception:
                YLogger.debug(client_context, "nluslot non search item:%s", itemName)

        if resolved == '':
            YLogger.debug(client_context, "nluslot failed slot=[%s] item=[%s]", slotName, itemName)
            resolved = TemplateGetNode.get_default_value(client_context)

        YLogger.debug(client_context, "nluslot [%s] resolved to [%s:%s]", slotName, itemName, resolved)

        return resolved

    def to_string(self):
        return "[nluslot]"

    def to_xml(self, client_context):
        xml = "<nluslot>"
        xml += "<name>"
        xml += self._slotName.to_xml(client_context)
        xml += "</name>"
        xml += "<item>"
        xml += self._itemName.to_xml(client_context)
        xml += "</item>"
        if self._index is not None:
            xml += "<index>"
            xml += self._index.to_xml(client_context)
            xml += "</index>"
        xml += self.children_to_xml(client_context)
        xml += "</nluslot>"
        return xml

    # ######################################################################################################
    # JSON_PREDICATE_EXPRESSION ::==
    # <json name="JSONName">TEMPLATE_EXPRESSION</json> |

    def parse_expression(self, graph, expression):

        if 'name' in expression.attrib:
            self._slotName = self.parse_attrib_value_as_word_node(graph, expression, 'name')

        if 'item' in expression.attrib:
            self._itemName = self.parse_attrib_value_as_word_node(graph, expression, 'item')

        if 'index' in expression.attrib:
            self._index = self.parse_attrib_value_as_word_node(graph, expression, 'index')

        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:
            tagName = TextUtils.tag_from_text(child.tag)

            if tagName == 'name':
                self._slotName = self.parse_children_as_word_node(graph, child)
            if tagName == 'item':
                self._itemName = self.parse_children_as_word_node(graph, child)
            if tagName == 'index':
                self._index = self.parse_children_as_word_node(graph, child)
            else:
                graph.parse_tag_expression(child, self)
                self.parse_text(graph, self.get_tail_from_element(child))

        if self._slotName is None or self._itemName is None:
            raise ParserException("Missing either slot or item", xml_element=expression, nodename='nluslot')
