import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_props_to_HTML(self):
        node = HTMLNode("p", "This is a text node", ["a","b"], {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(node.props_to_html(), "href=\"https://www.google.com\" target=\"_blank\"")
        

    def test_print(self):
        node = HTMLNode("p", "This is a text node", ["a","b"], {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(str(node), "tag=p\nvalue=This is a text node\nchildren=['a', 'b']\nprops={'href': 'https://www.google.com', 'target': '_blank'}")
    

if __name__ == "__main__":
    unittest.main()