class Node:
   pass

class Void(Node):
    def __init__(self):
        self.computedType = 'Void'

class ProgramNode(Node):
    def __init__(self, classList):
        self.classList = classList

class ExpressionNode(Node):
    pass

class Arithmetic(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Assignment(ExpressionNode):  #llrga la variable en id
    def __init__(self, asid, expr):
        self.id = asid
        self.expr = expr

class Conditional(ExpressionNode):
    def __init__(self, ifexpr, thenexpr,elseexpr):
        self.ifexpr = ifexpr
        self.thenexpr = thenexpr
        self.elseexpr = elseexpr

class Loop(ExpressionNode):
    def __init__(self, whileexpr, loopexpr):
        self.whileexpr = whileexpr
        self.loopexpr = loopexpr

class Block(ExpressionNode):
    def __init__(self, exprlist):
        self.exprlist = exprlist

class Compare(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Equal(Compare):
    # def __init__(self, left, right):
    #     self.left = left
    #     self.right = right
    pass
    
class CompareNotEqual(Compare):
    pass

class LessThan(CompareNotEqual):
    pass

class LessEqualThan(CompareNotEqual):
    pass
  
class PlusNode(Arithmetic):
    # def __init__(self, left, right):
    #     Arithmetic.__init__(self, left, right)
    pass
    
class MinusNode(Arithmetic):
    pass

class StarNode(Arithmetic):
    pass

class DivNode(Arithmetic):
    pass

class IsVoid(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr

class New(ExpressionNode):
    def __init__(self, newType):
       self.newType =  newType

class Not(ExpressionNode):
    def __init__(self,expr):
        self.expr = expr

class Neg(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr

class Let(ExpressionNode):
    def __init__(self, letAttrList,body):
        self.letAttrList = letAttrList
        self.body = body


# class LetAttr_Init(ExpressionNode):
#     def __init__(self, name_AttrType, expr):
#         self.name = name_AttrType[0]
#         self.attrType = name_AttrType[1]
#         self.expr = expr

# class LetAttr_Declaration(ExpressionNode):
#     def __init__(self, name_attrType):
#         self.name = name_attrType[0]
#         self.attrType = name_attrType[1]

class Declaration(ExpressionNode):
    def __init__(self, attrName, attrType, expr):
        self.attrName = attrName
        self.attrType = attrType    
        self.expr = expr

class DeclarationWithInitialization(Declaration):
    def __init__(self, decl_only, expr):
        super(DeclarationWithInitialization,self).__init__(decl_only.attrName,decl_only.attrType,expr)
        # self.expr = expr

class DeclarationOnly(Declaration):
    def __init__(self, name_attrType):
        thetype = name_attrType[1]
        default = Void()
        if thetype == "Bool":
            default = Ctes(False,"Bool")
        elif thetype == "Int":
            default = Ctes(0,"Int")
        elif thetype == "String":
            default = Ctes("","String")
        super(DeclarationOnly,self).__init__(name_attrType[0],name_attrType[1],default)
            


class Case(ExpressionNode):
    def __init__(self, case0,exprList):
        self.case0 = case0 
        self.exprList = exprList 

class CaseExpr(ExpressionNode):
    def __init__(self, decl,expr):
        self.decl = decl # tupla name,type
        self.expr = expr 

class CoolClass(ExpressionNode):
    def __init__(self, name,parent,attrs,methods):
        self.name = name
        # self.expr = expr
        self.attrs = attrs
        self.methods = methods
        self.parent = parent

class ClassDecl(CoolClass):
    def __init__(self, name,attrs,methods):
        super(ClassDecl,self).__init__(name,"Object",attrs,methods)
        # self.name = name
        # # self.expr = expr
        # self.attrs = attrs
        # self.methods = methods

class ClassInh(CoolClass):
    pass
    # def __init__(self, name,parent,methods,attrs):
        # self.name = name
        # # self.expr = expr
        # self.attrs = attrs
        # self.methods = methods
        # self.parent = parent

class Method(ExpressionNode):
    def __init__(self, name, paramsList, returnType, exprbody):
        self.name = name
        self.returnType = returnType
        self.paramsList = paramsList
        self.exprbody = exprbody


class DispatchSelf(ExpressionNode):
    def __init__(self, methodName, paramsList):
        self.methodName = methodName
        self.paramsList = paramsList

class DispatchDot(ExpressionNode):
    def __init__(self, expr0, methodName, paramsList):
        self.expr0 = expr0
        self.methodName = methodName
        self.paramsList = paramsList
        

class StaticDispatch(ExpressionNode):
    def __init__(self, dispObject, className,methodName,paramsList):
        self.dispObject = dispObject
        self.className = className
        self.methodName = methodName
        self.paramsList = paramsList
        

class Attribute(ExpressionNode):
    def __init__(self, name_attrType,expr):
        self.attrName = name_attrType.attrName
        self.attrType = name_attrType.attrType
        self.expr = expr

class Attr_Init(Attribute):
    def __init__(self, name_attrType, expr):
        super(Attr_Init,self).__init__(name_attrType,expr)

class Attr_Declaration(Attribute):
    def __init__(self, name_attrType):
        super(Attr_Declaration,self).__init__(name_attrType,name_attrType.expr)


class Ctes(ExpressionNode):
    def __init__(self, value,ctetype):
        self.value = value
        self.type = ctetype


class Variable(ExpressionNode):
    def __init__(self, name):
        self.name = name

