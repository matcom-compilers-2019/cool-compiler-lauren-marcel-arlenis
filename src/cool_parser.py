from cool_tokens import tokens
import ply.lex as lex
import ply.yacc as yacc
from ply.lex import TOKEN
from cool_lexer import Cool_Lexer
import cool_ast_hierarchy as ast_cool

class Cool_Parser:
    # Methods for parser
    def __init__(self, errors, lexer = None): 
        self.errors = errors
        self.tokens = tokens
        self.lexer = lexer if lexer else Cool_Lexer(self.errors)               
        self.parser = yacc.yacc(module=self)
    
    def parse(self, data_input):
        return self.parser.parse(data_input)

    # Rules
    def p_program(self, p):
        """
        program : list_class
        """
        p[0] = ast_cool.ProgramNode(p[1])

    def p_list_class_1(self, p):
        """
        list_class : decl_class SEMICOLON list_class
        """
        p[0] = [p[1]] + p[3]

    def p_list_class_2(self, p):
        """
        list_class : decl_class SEMICOLON
        """
        p[0] = [p[1]]

    def p_decl_class(self, p):
        """
        decl_class : class 
                   | class_inh
        """
        p[0] = p[1]

    def p_class(self, p):
        """
        class : CLASS TYPE OCURLY feature_list CCURLY
        """
        p[0] = ast_cool.ClassDecl(p[2], p[4][0], p[4][1])

    def p_class_inh(self, p):
        """
        class_inh : CLASS TYPE INHERITS TYPE OCURLY feature_list CCURLY
        """
        p[0] = ast_cool.ClassInh(p[2], p[4], p[6][0], p[6][1])

    def p_feature_list_1(self, p):
        """
        feature_list : method SEMICOLON feature_list
        """
        p[0] = (p[3][0], [p[1]] + p[3][1])
        
    def p_feature_list_2(self, p):
        """
        feature_list : attribute SEMICOLON feature_list
        """
        p[0] = ([p[1]] + p[3][0], p[3][1])

    def p_feature_list_3(self, p):
        """
        feature_list : empty
        """  
        p[0] = ([], [])

    def p_method(self, p):
        """
        method : ID OPAREN params_method CPAREN COLON TYPE OCURLY general_expression CCURLY
        """  
        p[0] = ast_cool.Method(p[1], p[3], p[6], p[8])

    def p_params_method_1(self, p):
        """
        params_method : params
        """
        p[0] = p[1]

    def p_params_method_2(self, p):
        """
        params_method : empty
        """
        p[0] = []
        
    def p_params_1(self, p):
        """
        params : declaration COMMA params
        """
        p[0] = [p[1]] + p[3]

    def p_params_2(self, p):
        """
        params : declaration
        """
        p[0] = [p[1]]

    def p_attribute_1(self, p):
        """
        attribute : declaration
        """
        p[0] = ast_cool.Attr_Declaration(p[1])

    def p_attribute_2(self, p):
        """
        attribute : declaration arrow
        """
        p[0] = ast_cool.Attr_Init(p[1], p[2])

    def p_declaration(self, p):
        """
        declaration : ID COLON TYPE
        """
        p[0] = ast_cool.DeclarationOnly((p[1], p[3]))

    def p_arrow(self, p):
        """
        arrow : ASSIGN general_expression
        """
        p[0] = p[2]

    def p_general_expression(self, p):
        """
        general_expression : assignment
                           | comparison_expression
        """
        p[0] = p[1]

    def p_assignment(self, p):
        """
        assignment : ID arrow
        """
        p[0] = ast_cool.Assignment(ast_cool.Variable(p[1]), p[2])

    def p_comparison_expression_1(self, p):
        """
        comparison_expression : NOT comparison
        """
        p[0] = ast_cool.Not(p[2])

    def p_comparison_expression_2(self, p):
        """
        comparison_expression : comparison
        """
        p[0] = p[1]

    def p_comparison_1(self, p):
        """
        comparison : comparison LT arithmetic
        """
        p[0] = ast_cool.LessThan(p[1], p[3])

    def p_comparison_2(self, p):
        """
        comparison : comparison LTEQ arithmetic
        """
        p[0] = ast_cool.LessEqualThan(p[1], p[3])

    def p_comparison_3(self, p):
        """
        comparison : comparison EQUAL arithmetic
        """
        p[0] = ast_cool.Equal(p[1], p[3])

    def p_comparison_4(self, p):
        """
        comparison : arithmetic
        """
        p[0] = p[1]
    
    def p_arithmetic_1(self, p):
        """
        arithmetic : arithmetic PLUS term
        """
        p[0] = ast_cool.PlusNode(p[1], p[3])

    def p_arithmetic_2(self, p):
        """
        arithmetic : arithmetic MINUS term
        """
        p[0] = ast_cool.MinusNode(p[1], p[3])

    def p_arithmetic_3(self, p):
        """
        arithmetic : term
        """
        p[0] = p[1]

    def p_term_1(self, p):
        """
        term : term STAR interatom
        """
        p[0] = ast_cool.StarNode(p[1], p[3])

    def p_term_2(self, p):
        """
        term : term DIVIDE interatom
        """
        p[0] = ast_cool.DivNode(p[1], p[3])

    def p_term_3(self, p):
        """
        term : interatom
        """
        p[0] = p[1]

    def p_interatom_1(self, p):
        """
        interatom : atomexpression
        """
        p[0] = p[1]

    def p_interatom_2(self, p):
        """
        interatom : ISVOID atomexpression
        """
        p[0] = ast_cool.IsVoid(p[2])  

    def p_atomexpression_1(self, p):
        """
        atomexpression : atom
        """
        p[0] = p[1]

    def p_atomexpression_2(self, p):
        """
        atomexpression : COMPLEMENT atom
        """
        p[0] = ast_cool.Neg(p[2])

    def p_atom_1(self, p):
        """
        atom : ID 
        """
        p[0] = ast_cool.Variable(p[1])

    def p_atom_2(self, p):
        """
        atom : const 
             | block 
             | dispatch
             | let
             | case
             | new
             | cond
             | loop
        """
        p[0] = p[1]

    def p_atom_3(self, p):
        """
        atom : OPAREN general_expression CPAREN
        """
        p[0] = p[2]

    def p_const_1(self, p):
        """
        const : BOOL
        """
        p[0] = ast_cool.Ctes(p[1], 'Bool')

    def p_const_2(self, p):
        """
        const : INTEGER
        """
        p[0] = ast_cool.Ctes(p[1], 'Int')

    def p_const_3(self, p):
        """
        const : STRING
        """
        p[0] = ast_cool.Ctes(p[1], 'String')

    def p_cond(self, p):
        """
        cond : IF general_expression THEN general_expression ELSE general_expression FI
        """
        p[0] = ast_cool.Conditional(p[2], p[4], p[6])

    def p_loop(self, p):
        """
        loop : WHILE general_expression LOOP general_expression POOL
        """
        p[0] = ast_cool.Loop(p[2], p[4])

    def p_block(self, p):
        """
        block : OCURLY general_expression SEMICOLON list_blocks CCURLY
        """
        p[0] = ast_cool.Block([p[2]] + p[4])

    def p_list_blocks_1(self, p):
        """
        list_blocks : general_expression SEMICOLON list_blocks
        """
        p[0] = [p[1]] + p[3]
    
    def p_list_blocks_2(self, p):
        """
        list_blocks : empty
        """
        p[0] = []

    def p_let(self, p):
        """
        let : LET list_let IN general_expression
        """
        p[0] = ast_cool.Let(p[2], p[4])

    def p_list_let_1(self, p):
        """
        list_let : declaration_let COMMA list_let
        """
        p[0] = [p[1]] + p[3]

    def p_list_let_2(self, p):
        """
        list_let : declaration_let
        """
        p[0] = [p[1]]

    def p_declaration_let_1(self, p):
        """
        declaration_let : declaration
        """
        p[0] = p[1]

    def p_declaration_let_2(self, p):
        """
        declaration_let : declaration arrow
        """
        p[0] = ast_cool.DeclarationWithInitialization(p[1],p[2])
        
    def p_case(self, p):
        """
        case : CASE general_expression OF list_case ESAC
        """
        p[0] = ast_cool.Case(p[2], p[4])

    def p_list_case_1(self, p):
        """
        list_case : declaration ARROW general_expression SEMICOLON
        """
        p[0] = [ast_cool.CaseExpr(p[1], p[3])]

    def p_list_case_2(self, p):
        """
        list_case : declaration ARROW general_expression SEMICOLON list_case
        """
        p[0] = [ast_cool.CaseExpr(p[1], p[3])] + p[5]

    def p_new(self, p):
        """
        new : NEW TYPE
        """
        p[0] = ast_cool.New(p[2])

    def p_dispatch(self, p):
        """
        dispatch : static_dispatch
                 | dinamic_dispatch
        """
        p[0] = p[1]

    def p_dinamic_dispatch_1(self, p):
        """
        dinamic_dispatch : call
        """
        p[0] = ast_cool.DispatchSelf(p[1][0], p[1][1])

    def p_dinamic_dispatch_2(self, p):
        """
        dinamic_dispatch : atom DOT call
        """
        p[0] = ast_cool.DispatchDot(p[1], p[3][0], p[3][1])

    def p_static_dispatch(self, p):
        """
        static_dispatch : atom AT TYPE DOT call
        """
        p[0] = ast_cool.StaticDispatch(p[1], p[3], p[5][0], p[5][1])

    def p_call(self, p):
        """
        call : ID OPAREN dispatch_list CPAREN
        """
        p[0] = (p[1], p[3])

    def p_dispatch_list_1(self, p):
        """
        dispatch_list : expression_list
        """
        p[0] = p[1]

    def p_dispatch_list_2(self, p):
        """
        dispatch_list : empty
        """
        p[0] = []

    def p_expression_list_1(self, p):
        """
        expression_list : general_expression
        """
        p[0] = [p[1]]

    def p_expression_list_2(self, p):
        """
        expression_list : general_expression COMMA expression_list
        """
        p[0] = [p[1]] + p[3]

    def p_empty(self, p):
        """ 
        empty : 
        """        
        pass

    # Error rule for syntax errors
    def p_error(self, p):
        if p is None:
            self.errors.append("({}, {}) - SyntacticError: Error! Fin de entrada inesperado!".format(p.lineno, p.lexpos))
            # print("Error! Unexpected end of input!")
        else:
            error = "({}, {}) - SyntacticError: Error! character: {}, type: {}".format(
                p.lineno, p.lexpos, p.value, p.type)
            self.errors.append(error)
