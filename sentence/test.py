# -*- coding: utf-8 -*-

import argparse
import sys

import docutils.nodes
import docutils.parsers.rst
import docutils.utils

title = ''

class MyVisitor(docutils.nodes.GenericNodeVisitor):
    def visit_list_item(self, node):
        sentence = node[0]
        notes = node[1]
        item = ''
        for child in sentence.children:
            if child.tagname == 'strong':
                item = child.children[0]
                break

        item = item + '\t' + sentence.rawsource.replace('*', '').replace('\n', ' ')
        for child in notes.children:
            if child == notes.children[0]:
                item = item + '\t'
            else:
                item = item + '<br>'
            item = item + child.rawsource.replace('*', '').replace('\n', ' ')
        if (title):
            item = item + '\t' + title
        item += '\n'
        store_anki_item_to_list(item)

    def visit_title(self, node):
        global title
        title = node.rawsource

    def default_visit(self, node):
        pass

def store_anki_item_to_list(item = '', L=[]):
    L.append(item)
    return L

def write_items_to_anki_file(items, file_name):
    with open(file_name[:-4] + '.txt', 'w+', encoding='utf-8') as f:
        for item in items:
            f.write(item)

def create_anki_file_from_rst(fileobj):
    # Parse the file into a document with the rst parser.
    default_settings = docutils.frontend.OptionParser(
        components=(docutils.parsers.rst.Parser,)).get_default_values()
    document = docutils.utils.new_document(fileobj.name, default_settings)
    parser = docutils.parsers.rst.Parser()
    parser.parse(fileobj.read(), document)

    # Visit the parsed document with our link-checking visitor.
    visitor = MyVisitor(document)
    document.walk(visitor)
    write_items_to_anki_file(store_anki_item_to_list(), fileobj.name)


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('infile', nargs='?', type=argparse.FileType('r', encoding='utf-8'),
                           default=sys.stdin)
    args = argparser.parse_args()
    if args.infile.name[-4:] != '.rst':
        print("Please input rst file!!!")
        return
    print('Reading', args.infile.name)
    create_anki_file_from_rst(args.infile)

if __name__ == '__main__':
    main()
