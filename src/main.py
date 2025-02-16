from helper import *


def main():

    copy_directory("static","public")
    generate_pages_recursive("content","template.html","public")



main()