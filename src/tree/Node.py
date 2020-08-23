class Node:
    def visit(self, compiler):
        raise Exception('Attempt to visit base Node')