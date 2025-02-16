

from htmlnode import *


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        htmlString = ""
        if self.tag == None:
            raise ValueError("No Tag")
        if self.children == None:
            raise ValueError("No Children")
        for child in self.children:
             htmlString+=child.to_html()
        if self.props == None:
            return f"<{self.tag}>{htmlString}</{self.tag}>"
        else:
            return f"<{self.tag} {self.props_to_html()}>{htmlString}</{self.tag}>"

    

