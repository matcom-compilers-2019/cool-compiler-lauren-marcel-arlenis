import cool_ast_hierarchy as ast
import visitor

class PrintVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node, tabs):
        ans = 'Program'
        if node.classList:
            for class_node in node.classList:
                ans += '\n' + self.visit(class_node, tabs+1)
        return ans
    
    @visitor.when(ast.Assignment)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Assignment' + '(id: ' + node.id.name + ')\n' + self.visit(node.expr, tabs+1)
        return ans
    
    @visitor.when(ast.Conditional)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Conditional\n' + self.visit(node.ifexpr, tabs+1) + '\n' + self.visit(node.thenexpr, tabs+1) + '\n' + self.visit(node.elseexpr, tabs+1)
        return ans

    @visitor.when(ast.Loop)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Loop\n' + self.visit(node.whileexpr, tabs+1) + '\n' + self.visit(node.loopexpr, tabs+1)
        return ans

    @visitor.when(ast.Block)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Block' 
        if node.exprlist:
            for expr_node in node.exprlist:
                ans += '\n' + self.visit(expr_node, tabs+1)
        return ans

    @visitor.when(ast.Equal)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Equal\n' + self.visit(node.left, tabs+1) + '\n' + self.visit(node.right, tabs+1)
        return ans

    @visitor.when(ast.LessThan)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'LessThan\n' + self.visit(node.left, tabs+1) + '\n' + self.visit(node.right, tabs+1)
        return ans

    @visitor.when(ast.LessEqualThan)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'LessEquealThan\n' + self.visit(node.left, tabs+1) + '\n' + self.visit(node.right, tabs+1)
        return ans

    @visitor.when(ast.PlusNode)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'PlusNode\n' + self.visit(node.left, tabs+1) + '\n' + self.visit(node.right, tabs+1)
        return ans

    @visitor.when(ast.MinusNode)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'MinusNode\n' + self.visit(node.left, tabs+1) + '\n' + self.visit(node.right, tabs+1)
        return ans
    
    @visitor.when(ast.StarNode)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'StarNode\n' + self.visit(node.left, tabs+1) + '\n' + self.visit(node.right, tabs+1)
        return ans

    @visitor.when(ast.DivNode)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'DivNode\n' + self.visit(node.left, tabs+1) + '\n' + self.visit(node.right, tabs+1)
        return ans

    @visitor.when(ast.IsVoid)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'IsVoid\n' + self.visit(node.expr, tabs+1)
        return ans

    @visitor.when(ast.New)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'New(type: ' +  node.newType + ')' 
        return ans

    @visitor.when(ast.Not)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Not\n' + self.visit(node.expr, tabs+1)
        return ans
    
    @visitor.when(ast.Neg)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Neg\n' + self.visit(node.expr, tabs+1)
        return ans

    @visitor.when(ast.Let)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Let'
        if node.letAttrList:
            for attr in node.letAttrList:
                ans += '\n' + self.visit(attr, tabs+1)
        ans += '\n' + self.visit(node.body, tabs+1)
        return ans

    @visitor.when(ast.DeclarationOnly)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Declaration_Only(name: ' + node.attrName + ', type: ' + node.attrType + ')'
        return ans

    @visitor.when(ast.DeclarationWithInitialization)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'DeclarationWithInitialization(name: ' + node.attrName + ', type: ' + node.attrType + ')\n' + self.visit(node.expr, tabs + 1)
        return ans

    @visitor.when(ast.Case)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Case'
        ans += '\n' + self.visit(node.case0, tabs+1)
        if node.exprList:
            for case in node.exprList:
                ans += '\n' + self.visit(case, tabs+1)
        return ans

    @visitor.when(ast.CaseExpr)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'CaseExpr\n' + self.visit(node.decl, tabs + 1) + '\n' + self.visit(node.expr, tabs + 1)
        return ans

    @visitor.when(ast.ClassDecl)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'ClassDecl(name: ' + node.name + ')'
        if node.attrs:
            for attr in node.attrs:
                ans += '\n' + self.visit(attr, tabs + 1)
        if node.methods:
            for method in node.methods:
                ans += '\n' + self.visit(method, tabs + 1)
        return ans

    @visitor.when(ast.ClassInh)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'ClassInh(name: ' + node.name + ', parent: ' + node.parent +')'
        if node.attrs:
            for attr in node.attrs:
                ans += '\n' + self.visit(attr, tabs + 1)
        if node.methods:
            for method in node.methods:
                ans += '\n' + self.visit(method, tabs + 1)
        return ans

    @visitor.when(ast.Method)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Method(name: ' + node.name + ', type: ' + node.returnType
        if node.paramsList:
            for i, arg in enumerate(node.paramsList):
                ans += '\n' + self.visit(arg, tabs + 1)
        ans += ')'
        ans += '\n' + self.visit(node.exprbody, tabs + 1)                    
        return ans

    @visitor.when(ast.DispatchSelf)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'DispatchSelf(name: ' + node.methodName + ')'
        if node.paramsList:
            for param in node.paramsList:
                ans += '\n' + self.visit(param, tabs + 1)
                # ans += ', param' + str(i) + '\n' + a
        return ans

    @visitor.when(ast.DispatchDot)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'DispatchDot(name: ' + node.methodName + ')'
        ans += '\n' + self.visit(node.expr0, tabs + 1)
        if node.paramsList:
            for param in node.paramsList:
                ans += '\n' + self.visit(param, tabs + 1)
                # ans += ', param' + str(i) + '\n' + a
        return ans

    @visitor.when(ast.StaticDispatch)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'StaticDispatch(class_name: ' + node.className + ', method_name: ' + node.methodName + ')'
        ans += '\n' + self.visit(node.dispObject, tabs + 1)
        if node.paramsList:
            for i, param in enumerate(node.paramsList):
                ans += '\n' + '\t'*(tabs+1) + 'param' + str(i) + ': ' 
                ans += '\n' + self.visit(param, tabs+2)
        return ans

    @visitor.when(ast.Attr_Declaration)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Attr_Declaration(name: ' + node.attrName + ', type: ' + node.attrType + ')'
        return ans

    @visitor.when(ast.Attr_Init)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Attr_Init(name: ' + node.attrName + ', type: ' + node.attrType + ')\n' + self.visit(node.expr, tabs + 1)
        return ans

    @visitor.when(ast.Ctes)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Ctes(value: ' + str(node.value) + ', type: ' + node.type + ')'
        return ans

    @visitor.when(ast.Variable)
    def visit(self, node, tabs):
        ans = '\t'*tabs + '|___' + 'Variable(name: ' + node.name + ')'
        return ans