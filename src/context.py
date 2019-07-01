
class TypeNode:
    def __init__(self,className,parent="Object"):
        self.name = className
        self.attrlist = [Attribute("self",className)]
        self.methodlist = {}
        self.default = "void"
        self.parent = parent
        self.children = []

    # def GetAttribute(self,attrName):
    #     attr = [attr.Name == attrName for attr in self.attrlist]
    #     return attr[0]

    # def GetMethod(self,methodName):
    #     meth = [meth.Name == methodName for meth in self.attrlist]
    #     return meth[0]
    
    def DefineAttribute(self, attrName, attrType):
        if not (self._IsDefineAttribute(attrName) == None):
            return False
        self.attrlist.append(Attribute(attrName,attrType))
        # print("------selflist ", self.attrlist)
        return True

    def DefineMethod(self, methodName,argName,argType,returnType,rename):
        if not (self._IsLocalDefineMethod(methodName) == None) or self._IsDefineADiferentMethodWhitSameName(methodName,argName,argType,returnType):
            return False
        # self.methodlist.append(Method(methodName,argName,argType,returnType,rename))
        self.methodlist[methodName] = Method(methodName,argName,argType,returnType,rename)
        return True

    def GetMethodReturnType(self,methodName):
        self.methodlist.values()
        for element in self.methodlist.values():
            # print("//////element.paramsType paramsType",element.paramsType , paramsType)
            if element.name == methodName:
                # for i,param in enumerate(paramsType):
                #     element.paramsType[i] derived paramstype
                # print("element.returnType",element.returnType)
                return element
        if self.parent == None:
            return None
        return self.parent.GetMethodReturnType(methodName)

    def _IsDefineMethod(self, methodName,argName,argType,returnType):
        for element in self.methodlist.values():
            if element.name == methodName and ((element.returnType == returnType) and (element.paramsType == argType) ):
                return True
        if self.parent == None:
            return False
        return self.parent._IsDefineMethod(methodName,argName,argType,returnType)


    def _IsDefineAttribute(self, attrName):
        attr = [ attr.Type for attr in self.attrlist if attr.Name == attrName]
        if len(attr):
            return attr[0]
        if self.parent == None:
            return None
        return self.parent._IsDefineAttribute(attrName)

    def _IsDefineAttributeInParent(self, attrName):
        parent = self.parent
        if parent == None:
            return None
        return parent._IsDefineAttribute(attrName)

    def _IsLocalDefineMethod(self, methodName):
        meth = self.methodlist.get(methodName)
        #  [ meth for meth in self.methodlist if meth.name == methodName]
        return meth
        # if len(meth):
        #     return meth[0]
        # return None

    def _IsDefineADiferentMethodWhitSameName(self, methodName,argName,argType,returnType):
        for element in self.methodlist.values():
            if element.name == methodName and (not (element.returnType == returnType) or not(element.paramsType == argType) ):
                return True
        if self.parent == None:
            return False
        return self.parent._IsDefineADiferentMethodWhitSameName(methodName,argName,argType,returnType)

    
    def IsDerived(self, ancestor):
        derivedparent = self.parent
        if derivedparent == None:
            return False
        if derivedparent.Name == ancestor:
            return True
        return derivedparent.IsDerived(ancestor)

    # def GetTypeNode(self,typeName):
    #     if self.name == typeName:
    #         return self
    #     for child in self.children:
    #         cd = child.GetTypeNode(typeName)
    #         if not (cd == None):
    #             return cd
    #     return child
        
     
class Attribute:
    def __init__(self, attrName,attrType):
        self.Name = attrName
        self.Type = attrType

        
class Method:
    def __init__(self, name,paramsName, paramsType,returnType,rename):
        self.name = name
        self.returnType = returnType
        self.paramsType = paramsType
        self.paramsName = paramsName
        self.rename = rename
        # self.mmholder = mmholder

class Context:
    def __init__(self, parent = None):
        if parent == None:
            self.buildin = self.__GetBuildIn()
        # self.hierarchy = {"Object":TypeNode("Object",None)}
        # self.hierarchyNode = TypeNode("Object",None)

        self.variables = {} #nombre de la variable, su tipo
        self.parent = parent
        self.children = []
        self.currentClass = None
        self.order_classes = []
        # self.index_at_parent = 0 if parent is None else len(parent.locals)

    def __GetBuildIn(self):
        self.hierarchy = {}
        typeObject =  TypeNode("Object",parent = None)
        self.hierarchy["Object"] = typeObject

        typeString =  TypeNode("String","Object")
        # typeObject =  TypeNode("Object",self.hierarchy["Object"])
        typeBool =  TypeNode("Bool","Object")
        typeInt =  TypeNode("Int","Object")
        typeIO =  TypeNode("IO","Object")

        typeObject.methodlist["abort"] = (Method("abort",[],[],"Object",None))
        typeObject.methodlist["type_name"] =(Method("type_name",[],[],"String",None))
        
        typeIO.methodlist["in_string"] =(Method("in_string",[],[],"String",None))
        typeIO.methodlist["in_int"] =(Method("in_int",[],[],"Int",None))
        typeIO.methodlist["out_string"] = (Method("out_string", ["x"], ["String"], "IO", None))
        typeIO.methodlist["out_int"] = (Method("out_int", ["x"], ["Int"], "IO", None))

        typeString.methodlist["length"] =(Method("length",[],[],"Int",None))
        typeString.methodlist["concat"] =(Method("concat",["s"],["String"],"String",None))
        typeString.methodlist["substr"] =(Method("substr",["i","l"],["Int","Int"],"String",None))
        
        typeInt.default = 0
        typeBool.default = "false"
        typeString.default = ""

        
        self.hierarchy["String"] = typeString
        self.hierarchy["Bool"] = typeBool
        self.hierarchy["Int"] = typeInt
        self.hierarchy["IO"] = typeIO
        

        return [typeString,typeBool,typeInt]



########
    def GetMethodReturnType(self,ctype,methodName,paramsType):
        myctype = self.hierarchy[ctype]
        meth = myctype.GetMethodReturnType(methodName)
        if meth == None:
            return None
        if not (len(paramsType)== len(meth.paramsType)):
            return None 
        for i,param in enumerate(paramsType):
            if not (meth.paramsType[i] == param) and (not self.IsDerived(param,meth.paramsType[i])):
                return None
        return meth.returnType


    def GetType(self,typeName): # devuelve el objeto
        # print ("self1",self.hierarchyNode.GetTypeNode(typeName))
        return self.hierarchy.get(typeName)


    def IsDefineType(self,typeName):
        return self.hierarchy.__contains__(typeName)
        
    def CreateType(self,typeName,typeParent):
        if not self.GetType(typeName) == None:
            return False
        newType = TypeNode(typeName,typeParent)
        # parent.children.append(newType)
        self.hierarchy[typeName] = newType 
        return True

    def LinkTypes(self,errors):
        values = list(self.hierarchy.values())
        # for item in values:
        #     print(item.name)
        # print("values1",values1)
        # a = self.hierarchy["String"]
        # print("a",a.name)
        # values = values1.remove(a)
        # print("values",values)
        for item in values:
            # print("item.name",item.name)
            # print("item.parent",item.parent)
            if not (item.parent == None):
                # print("item.parent1",item.parent)
                parent = self.GetType(item.parent)
                # print("here",parent)
                if parent == None:
                    errors.append("(0,0) - TypeError: El tipo "+ item.parent + " no esta definido")
                    return False
                item.parent = parent
                parent.children.append(item)

        return self.IsValid(errors)
        # return True

 

    def IsDerived(self, derived, ancestor):
        # print("derived,ancestor",derived,ancestor)
        derivedType = self.GetType(derived)
        return self._IsDerived(derivedType,ancestor)

    def _IsDerived(self, derived, ancestor):
        # print("derived,ancestor1",derived.name,ancestor)
        derivedparent = derived.parent
        if derivedparent == None:
            return False
        if derivedparent.name == ancestor:
            return True
        return self._IsDerived(derivedparent,ancestor)

    def IsValid(self,errors): #revisar q no haya ciclos
        for item in self.buildin:
            if len(item.children):
                errors.append("(0,0) - SemanticError: No se puede heredar del metodo "+ item.name)
                # print("buildin con hijos "  + item.name)
                return False
        return self.NotExistCicle(errors)

    def NotExistCicle(self,errors):
        # self.order_classes = []
        self._NotExistCicle( self.hierarchy["Object"],self.order_classes)
        # print("No Hay ciclo", len(self.order_classes) == len(self.hierarchy))
        # print(self.order_classes)
        if len(self.order_classes) == len(self.hierarchy):
            self.sorted = self.order_classes
            return True
        errors.append("(0,0) - SemanticError: No pueden existir ciclos en la herencia")
        return False
        # return len(self.order_classes) == len(self.hierarchy)


    def _NotExistCicle(self, a: TypeNode, types: list):
        # print("aciclicos",a.name)
        if a is None:
            return True
        if types.__contains__(a.name):
            return False
        types.append(a.name)

        for child in a.children:
            if not self._NotExistCicle(child, types):
                return False
        return True


    def NotIOReimplemetation(self):
        # print("------------")
        
        # print("HOLA")
        io = self.hierarchy["IO"]
        succ = io.children 
        # print("----cosita",io.children)
        # print("----cosita2",io.children[0].methodlist)
        # print("succ ", succ)
        while len(succ):
            item = succ.pop()
            # print("metodos", item.methodlist.values())
            for m in item.methodlist.values():
                if m.name == "in_string" or m.name == "in_int" or m.name == "out_string" or m.name == "out_int":
                    return False
            succ = succ + item.children

        # print("------------")
        return True

    def LCA(self,a: TypeNode, b: TypeNode):
        # Si son iguales
        if a.name == b.name:
            return a.name
        
        # Lista de los posibles ancestros
        ancestors = []
    
        # Voy subiendo hasta llegar a la raíz y guardando los nodos.name que son los ancestros de a
        while a is not None:
            ancestors.append(a.name)
            a = a.parent
    
        # Trato de encontrar un ancestro de b que sea ancestro de a, el cual será el LCA
        # b = b.parent
        while b is not None:
            if ancestors.__contains__(b.name):
                return b.name
            b = b.parent
    
        return None

#######

    def DefineVariable(self, vname, vtype):
        var = VariableInfo(vname,vtype)
        self.variables[vname] =  var
        return var 
        
    # def IsDefineVariable(self,vname):
    #     print("is def var")
    #     if self.variables.__contains__(vname):
    #         print("contain")
    #         return True, self.variables[vname]
    #     if not (self.parent == None):
    #         print("parent")
    #         return self.parent.IsDefineVariable(vname)
    #     return False,None

        
    def _GetType(self, vname):
        var =  self.variables.get(vname) 
        if var == None:
            return None
        return var.ctype

    def GetVinfo(self,vname):
        # print("is def var")
        var =  self.variables.get(vname) 
        if not (var == None):
            # print("contain",vname)
            return var
        if self.parent == None:
            return None
        # print("parent")
        return self.parent.GetVinfo(vname)


    def IsDefineVariable(self,vname):
        vinfo = self.GetVinfo(vname)
        if vinfo == None:
            vtype = self.hierarchy[self.currentClass]._IsDefineAttributeInParent(vname)
            if vtype == None:
                return None
            return vtype
        return vinfo.ctype        

    # def GetVariableType(self,variable):
    #     return self.variables[variable]

    # def IsLocalVariable(self,vname):
    #     if self.variables.__contains__(vname):
    #         return True, self.variables[vname]
    #     return False,None

    def CreateChildContext(self):
        childContext = Context(self)
        childContext.hierarchy = self.hierarchy
        childContext.currentClass = self.currentClass
        return childContext


class VariableInfo:
    def __init__(self, name, ctype = None, vmholder = 0):
        self.name = name
        self.ctype = ctype
        self.vmholder = vmholder

    def __str__(self):
        return " name: " + str(self.name) + ", tipo: "+ str(self.ctype)  + ", vmholder: " + str(self.vmholder)

class MethodInfo:
    def __init__(self, name, vmholder = 0, paramsType = [], returnType = None):
        self.name = name
        self.vmholder = vmholder
        self.paramsType = paramsType
        self.returnType = returnType

    def __str__(self):
        return " name: " + str(self.name)  + ", vmholder: " + str(self.vmholder)


class ClassInfo:
    def __init__(self, name, attr_length = 0, meth_length = 0, parent = None):
        self.name = name
        self.attr_length = attr_length
        self.meth_length = meth_length
        self.parent = parent

    def __str__(self):
        return " name: " + str(self.name)  + " parent: " + str(self.parent.cinfo.name) + ", attr_length: " + str(self.attr_length) + ", meth_length: " + str(self.meth_length)
