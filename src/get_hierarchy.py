import visitor
import cool_ast_hierarchy as ast
import context 
from context import Context as Hierarchy



class VisitorTypeCollector:
    def __init__(self):
        self.count = 0

    @visitor.on('node')
    def visit(self, node, scope, errors):
        # self.count = 0
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node, scope, errors):
        # Primer visitor
        for classitem in node.classList:
            if not scope.CreateType(classitem.name,classitem.parent):
                errors.append("(0,0) - SemanticErrors: La clase "+ classitem.name+ " ya esta definida")   
        if not scope.LinkTypes(errors):
             pass
            #  errors.append("(0,0) - SemanticErrors: Error con los tipos")
        # posibles errores: que no exista el padre d alguien
        # que se derive de los tipos buildIn
        # que haya ciclo
        # que se sobrescriba alguien de IO

        if len(errors):
            return False    
        
        node.classList.sort(key=lambda x: scope.order_classes.index(x.name))
        # Segundo visitor
        # if scope.IsValid():
        for classitem in node.classList:
            self.visit(classitem,scope,errors)
        
        mainexist = scope.GetType("Main")
        if mainexist == None:
            errors.append("(0,0)  -  SemanticErrors: Debe existir una clase llamada Main")
        else:
            # print("||||| mainexist", mainexist.name)
            # a = [item.name for item in mainexist.methodlist]
            # print("||||| mainexist methods",mainexist.methodlist )
            meth = mainexist._IsLocalDefineMethod("main")
            if meth == None:
                errors.append("(0,0)  -  SemanticErrors: La clase Main debe tener un m'etodo main")
            elif not meth.paramsType == []:
                errors.append("(0,0)  -  SemanticErrors: La clase Main debe tener un m'etodo main que no reciba argumentos")
            
        if not scope.NotIOReimplemetation():
            errors.append("(0,0) - SemanticErrors: Herederos de IO sobreescriben")
        
        if len(errors):
            return False    
        return True
        # return False

    @visitor.when(ast.CoolClass)
    def visit(self, node, scope, errors):
        coolType = scope.GetType(node.name)
        # print("coolType",coolType.name)   
 
        for attr in node.attrs:
            if attr.attrName == "self":
                errors.append("(0,0) - SemanticErrors: Los atributos no pueden llamarse self")
            else: 
                if scope.IsDefineType(attr.attrType):
                    # print("attr",attr.attrName)
                    if not coolType.DefineAttribute(attr.attrName, attr.attrType):
                        errors.append("(0,0) - SemanticErrors: el atrributo " + attr.attrName +" ya estaba definido")

                else:
                    errors.append("(0,0)  -  TypeErrors: El tipo del attributo " + attr.attrName + " no est'a definido")
                    # return False        
        
        # print("coolattr",coolType.attrlist)  
       
        for func in node.methods:
            # print("func",func.name)
            if scope.IsDefineType(func.returnType):
                argsName = []
                argsType = []
                for param in func.paramsList:
                    if  scope.IsDefineType(param.attrType): 
                        if argsName.__contains__(param.attrName):
                            errors.append("(0,0) - SemanticErrors: El par'ametro "+param.attrName+" ya esta definido en el metodo "+ func.name)
                        else:
                            argsName.append(param.attrName)
                            argsType.append(param.attrType)
                    else:
                        errors.append("(0,0) - TypeErrors: El tipo del par'ametro "+param.attrName+" no esta definido")
                        # return False     
                # return coolType.DefineMethod(func.name,argsName,argsType,func.returnType)
                if not coolType.DefineMethod(func.name,argsName,argsType,func.returnType,"func_"+func.name+"_"+str(self.count)):
                    errors.append("(0,0) - SemanticErrors: No se puede sobrescribir el m'etodo "+ func.name)
                else:
                    self.count+=1
            else:
                errors.append("(0,0) - TypeErrors: El tipo de retorno de le funcion "+ func.name+ " no est'a definido")
                # return False
        # print("coolmeth",coolType.methodlist)
        
        
        
   

 