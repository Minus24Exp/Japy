import sys
import os.path

from .compiler.Compiler import Compiler
from .parser.Lexer import Lexer
from .parser.Parser import Parser, JacyError


class Jacy:
    debug = False
    main_file = ''

    lexer: Lexer
    parser: Parser
    compiler: Compiler

    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.compiler = Compiler()

    def launch(self):
        script_argv = []
        
        for arg in sys.argv:
            if arg[0] == '-':
                if arg == '-debug':
                    self.debug = True
                else:
                    script_argv.append(arg)
            else:
                if arg.endswith('.jc') and not self.main_file:
                    self.main_file = arg

        if not self.main_file:
            self.run_repl()
        else:
            self.run_script(self.main_file)

    def run_repl(self):
        while True:
            try:
                self.run(input('> '), 'REPL')
            except EOFError as e:
                print('Uncaught eof error', e)
            except JacyError as e:
                print('[ERROR]:', e)
            # except Exception as e:
            #     print('Uncaught error:', e)

    def run_script(self, path):
        if not os.path.exists(path):
            print('File', path, 'does not exist')
            return

        file = open(path, mode='r')

        # try:
        self.run(file.read(), path)
        # except Exception as e:
        #     print('\u001b[31m', str(e).strip(), '\u001b[0m', sep='')

    def run(self, script: str, file_name: str):
        tokens = self.lexer.lex(script, file_name)
        print('Tokens:')
        for t in tokens:
            print(str(t))
        tree = self.parser.parse(tokens)
        self.compiler.eval(tree)