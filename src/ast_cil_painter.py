import cil_hierarchy as cil
import visitor

# a = {1: 2}
# for x in a.values():
#     print(x)

# class B():
#     def __str__(self):
#         return "B"
#
# print('class ' + str(B()))


class PrintVisitorCIL(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(cil.CILProgramNode)
    def visit(self, node: cil.CILProgramNode, tabs):
        ans = 'CILProgramNode'

        ans += '\n---DOTTYPES---\n'

        if node.dottypes:
            for types in node.dottypes.values():
                ans += '\n' + self.visit(types, tabs + 1)

        ans += '\n---DOTDATA---\n'

        if node.dotdata:
            for data in node.dotdata.values():
                ans += '\n' + self.visit(data, tabs + 1)

        ans += '\n---DOTCODE---\n'

        if node.dotcode:
            for code in node.dotcode:
                ans += '\n' + self.visit(code, tabs + 1)

        return ans

    @visitor.when(cil.CILTypeNode)
    def visit(self, node: cil.CILTypeNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILTypeNode ' + str(node.cinfo.name)
        if node.attrs:
            for vinfo in node.attrs.values():
                ans += '\n' + ' \t' * (tabs + 1) + '|___' + 'attr_name: ' + str(vinfo)
        if node.methods:
            for CILFunctionNode in node.methods:
                ans += '\n' + ' \t' * (tabs + 1) + '|___' + 'fname: ' + CILFunctionNode + ': ' + str(node.methods[CILFunctionNode].finfo)
        return ans

    @visitor.when(cil.CILDataNode)
    def visit(self, node: cil.CILDataNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILDataNode ' + 'name: ' + str(node.vname) + ' value: ' + str(node.value)
        return ans

    @visitor.when(cil.CILFunctionNode)
    def visit(self, node: cil.CILFunctionNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILFunctionNode ' + 'name: ' + str(node.finfo.name)
        if node.arguments:
            for CILArgNode in node.arguments:
                ans += '\n' + self.visit(CILArgNode, tabs + 1)
        if node.localvars:
            for CILLocalNode in node.localvars:
                ans += '\n' + self.visit(CILLocalNode, tabs + 1)
        if node.instructions:
            for CILInstructionNode in node.instructions:
                ans += '\n' + self.visit(CILInstructionNode, tabs + 1)
        return ans

    @visitor.when(cil.CILParamNode)
    def visit(self, node: cil.CILParamNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILParamNode ' + str(node.vinfo)
        return ans

    @visitor.when(cil.CILLocalNode)
    def visit(self, node: cil.CILLocalNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILLocalNode ' + str(node.vinfo)
        return ans

    @visitor.when(cil.CILAssignNode)
    def visit(self, node: cil.CILAssignNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILAssignNode ' + 'dest ' + str(node.dest) + ' source ' + str(node.source)
        return ans

    @visitor.when(cil.CILPlusNode)
    def visit(self, node: cil.CILPlusNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILPlusNode ' + 'dest ' + str(node.dest) + ' left ' + str(node.left) +\
              'right ' + str(node.right)
        return ans

    @visitor.when(cil.CILMinusNode)
    def visit(self, node: cil.CILMinusNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILMinusNode ' + 'dest ' + str(node.dest) + ' left ' + str(node.left) +\
              'right ' + str(node.right)
        return ans

    @visitor.when(cil.CILStarNode)
    def visit(self, node: cil.CILStarNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILStarNode ' + 'dest ' + str(node.dest) + ' left ' + str(node.left) +\
              ' right ' + str(node.right)
        return ans

    @visitor.when(cil.CILDivNode)
    def visit(self, node: cil.CILDivNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILDivNode ' + 'dest ' + str(node.dest) + ' left ' + str(node.left) +\
              ' right ' + str(node.right)
        return ans

    @visitor.when(cil.CILGetAttribNode)
    def visit(self, node: cil.CILGetAttribNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILGetAttribNode ' + 'dest ' + str(node.dest) + ' attr ' + str(node.nattr) +\
              ' source ' + str(node.source)
        return ans

    @visitor.when(cil.CILSetAttribNode)
    def visit(self, node: cil.CILSetAttribNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILSetAttribNode ' + 'dest ' + str(node.dest) + ' attr ' + str(node.nattr) +\
              ' source ' + str(node.source)
        return ans

    @visitor.when(cil.CILGetIndexNode)
    def visit(self, node: cil.CILGetIndexNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILGetIndexNode ' + 'dest ' + str(node.dest) + ' array ' + str(node.array) +\
              ' index ' + str(node.index)
        return ans

    @visitor.when(cil.CILSetIndexNode)
    def visit(self, node: cil.CILSetIndexNode, tabs):
        pass

    @visitor.when(cil.CILAllocateNode)
    def visit(self, node: cil.CILAllocateNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILAllocateNode ' + 'dest: ' + str(node.dest) + ' type: ' + str(node.cinfo.name)
        return ans

    @visitor.when(cil.CILArrayNode)
    def visit(self, node: cil.CILArrayNode, tabs):
        pass

    @visitor.when(cil.CILTypeOfNode)
    def visit(self, node: cil.CILTypeOfNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILTypeOfNode' + ' dest: ' + str(node.dest) + ' var: ' + str(node.var)
        return ans

    @visitor.when(cil.CILLabelNode)
    def visit(self, node: cil.CILLabelNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILLabelNode' + ' name: ' + str(node.name)
        return ans

    @visitor.when(cil.CILGotoNode)
    def visit(self, node: cil.CILGotoNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILGotoNode\n' + self.visit(node.label, tabs+1)
        return ans

    @visitor.when(cil.CILGotoIfNode)
    def visit(self, node: cil.CILGotoIfNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILGotoIfNode\n' + self.visit(node.label, tabs+1) + ' vinfo: ' + str(node.vinfo)
        return ans

    @visitor.when(cil.CILStaticCallNode)
    def visit(self, node: cil.CILStaticCallNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILStaticCallNode' + ' meth: ' + str(node.meth_name) + ' dest: ' + str(node.dest)
        return ans

    @visitor.when(cil.CILDynamicCallNode)
    def visit(self, node: cil.CILDynamicCallNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILDynamicCallNode ' + 'meth: ' + str(node.meth_name) + ' dest: ' + str(node.dest) +\
              str(node.ctype)
        return ans

    @visitor.when(cil.CILArgNode)
    def visit(self, node: cil.CILArgNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILArgNode ' + str(node.vinfo)
        return ans

    @visitor.when(cil.CILReturnNode)
    def visit(self, node: cil.CILReturnNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILReturnNode ' + str(node.value)
        return ans

    @visitor.when(cil.CILLoadNode)
    def visit(self, node: cil.CILLoadNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILLoadNode ' + 'dest: ' + str(node.dest) + ' msg: \n' + self.visit(node.msg, tabs + 1)
        return ans

    @visitor.when(cil.CILLengthNode)
    def visit(self, node: cil.CILLengthNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILLengthNode ' + 'dest: ' + str(node.dest) + ' string: ' + str(node.array)
        return ans

    @visitor.when(cil.CILConcatNode)
    def visit(self, node: cil.CILConcatNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILConcatNode ' + 'dest: ' + str(node.dest) + ' string1: ' + str(
            node.array1) + ' string2 ' + str(node.array2)
        return ans

    @visitor.when(cil.CILPrefixNode)
    def visit(self, node: cil.CILPrefixNode, tabs):
        pass

    @visitor.when(cil.CILSubstringNode)
    def visit(self, node: cil.CILSubstringNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILSubstringNode ' + 'dest: ' + str(node.dest) + ' string: ' + str(
            node.array) + ' i ' + str(node.i) + ' j ' + str(node.l)
        return ans

    @visitor.when(cil.CILPrintIntNode)
    def visit(self, node: cil.CILPrintIntNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILPrintIntNode ' + 'vinfo: ' + str(node.vinfo)
        return ans

    @visitor.when(cil.CILPrintStrNode)
    def visit(self, node: cil.CILPrintStrNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILPrintStrNode ' + 'vinfo: ' + str(node.vinfo)
        return ans

    @visitor.when(cil.CILReadIntNode)
    def visit(self, node: cil.CILReadIntNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILReadIntNode ' + 'vinfo: ' + str(node.vinfo)
        return ans

    @visitor.when(cil.CILReadStrNode)
    def visit(self, node: cil.CILReadStrNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILReadStrNode ' + 'vinfo: ' + str(node.vinfo)
        return ans

    @visitor.when(cil.CILParentNode)
    def visit(self, node: cil.CILParentNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILParentNode' + 'dest: ' + str(node.dest) + 'ntype: ' + str(node.ntype)
        return ans

    @visitor.when(cil.CILErrorNode)
    def visit(self, node: cil.CILErrorNode, tabs):
        ans = '\t' * tabs + '|___' + 'CILErrorNode ' + 'error: ' + str(node.num)
        return ans

    @visitor.when(cil.CILSaveState)
    def visit(self, node: cil.CILSaveState, tabs):
        ans = '\t' * tabs + '|___' + 'CILSaveState '
        return ans

    @visitor.when(cil.CILLessThan)
    def visit(self, node: cil.CILLessThan, tabs):
        ans = '\t' * tabs + '|___' + 'CILLessThan ' + 'dest: ' + str(node.dest) + ' left: ' + str(node.left) + ' right: ' + str(node.right)
        return ans

    @visitor.when(cil.CILTypeName)
    def visit(self, node: cil.CILTypeName, tabs):
        ans = '\t' * tabs + '|___' + 'CILTypeName ' + 'dest: ' + str(node.dest) + ' class: ' + str(node.nclass)
        return ans

    @visitor.when(cil.CILReturnFinal)
    def visit(self, node: cil.CILSaveState, tabs):
        ans = '\t' * tabs + '|___' + 'CILReturnFinal '
        return ans
