import unittest

from leafnode import LeafNode
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_to_node1(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(str(node.text_node_to_html_node()), str(LeafNode("b", "This is a text node")))

    def test_to_node2(self):
        node = TextNode("Image Name", TextType.IMAGE, "/src/image.jpg")
        self.assertEqual(str(node.text_node_to_html_node()), str(LeafNode("img", None, {"src":"/src/image.jpg","alt":"Image Name"})))

    



if __name__ == "__main__":
    unittest.main()