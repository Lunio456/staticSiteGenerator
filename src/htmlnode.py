class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        s=""
        for e in self.props.keys():
            s+= f"{e}=\"{self.props[e]}\" "
        return s[:-1]
    

    def __repr__(self):
        s = "tag=" + str(self.tag) + "\n"
        s += "value=" + str(self.value) + "\n"
        s += "children=" + str(self.children) + "\n"
        s += "props=" + str(self.props) + "\n"
        return s

