

import os
import re
import shutil
from htmlnode import HTMLNode
from parentnode import ParentNode
from textnode import *


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    newnodes = []

    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            textlist  = node.text.split(delimiter)
            for i in range(0,len(textlist)):
                if len(textlist[i])>0:
                    if i % 2 == 0:
                        newnodes.append(TextNode(textlist[i],TextType.NORMAL))
                    else:
                        newnodes.append(TextNode(textlist[i],text_type))
        else:
            newnodes.append(node)
    
    return newnodes


def extract_markdown_images(text):
    images = []
    for image in re.findall("!\[[^\]]+\]\([^\)]+\)",text):
        tupel = image.split("](")
        images.append((tupel[0][2:],tupel[1][:-1]))
    return images

def extract_markdown_links(text):
    links = []
    for image in re.findall("\[[^\]]+\]\([^\)]+\)",text):
        tupel = image.split("](")
        links.append((tupel[0][1:],tupel[1][:-1]))
    return links

def split_nodes_link(old_nodes):

    newNodes = []

    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            links = extract_markdown_links(node.text)
            text = re.split("\[[^\]]+\]\([^\)]+\)",node.text)
            for i in range(0,len(links)):
                if len(text[i])>0:
                    newNodes.append(TextNode(text[i],TextType.NORMAL))
                newNodes.append(TextNode(links[i][0],TextType.LINK,links[i][1]))
            if len(text[len(text)-1])>0:
                newNodes.append(TextNode(text[len(text)-1],TextType.NORMAL))
        else:
            newNodes.append(node)
    
    return newNodes

def split_nodes_image(old_nodes):

    newNodes = []

    for node in old_nodes:
        if node.text_type == TextType.NORMAL:
            images = extract_markdown_images(node.text)
            text = re.split("!\[[^\]]+\]\([^\)]+\)",node.text)
            for i in range(0,len(images)):
                if len(text[i])>0:
                    newNodes.append(TextNode(text[i],TextType.NORMAL))
                newNodes.append(TextNode(images[i][0],TextType.IMAGE,images[i][1]))
            if len(text[len(text)-1])>0:
                newNodes.append(TextNode(text[len(text)-1],TextType.NORMAL))
        else:
            newNodes.append(node)
    
    return newNodes

def text_to_textnodes(text):

    textnodes = [TextNode(text,TextType.NORMAL)]

    textnodes = split_nodes_delimiter(textnodes,"**",TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes,"*",TextType.ITALIC)
    textnodes = split_nodes_delimiter(textnodes,"`",TextType.CODE)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)

    return textnodes

def text_to_leafnodes(text):

    textnodes = text_to_textnodes(text)
    leafnodes = []
    for text in textnodes:
        leafnodes.append(text.text_node_to_html_node())
    
    return leafnodes


def markdown_to_blocks(markdown):

    blocks = markdown.split("\n\n")
    stripedblocks = []

    for i in range(0,len(blocks)):
        blocks[i] = blocks[i].strip()
        if len(blocks[i])>0:
            stripedblocks.append(blocks[i])

    return stripedblocks

def block_to_block_type(block):

    match block[:2]:
        case "# ":
            return "heading"
        case "##":
            return "heading"
        case "``":
            return "code"
        case "> ":
            return "quote"
        case "* ":
            return "unordered_list"
        case "- ":
            return "unordered_list"
        case "1.":
            return "ordered_list"

    return "paragraph"    

def heading_type(block):
        
    if block[:6] == "######":
        return "h6"
    if block[:5] == "#####":
        return "h5"
    if block[:4] == "####":
        return "h4"
    if block[:3] == "###":
        return "h3"
    if block[:2] == "##":
        return "h2"
    else:
        return "h1" 


def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)
    nodes = []

    for block in blocks:
        match block_to_block_type(block):
            case "heading":
                nodes.append(ParentNode(heading_type(block),text_to_leafnodes(re.sub("#+\s","",block))))
            case "code":
                nodes.append(ParentNode("pre",[ParentNode("code",text_to_leafnodes(block.replace("```","")))]))
            case "ordered_list":
                nodes.append(ParentNode("ol",html_node_split_list(re.sub("\d+\.\s","",block))))
            case "unordered_list":
                nodes.append(ParentNode("ul",html_node_split_list(block.replace("* ","").replace("- ",""))))
            case "quote":
                nodes.append(ParentNode("blockquote",text_to_leafnodes(block.replace("> ",""))))
            case "paragraph":
                nodes.append(ParentNode("p",text_to_leafnodes(block)))

    return ParentNode("div",nodes)

    
def html_node_split_list(text):

    nodes = []

    for line in text.split("\n"):
        nodes.append(ParentNode("li",text_to_leafnodes(line)))

    return nodes


def copy_directory(source,target):

    if os.path.exists(source)==False:
        raise Exception("Source does not exist")
    
    if os.path.exists(target)==True:
        shutil.rmtree(target)

    shutil.copytree(source, target)

def extract_title(markdown):

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block)=="heading":
            if heading_type(block) == "h1":
                return re.sub("#+\s","",block)
    
    raise Exception("No title found")


def generate_path(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        markdown = open(from_path,"r").read()
        template = open(template_path,"r").read()
    except Exception as e:
        print(type(e).__name__)


    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    
    open(dest_path,"w").write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    for file in os.listdir(dir_path_content):
        if os.path.isdir(dir_path_content + "/" + file) == True:
            os.makedirs(dest_dir_path + "/" + file)
            generate_pages_recursive(dir_path_content + "/" + file, template_path, dest_dir_path + "/" + file)
        if os.path.splitext(file)[1] == ".md":
            generate_path(dir_path_content+ "/" + file, template_path, dest_dir_path+ "/" + file.replace(".md",".html"))

