import visitor
import cool_ast_hierarchy as ast
# from context import Hierarchy
import context
# from hierarchy import TypeHierarchy as Hierarchy

ERROR = "ERROR"

# hierarchy = Hierarchy()

class VisitorCheckSemantic:
    @visitor.on('node')
    def visit(self, node, scope, errors):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node, scope, errors):
        # print("----------> ast.ProgramNode")
        # scope = context.Context()
        res = 0
        for classItem in node.classList:
            classScope = scope.CreateChildContext()
            classScope.currentClass = classItem.name
            for attr in classItem.attrs:
                # print(attr.attrName)
                res = self.visit(attr, classScope, errors)
                # res = res or self.visit(attr, scope, errors)
                # if res == ERROR:
                #     print("ERROR!!",res)
                    # return ERROR
            for meth in classItem.methods:
                # print(meth.name)
                res = self.visit(meth, classScope, errors)
                # if res == ERROR:
                #     print("ERROR!!!!",res)
                    # return ERROR
        # print("res",res)
        return res
        
    @visitor.when(ast.Arithmetic)
    def visit(self, node, scope, errors):
        # print("----------> ast.Arithmetic")
        left = self.visit(node.left,scope,errors)
        right = self.visit(node.right,scope,errors)
        if left == right and right == "Int":
            node.computedType = "Int"
            return "Int"
        node.computedType = ERROR
        errors.append("(0,0) -  TypeError :Ambas expresiones de una expresion aritm'etica deben ser de tipo Int")    
        return ERROR


    @visitor.when(ast.Assignment)
    def visit(self, node, scope, errors):
        # print("----------> ast.Assignment",node.id)
        # variableType = scope.IsDefineVariable(node.id)
        # if variableType == None:
        #     return ERROR
        if node.id.name == "self":
            errors.append("(0,0) -  SemanticError : En la clase " + scope.currentClass + ": " + "no se puede hacer una asignacion a la variable self")
        variableType = self.visit(node.id,scope,errors)
        exprType = self.visit(node.expr,scope,errors)
        if variableType == ERROR or exprType == ERROR:
            # errors.append("(0,0) -  SemanticError :(0,0) - En la clase " + )
            node.computedType = ERROR
            return ERROR
        if (exprType == variableType or scope.IsDerived(exprType,variableType)):
            node.computedType = exprType
            return exprType
        errors.append("(0,0) -  TypeError : En la clase " + scope.currentClass + ": " +"El tipo de la expresion asignada a la variable " + node.id.name +" debe ser "+ variableType +" y esta siendo "+exprType)
        node.computedType = ERROR
        return ERROR
        
    @visitor.when(ast.Conditional)
    def visit(self, node, scope, errors):
        # print("----------> ast.Conditional")
        ifexpr = self.visit(node.ifexpr,scope,errors)
        if ifexpr == "Bool":
            thenexpr = self.visit(node.thenexpr,scope,errors)
            elseexpr = self.visit(node.elseexpr,scope,errors)
            if thenexpr == ERROR or elseexpr == ERROR:
                errors.append("(0,0) -  SemanticError : En la clase " + scope.currentClass + ": " + "Hubo problemas en la evaluacion del if")
                node.computedType = ERROR
                return ERROR
            
            lcatype = scope.LCA(scope.hierarchy[thenexpr],scope.hierarchy[elseexpr])
            node.computedType = lcatype
            return lcatype
        errors.append("(0,0) -  TypeError : En la clase " + scope.currentClass + ": " + "La condicional debe ser de tipo Bool")
        node.computedType = ERROR
        return ERROR

    @visitor.when(ast.Loop)
    def visit(self, node, scope, errors):
        # print("----------> ast.Loop")
        whileexpr = self.visit(node.whileexpr,scope, errors)
        if whileexpr == "Bool":
            loopexpr = self.visit(node.loopexpr,scope,errors)
            if loopexpr == ERROR:
                node.computedType = ERROR
                return ERROR  
            node.computedType = "Object"
            return "Object"
        errors.append("(0,0) -  TypeError :En la clase " + scope.currentClass + ": "+ "La expresion del ciclo debe ser de tipo Bool")
        node.computedType = ERROR
        return ERROR
        
    @visitor.when(ast.Block)
    def visit(self, node, scope, errors):
        # print("----------> ast.Block")
        flag = False
        exprType = None
        for expr in node.exprlist:
            exprType = self.visit(expr,scope,errors)
            if exprType == ERROR:
                 flag = True
        if flag:
            node.computedType = ERROR
            return ERROR
        node.computedType = exprType
        return exprType

    @visitor.when(ast.Equal) 
    def visit(self, node, scope, errors):
        # print("----------> ast.Equal")
        left = self.visit(node.left,scope,errors)
        right = self.visit(node.right,scope,errors)
        a = ["Int","String","Bool"]
        if a.__contains__(left) or a.__contains__(right):
            if (left == right):
                node.computedType = "Bool"
                return "Bool"
            errors.append("(0,0) -  TypeError : En la clase " + scope.currentClass + ": " +"En una igualdad, ambas expresiones deben ser del mismo tipo")
            node.computedType = ERROR
            return ERROR
        elif left==ERROR or right==ERROR:
            node.computedType = ERROR
            return ERROR
        node.computedType = "Bool"
        return "Bool" 


    @visitor.when(ast.CompareNotEqual)
    def visit(self, node, scope, errors):
        # print("----------> ast.CompareNotEqual")
        left = self.visit(node.left,scope,errors)
        right = self.visit(node.right,scope,errors)
        # print("left,right",left,right)
        if left == right and right == "Int":
            node.computedType = "Bool"
            return "Bool"
        errors.append("(0,0) -  TypeError :  En la clase " + scope.currentClass + ": " +"Las expresiones de una comparacion deben ser ambas de tipo Int")
        node.computedType = ERROR
        return ERROR
    
    @visitor.when(ast.IsVoid)
    def visit(self, node, scope, errors):
        # print("----------> ast.IsVoid")
        if self.visit(node.expr,scope,errors) == ERROR:
            node.computedType = ERROR
            return ERROR  
        node.computedType = "Bool"
        return "Bool" 

    @visitor.when(ast.New)
    def visit(self, node, scope, errors):
        # print("----------> ast.New")
        if scope.IsDefineType(node.newType):
            node.computedType = node.newType
            return node.newType
        errors.append("(0,0) -  TypeError :En la clase " + scope.currentClass + ": " +"El tipo "+ node.newType +" no est'a definido")
        node.computedType = ERROR 
        return ERROR
    
    @visitor.when(ast.Not)
    def visit(self, node, scope, errors):
        # print("----------> ast.Not")
        expr = self.visit(node.expr,scope,errors)
        if expr == "Bool":
            node.computedType = "Bool"
            return "Bool" 
        errors.append("(0,0) -  TypeError :En la clase "+ scope.currentClass + ": la negaci'on solo puede aplicarse al tipo Int")
        node.computedType = ERROR
        return ERROR

    @visitor.when(ast.Neg)
    def visit(self, node, scope, errors):
        # print("----------> ast.Neg")
        expr = self.visit(node.expr,scope,errors)
        if expr == "Int":
            node.computedType = "Int"
            return "Int"  
        errors.append("(0,0) -  TypeError :En la clase "+ scope.currentClass + ": el complemento solo puede aplicarse al tipo Int")
        node.computedType = ERROR
        return ERROR

    @visitor.when(ast.Let)
    def visit(self, node, scope, errors):
        # print("----------> ast.Let")
        myscope = scope.CreateChildContext()
        flag = False
        for identifier in node.letAttrList:
            visit = self.visit(identifier,myscope,errors)
            if visit == ERROR:
                flag = True
            # myscope.defineVariable(identifiers.name,identifiers.attrType)
            # cdo revise adentro lo pone en myscope
        res = self.visit(node.body,myscope,errors)
        if res == ERROR:
            flag = True
        if flag:
            node.computedType = ERROR
            return ERROR
        node.computedType = res
        return res

    @visitor.when(ast.DeclarationOnly)
    def visit(self, node, scope, errors):
        # print("----------> ast.DeclarationOnly ",node.attrName)
        if node.attrName == "self":
            errors.append("(0,0) -  SemanticError :En la clase " + scope.currentClass + ": " +"NO se puede declarar una variable con  nombre self")
            node.computedType = ERROR
            return ERROR
        node.vinfo = scope.DefineVariable(node.attrName,node.attrType)
        node.computedType = node.attrType
        self.visit(node.expr, scope, errors)
        return node.attrType

    @visitor.when(ast.DeclarationWithInitialization)
    def visit(self, node, scope, errors):
        # print("----------> ast.DeclarationWithInitialization ",node.attrName)
        if node.attrName == "self":
            errors.append("(0,0) -  SemanticError :En la clase " + scope.currentClass + ": " +"NO se puede declarar una variable con  nombre self")
            node.computedType = ERROR
            return ERROR
        visitexpr = self.visit(node.expr,scope,errors)     
        if visitexpr == ERROR:
            node.computedType = ERROR
            return ERROR
        if visitexpr == node.attrType or scope.IsDerived(visitexpr, node.attrType):
            node.vinfo = scope.DefineVariable(node.attrName,node.attrType)
            node.computedType = node.attrType
            return node.attrType
        errors.append("(0,0) -  TypeError :En la clase " + scope.currentClass + ": " +"El tipo de la expresion tiene que ser "+ node.attrType)
        node.computedType = ERROR
        return ERROR
    
    @visitor.when(ast.Case)
    def visit(self, node, scope, errors):
        # print("----------> ast.Case")
        expr0 = self.visit(node.case0,scope,errors)
        # if expr0 == ERROR:
        #     return ERROR
        myscope = scope.CreateChildContext()
        supraType = self.visit(node.exprList[0],myscope,errors)
        if supraType==ERROR:
            node.computedType = ERROR
            return ERROR
        for i in range(1,len(node.exprList)):
            myscope = scope.CreateChildContext()
            x =  self.visit(node.exprList[i],myscope,errors)
            if x == ERROR:
                node.computedType = ERROR
                return ERROR
            supraType = scope.LCA(scope.hierarchy[supraType],scope.hierarchy[x])
        node.computedType = supraType
        return supraType

        
    @visitor.when(ast.CaseExpr) #!!!REVISAR CON STA GNT
    def visit(self, node, scope, errors):
        # print("----------> ast.CaseExpr")
        declType = self.visit(node.decl,scope,errors)
        exprType = self.visit(node.expr,scope,errors)
        node.computedType = exprType
        return exprType

    @visitor.when(ast.ClassDecl)
    def visit(self, node, scope, errors):
        # print("----------> ast.ClassDecl")
        pass
    
    @visitor.when(ast.ClassInh)
    def visit(self, node, scope, errors):
        # print("----------> ast.ClassInh")
        pass
    
    @visitor.when(ast.Method)
    def visit(self, node, scope, errors):
        # print("----------> ast.Method ",node.name)
        myscope = scope.CreateChildContext()
        visitparams = None
        for params in node.paramsList:
            visitparams = self.visit(params,myscope,errors)
            # if visit == ERROR:
            #     return ERROR
        visitbody = self.visit(node.exprbody,myscope,errors)

        # print("visitparams",visitparams)
        # print("visitbody",visitbody)
        if visitparams == ERROR or visitbody == ERROR:
            node.computedType = ERROR
            return ERROR 
        if visitbody == node.returnType or scope.IsDerived(visitbody,node.returnType):
            node.computedType = node.returnType
            return node.returnType
        errors.append("(0,0) -  TypeError :En la clase " + scope.currentClass + ": " +"La salida del m'etodo "+ node.name+ " debe ser de tipo " + node.returnType + " y esta siendo "+visitbody)
        node.computedType = ERROR
        return ERROR

    @visitor.when(ast.DispatchSelf)
    def visit(self, node, scope, errors):
        # print("----------> ast.DispatchSelf ",node.methodName)
        paramsType = []
        for params in node.paramsList:
            visit = self.visit(params,scope,errors)
            if visit == ERROR:
                errors.append("(0,0) -  SemanticError :En la clase " + scope.currentClass + ": " +"No pude computarse los par'ametros del m'etodo"+ node.methodName)
                node.computedType = ERROR
                return ERROR
            paramsType.append(visit)
        
        # typeNode = scope.hierarchy[scope.currentClass]
        methodType = scope.GetMethodReturnType(scope.currentClass,node.methodName,paramsType)
        if methodType == None:
            errors.append("(0,0) -  AtributeError :En la clase " + scope.currentClass + ": " +"El tipo " + scope.currentClass + " no contien un m'etodo "+ node.methodName +" con esa signatura")
            node.computedType = ERROR
            return ERROR
        # if methodType == "SELF_TYPE":
        #     return scope.currentClass
        node.computedType = methodType
        return methodType


    @visitor.when(ast.DispatchDot)
    def visit(self, node, scope, errors):
        # print("----------> ast.DispatchDot ",node.methodName)
        typeExpr0 = self.visit(node.expr0,scope,errors)
        if typeExpr0 == ERROR:
            errors.append("(0,0) -  SemanticError :En la clase " + scope.currentClass + ": " +"No pudo computarse el tipo de la expresion")
            node.computedType = ERROR
            return ERROR
        paramsType = []
        for params in node.paramsList:
            visit = self.visit(params,scope,errors)
            if visit == ERROR:
                errors.append("(0,0) -  SemanticError :En la clase " + scope.currentClass + ": " +"No pude computarse los par'ametros del metodo"+ node.methodName)
                node.computedType = ERROR
                return ERROR
            paramsType.append(visit)

        # typeNode = scope.hierarchy[typeExpr0]
        methodType = scope.GetMethodReturnType(typeExpr0,node.methodName,paramsType)
        # print("methodType",methodType)
        if methodType == None:
            errors.append("(0,0) -  AtributeError :En la clase " + scope.currentClass + ": " +"El tipo " +typeExpr0 + " no contien un m'etodo "+ node.methodName+" con esa signatura" )
            node.computedType = ERROR
            return ERROR
        # if methodType == "SELF_TYPE":
        #     return typeExpr0
        node.computedType = methodType
        return methodType
            
    
    @visitor.when(ast.StaticDispatch)
    def visit(self, node, scope, errors):
        # print("----------> ast.StaticDispatch ",node.methodName)
        dispObject = self.visit(node.dispObject,scope,errors)
        if dispObject == ERROR:
            node.computedType = ERROR
            return ERROR
        if dispObject == node.className or scope.IsDerived(dispObject,node.className):
            paramsType = []
            for params in node.paramsList:
                visit = self.visit(params,scope,errors)
                if visit == ERROR:
                    errors.append("(0,0) -  SemanticError :En la clase " + scope.currentClass + ": " +"No pude computarse los par'ametros del metodo"+ node.methodName)
                    node.computedType = ERROR
                    return ERROR
                paramsType.append(visit)
            # typeNode = scope.hierarchy[node.className]
            methodType = scope.GetMethodReturnType(node.className,node.methodName,paramsType)
            if methodType == None:
                errors.append("(0,0) -  AtributeError :En la clase " + scope.currentClass + ": " +"El tipo " +node.className + " no contien un m'etodo "+ node.methodName +" con esa signatura" )
                node.computedType = ERROR
                return ERROR
            # if methodType == "SELF_TYPE":
            #     return node.className
            node.computedType = methodType
            return methodType
        else:
            errors.append("(0,0) -  TypeError :En la clase " + scope.currentClass + ": " +"El tipo de la expresion en el dispatch debe ser compatible con " + node.className + " y esta siendo "+ dispObject)
            node.computedType = ERROR
            return ERROR
    
    @visitor.when(ast.Attr_Init)
    def visit(self, node, scope, errors):
        # print("----------> ast.Attr_Init ",node.attrName)
        exprType = self.visit(node.expr,scope, errors)

        var = scope.IsDefineVariable(node.attrName)
        if not var == None:
            errors.append("(0,0) -  SemanticError :La variable " + node.attrName + " ya está definida en el contexto actual")
            node.computedType = ERROR
            return ERROR
        if exprType == ERROR:
            node.computedType = ERROR
            return ERROR
        if (not (exprType ==  ERROR )) and (exprType == node.attrType or scope.IsDerived(exprType,node.attrType)):
            node.vinfo = scope.DefineVariable(node.attrName,node.attrType)
            node.computedType = node.attrType
            return node.attrType
        else:
            errors.append("(0,0) -  TypeError :En la variable " + node.attrName + " el tipo de la expresion debe ser compatible con " + node.attrType)
            node.computedType = ERROR
            return ERROR
    
    @visitor.when(ast.Attr_Declaration)
    def visit(self, node, scope, errors):
        # print("----------> ast.Attr_Declaration ",node.attrName)
        isDefineVar = scope.IsDefineVariable(node.attrName)
        if not isDefineVar == None :
            errors.append("(0,0) -  SemanticError :La variable "+ node.attrName+ " ya está definida en el contexto actual")
            node.computedType = ERROR
            return ERROR
        node.vinfo = scope.DefineVariable(node.attrName,node.attrType)
        node.computedType = node.attrType
        return node.attrType
    
    @visitor.when(ast.Ctes)
    def visit(self, node, scope, errors):
        # print("----------> ast.Ctes ",node.value)
        node.computedType = node.type
        return node.type
      
    @visitor.when(ast.Variable)
    def visit(self, node, scope, errors):
        # print("----------> ast.Variable ",node.name)
        if node.name == "self":
            node.computedType = scope.currentClass
            node.vinfo = scope.GetVinfo(node.name)
            return scope.currentClass
        varType = scope.IsDefineVariable(node.name)
        # print("=======varType",varType)
        if varType == None: # ver si es define o IsLocalVariable define
            errors.append("(0,0) -  NameError :En la clase " + scope.currentClass + ": " +"La variable " + node.name +" no est'a declarda en el scope actual")
            node.vinfo = scope.GetVinfo(node.name)
            node.computedType = ERROR
            return ERROR
        
        node.vinfo = scope.GetVinfo(node.name)
        node.computedType = varType
        return varType
   


