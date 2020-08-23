

class Compiler:
    def __init__(self):
        pass

    def eval(self, tree):
        for stmt in tree:
            stmt.visit(self)

    ##############
    # Statements #
    ##############
    def visit_block(self, block):
        print('visit', block)

    def visit_class_decl(self, class_decl):
        print('visit', class_decl)

    def visit_for_stmt(self, for_stmt):
        print('visit', for_stmt)

    def visit_func_decl(self, func_decl):
        print('visit', func_decl)

    def visit_import(self, imp):
        print('visit', imp)

    def visit_return_stmt(self, ret):
        print('visit', ret)

    def visit_type_decl(self, t):
        print('visit', t)

    def visit_var_decl(self, var_decl):
        print('visit', var_decl)

    def visit_while_stmt(self, while_stmt):
        print('visit', while_stmt)

    ###############
    # Expressions #
    ###############
    def visit_assign(self, assign):
        print('visit', assign)

    def visit_dict_expr(self, dict_expr):
        print('visit', dict_expr)

    def visit_func_call(self, func_call):
        print('visit', func_call)

    def visit_get_expr(self, get_expr):
        print('visit', get_expr)

    def visit_get_item(self, get_item):
        print('visit', get_item)

    def visit_id(self, iden):
        print('visit', iden)

    def visit_if_expr(self, if_expr):
        print('visit', if_expr)

    def visit_infix(self, infix):
        print('visit', infix)

    def visit_list_expr(self, list_expr):
        print('visit', list_expr)

    def visit_null(self, null):
        print('visit', null)

    def visit_bool(self, _bool):
        print('visit', _bool)

    def visit_int(self, _int):
        print('visit', _int)

    def visit_float(self, _float):
        print('visit', _float)

    def visit_string(self, string):
        print('visit', string)

    def visit_prefix(self, prefix):
        print('visit', prefix)

    def visit_set_expr(self, set_expr):
        print('visit', set_expr)

    def visit_set_item(self, set_item):
        print('visit', set_item)
