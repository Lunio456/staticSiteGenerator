import unittest

from htmlnode import *
from textnode import *
from helper import *


class TestHelper(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(new_nodes),str([
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]))

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold text** with a **bold block**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(new_nodes),str([
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold text", TextType.BOLD),
            TextNode(" with a ", TextType.NORMAL),
            TextNode("bold block", TextType.BOLD)
        ]))

    def test_split_nodes_delimiter_bold_code(self):
        node1 = TextNode("This is text with a `code block` word", TextType.NORMAL)
        node2 = TextNode("This is **bold text** with a **bold block**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertEqual(str(new_nodes),str([
            TextNode("This is text with a `code block` word", TextType.NORMAL),
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold text", TextType.BOLD),
            TextNode(" with a ", TextType.NORMAL),
            TextNode("bold block", TextType.BOLD)
        ]))

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text),[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text),[("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes,[
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ])

    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes,[
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ])

    def test_split_nodes_images_one_element(self):
        node = TextNode(
            "![LOTR image artistmonkeys](/images/rivendell.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes,[
            TextNode("LOTR image artistmonkeys", TextType.IMAGE, "/images/rivendell.png"),
        ])

    def test_text_to_textnodes(self):
        self.assertEqual(text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"),[
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ] )

    def test_split_blocks(self):
        self.assertEqual(markdown_to_blocks("# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n" + 
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item \n\n\n"),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ])

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# This is a heading"),"heading")

    def test_markdown_to_html_node_heading(self):
        self.assertEqual(str(markdown_to_html_node("# This is a heading")),
                         str(ParentNode("div",[ParentNode("h1",[LeafNode(None,"This is a heading")])])))
        
    def test_markdown_to_html_node_quote(self):
        self.assertEqual(str(markdown_to_html_node("> This is a heading")),
                         str(ParentNode("div",[ParentNode("blockquote",[LeafNode(None,"This is a heading")])])))
        
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"),"Hello")

    def test_markdown_to_html_node_text(self):
        self.assertEqual(str(markdown_to_html_node("Splendid! Then we have an accord:")),
                         str(ParentNode("div",[ParentNode("p",[LeafNode(None,"Splendid! Then we have an accord:")])])))


if __name__ == "__main__":
    unittest.main()