import unittest

from parentnode import *
from leafnode import *


class TestParentNode(unittest.TestCase):
    def test_to_HTML1(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_HTML2(self):
        node = ParentNode(
            "p",None
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_HTML3(self):
        node = ParentNode(
            "p",
            [
                ParentNode("b", [
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                ]),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Normal text<i>italic text</i></b>Normal text</p>")
    

if __name__ == "__main__":
    unittest.main()