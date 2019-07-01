from cool_lexer import Cool_Lexer
from cool_parser import Cool_Parser
from ast_painter import PrintVisitor
from ast_cil_painter import PrintVisitorCIL
from cil_types import CILTypes
import check_semantic
import get_hierarchy
import context
import cool_to_cil as ctc
from  mips import VisitorMIPS
import os

class Compiler:
    def __init__(self, *args, **kwargs):
        self.errors = []
        self.lexer = Cool_Lexer(self.errors)
        self.parser = Cool_Parser(self.errors, lexer = Cool_Lexer)

    def _checksemantic(self, hast, context_):
        typeCollector = get_hierarchy.VisitorTypeCollector()
        typeCollector.visit(hast, context_, self.errors)
        # print("hierarchy", context_.hierarchy)

        if not len(self.errors):
            # print("errors", self.errors)        
            checksem = check_semantic.VisitorCheckSemantic()
            checksem.visit(hast, context_, self.errors)

    def _ciltypes(self, hast, hierarchy_):
        cil_types = CILTypes(hierarchy_)
        return cil_types.visit(hast)
    
    def _cooltocil(self, hast, hast2):
        cool_to_cil_visitor = ctc.COOLToCILVisitor(hast2)
        return cool_to_cil_visitor.visit(hast)

    def tokenize(self, data_input):
        # f = open('./tokens.txt', 'w')
        self.lexer.input(data_input)

        while True:
            tok = self.lexer.token()
            if not tok: 
                break
            # print(tok.type, tok.value, tok.lineno, tok.lexpos)
            # f.write(str(tok.type) + ' ' + str(tok.value) + ' ' + str(tok.lexpos) + '\n')

        # f.close()

    def parse(self, data_input):
        return self.parser.parse(data_input) 

    def compile(self, file_name):
        print("The_Coolest v1.0")
        print("Copyright (c) 2019: Lauren, Marcel, Arlenis")

        file = None
        try: 
           file = open(file_name)
        except:
            print("(0, 0) - CompilerError: No existe el fichero {}".format(file_name))
            exit(0)

        data = file.readlines()
        data = "".join(data)
        file.close()

        file_name = file_name[:-3] + '.mips'

        compiler = Compiler()
        compiler.tokenize(data)

        if not len(compiler.errors):
            ast = compiler.parse(data)

            if not len(compiler.errors):
                context_ = context.Context()
                pvisitor = PrintVisitor()
                pvisitor_cil = PrintVisitorCIL()
                # print("----------------AST----------------")
                # print(pvisitor.visit(ast, -1))

                res = compiler._checksemantic(ast, context_)
                # print("----------------Check Semantic----------------")
                # print(pvisitor.visit(ast, -1))

                if not len(compiler.errors) and not (res == "ERROR"):
                    # print("----------------Ordenado----------------")
                    # print(pvisitor.visit(ast, -1))

                    cil_types = compiler._ciltypes(ast, context_.hierarchy)
                    # print("----------------CIL Types----------------")
                    # print(pvisitor_cil.visit(cil_types, -1))

                    # print("----------------CIL----------------")
                    cil_ast = compiler._cooltocil(ast, cil_types)
                    # print(pvisitor_cil.visit(cil_ast, -1))

                    myfile = open(file_name, 'w')
                    mips = VisitorMIPS()
                    res = mips.visit(cil_ast)
                    myfile.write(res)  
                    myfile.close()              

                else:
                    # print("------------Errors---------------")
                    # print("Errores sem'anticos: ")
                    # myfile.write("Errores sem'anticos: ")
                    for i, error in enumerate(compiler.errors):
                        # error = "Error {}: {} ".format(i+1, error)
                        print(error)
                        # myfile.write(error)
                        exit(0)
                
            else:
                # print("------------Errors---------------")
                # myfile.write("Errores sint'acticos: ")
                # print("Errores sint'acticos: ")
                for i, error in enumerate(compiler.errors):
                    # error = "Error {}: {} ".format(i+1, error)
                    print(error)
                    # myfile.write(error)
                    exit(0)

        else:
            # print("------------Errors---------------")
            # myfile.write("Errores sint'acticos: ")
            # print("Errores sint'acticos: ")
            for i, error in enumerate(compiler.errors):
                # error = "Error {}: {} ".format(i+1, error)
                print(error)
                # myfile.write(error)
                exit(0)


        os.system('spim -f ' + file_name)