import sys
import os.path
from parser.Lexer import Lexer

class Jacy:
    debug = False
    main_file = ''

    lexer: Lexer

    def __init__(self):
        self.lexer = Lexer()

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
                self.run(input('> '))
            except Exception as err:
                print('[ERROR]:', err)
            except EOFError:
                break

    def run_script(self, path):
        if not os.path.exists(path):
            print('File', path, 'does not exist')
            return

        file = open(path, mode='r')

        self.run(file.read())

    def run(self, script: str):
        tokens = self.lexer.lex(script)
        print('tokens:', ''.join(str(t) for t in tokens))