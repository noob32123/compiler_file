from Semanticer import *
from definition import *

class File_Process_Language_Syntaxerror(Exception):
    def __init__(self, message):
        super().__init__(message)

class Parser:
    def __init__(self,code_after_lex):
        self.code_after_lex=code_after_lex
        self.cur_pos=0
        self.RPE_generator=Reverse_Polish_Expression_Generator()

    def FORMAT_STR_parser(self):
        self.RPE_generator.process_operand(self.code_after_lex[self.cur_pos])     #没有经过处理的模板字符串

    def LOOP_SENTENCE_parser(self):
        if self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_WHILE"]:
            self.cur_pos+=1
            self.RPE_generator.process_operator(STARTJ_OPERATION_NUMBER)
            print(self.RPE_generator.stack)
            self.RPE_generator.finish_one_sentence()
            if self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_LPAREN"]:
                self.RPE_generator.process_operator(self.code_after_lex[self.cur_pos][1])
                self.cur_pos+=1
                self.EXPRESSION_SENTENCE_parser()
                if self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_RPAREN"]:
                    self.RPE_generator.process_operator(self.code_after_lex[self.cur_pos][1])
                    self.cur_pos+=1
                else:
                    raise File_Process_Language_Syntaxerror("<循环语句>语句缺少)")
                if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_LCURLYBRASE"]:
                    self.RPE_generator.process_operator(JFALSE_OPERATION_NUMBER)
                    self.RPE_generator.finish_one_sentence()
                    self.cur_pos+=1
                else:
                    raise File_Process_Language_Syntaxerror("<循环语句>语句缺少{")
                self.SUB_BODY_parser()
                if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_RCURLYBRASE"]:
                    self.RPE_generator.process_operator(J_OPERATION_NUMBER)
                    self.RPE_generator.process_operator(ENDJ_OPERATION_NUMBER)
                    self.RPE_generator.finish_one_sentence()
                    self.cur_pos+=1
                else:
                    raise File_Process_Language_Syntaxerror("<循环语句>语句缺少}")
            else:
                raise File_Process_Language_Syntaxerror("<循环语句>语句缺少(")
            print("<循环语句>=while(<表达式>){<子程序体>}")
        else:
            raise File_Process_Language_Syntaxerror("出现<循环语句>错误")

    def BRANCH_SENTENCE_parser(self):
        if self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_IF"]:
            self.cur_pos+=1
            if self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_LPAREN"]:
                self.RPE_generator.process_operator(self.code_after_lex[self.cur_pos][1])
                self.cur_pos+=1
                self.EXPRESSION_SENTENCE_parser()
                if self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_RPAREN"]:
                    self.RPE_generator.process_operator(self.code_after_lex[self.cur_pos][1])
                    self.cur_pos+=1
                else:
                    raise File_Process_Language_Syntaxerror("<分支语句>语句缺少)")
                if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_LCURLYBRASE"]:
                    self.RPE_generator.process_operator(JFALSE_OPERATION_NUMBER)
                    self.RPE_generator.finish_one_sentence()
                    self.cur_pos+=1
                else:
                    raise File_Process_Language_Syntaxerror("<分支语句>语句缺少{")
                self.SUB_BODY_parser()
                if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_RCURLYBRASE"]:
                    self.RPE_generator.process_operator(ENDJ_OPERATION_NUMBER)
                    self.RPE_generator.finish_one_sentence()
                    self.cur_pos+=1
                else:
                    raise File_Process_Language_Syntaxerror("<分支语句>语句缺少}")
            else:
                raise File_Process_Language_Syntaxerror("<分支语句>语句缺少(")
            print("<分支语句>=if(<表达式>){<子程序体>}")
        else:
            raise File_Process_Language_Syntaxerror("出现<分支语句>错误")

    def OTHER_COMMAND_parser(self):
        if self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_COMPUTE"]:
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            self.RPE_generator.process_operator(reserved_dict["RESERVED_COMPUTE"])
            print("<其它命令>::=compute<表达式>")
        elif self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_SPLIT"]:
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("指令之间的参数需要,分隔")
            self.EXPRESSION_SENTENCE_parser()
            self.RPE_generator.process_operator(reserved_dict["RESERVED_SPLIT"])
            print("<其它命令>::=split<表达式>,<表达式>")
        elif self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_AGGREGATE"]:
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("指令之间的参数需要,分隔")
            self.EXPRESSION_SENTENCE_parser()
            self.RPE_generator.process_operator(reserved_dict["RESERVED_AGGREGATE"])
            print("<其它命令>::=aggregate<表达式>,<表达式>")
        elif self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_PRINT"]:
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            self.RPE_generator.process_operator(reserved_dict["RESERVED_PRINT"])
            print("<其它命令>::=print<表达式>")
        else:
            raise File_Process_Language_Syntaxerror("出现<其他命令>错误")

    def FILEREADWRITE_COMMAND_parser(self):
        if self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_WRITE"]:
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("指令之间的参数需要,分隔")
            self.EXPRESSION_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("指令之间的参数需要,分隔")
            self.EXPRESSION_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("指令之间的参数需要,分隔")
            self.EXPRESSION_SENTENCE_parser()
            self.RPE_generator.process_operator(reserved_dict["RESERVED_WRITE"])
            print("<文件读写命令>::=write<表达式>,<表达式>,<表达式>,<表达式>")
        elif self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_READ"]:
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("指令之间的参数需要,分隔")
            self.EXPRESSION_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("指令之间的参数需要,分隔")
            self.EXPRESSION_SENTENCE_parser()
            self.RPE_generator.process_operator(reserved_dict["RESERVED_READ"])
            print("<文件读写命令>::=read<表达式>,<表达式>,<表达式>")
        elif self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_CHANGE"]:
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("指令之间的参数需要,分隔")
            self.EXPRESSION_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("指令之间的参数需要,分隔")
            self.EXPRESSION_SENTENCE_parser()
            self.RPE_generator.process_operator(reserved_dict["RESERVED_CHANGE"])
            print("<文件读写命令>::=change<表达式>,<表达式>,<表达式>")
        else:
            raise File_Process_Language_Syntaxerror("出现<文件读写指令>错误")

    def FILEMOVE_COMMAND_parser(self):
        if self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_MAKE"]:
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            self.RPE_generator.process_operator(reserved_dict["RESERVED_MAKE"])
            print("<文件移动命令>::=make<表达式>")
        elif self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_COPY"]:
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("指令之间的参数需要,分隔")
            self.EXPRESSION_SENTENCE_parser()
            self.RPE_generator.process_operator(reserved_dict["RESERVED_COPY"])
            print("<文件移动命令>::=copy<表达式>,<表达式>")
        elif self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_MOVE"]:
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("指令之间的参数需要,分隔")
            self.EXPRESSION_SENTENCE_parser()
            self.RPE_generator.process_operator(reserved_dict["RESERVED_MOVE"])
            print("<文件移动命令>::=move<表达式>,<表达式>")
        elif self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_DELETE"]:
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            self.RPE_generator.process_operator(reserved_dict["RESERVED_DELETE"])
            print("<文件移动命令>::=delete<表达式>")
        else:
            raise File_Process_Language_Syntaxerror("出现<文件移动指令>错误")

    def STR_parser(self):
        if self.code_after_lex[self.cur_pos][1]==constant_dict["CONSTANT_STR"]:
            self.RPE_generator.process_operand(self.code_after_lex[self.cur_pos])
            self.cur_pos+=1
            print("<字符串>::=<不变字符串>")
        elif self.code_after_lex[self.cur_pos][1]==constant_dict["FORMAT_STR"]:
            self.FORMAT_STR_parser()
            self.cur_pos+=1
            print("<字符串>::=<模板字符串>")
        else:
            raise File_Process_Language_Syntaxerror("出现<字符串>错误")

    def COMMAND_SENTENCE_parser(self):
        if self.code_after_lex[self.cur_pos][1] in FILEMOVE_COMMAND_LIST:
            self.FILEMOVE_COMMAND_parser()
            print("<命令语句>::=<文件移动命令>")
        elif self.code_after_lex[self.cur_pos][1] in FILEREADWRITE_COMMAND_LIST:
            self.FILEREADWRITE_COMMAND_parser()
            print("<命令语句>::=<文件读写命令>")
        elif self.code_after_lex[self.cur_pos][1] in OTHER_COMMAND_LIST:
            self.OTHER_COMMAND_parser()
            print("<命令语句>::=<其它命令>")
        else:
            raise File_Process_Language_Syntaxerror("出现<命令语句>错误")

    def ASSIGNMENT_SENTENCE_parser(self):
        if self.code_after_lex[self.cur_pos][1]==identifier_dict["IDENTIFIER"]:
            self.RPE_generator.process_operand(self.code_after_lex[self.cur_pos])
            self.cur_pos+=1
            self.SUB_ASSIGNABLE_OBJECT_parser()
            if self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_ASSIGNMENT"]:
                self.RPE_generator.process_operator(operator_dict["OPERATOR_ASSIGNMENT"])
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("赋值语句缺少=")
            self.EXPRESSION_SENTENCE_parser()
            print("<赋值语句>::=<变量名><子可赋值对象>=<表达式>")
        else:
            print("赋值语句出现错误")

    def SUB_EXPRESSION_parser(self):
        if self.code_after_lex[self.cur_pos][1] in OPERATOR_LIST:
            self.RPE_generator.process_operator(self.code_after_lex[self.cur_pos][1])
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            print("<子表达式>::=<运算符><表达式>")
        elif self.code_after_lex[self.cur_pos][1] in SUB_EXPRESSION_FOLLOW_LIST:
            print("<子表达式>::=空")
            return
        else:
            raise File_Process_Language_Syntaxerror("出现<子表达式>错误")

    def EXPRESSION_HEAD_parser(self):
        if self.code_after_lex[self.cur_pos][1] in CONSTANT_FIRST_LIST:
            self.CONSTANT_parser()
            print("<表达式头>::=<常量>")
        elif self.code_after_lex[self.cur_pos][1]==identifier_dict["IDENTIFIER"]:
            self.RPE_generator.process_operand(self.code_after_lex[self.cur_pos])
            self.cur_pos+=1
            self.SUB_ASSIGNABLE_OBJECT_parser()
            print("<表达式头>::=<变量名><子可赋值对象>")
        elif self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_LPAREN"]:
            self.RPE_generator.process_operator(self.code_after_lex[self.cur_pos][1])
            self.cur_pos+=1
            self.COMMAND_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_RPAREN"]:
                self.RPE_generator.process_operator(self.code_after_lex[self.cur_pos][1])
                self.cur_pos+=1
                print("<表达式头>::=(命令语句)")
                self.RPE_generator.set_command_return_true()
                return
            else:
                raise File_Process_Language_Syntaxerror("缺少)")
        else:
            raise File_Process_Language_Syntaxerror("出现<表达式头>错误")

    def EXPRESSION_SENTENCE_parser(self):
        self.EXPRESSION_HEAD_parser()
        self.SUB_EXPRESSION_parser()
        print("<表达式>::=<表达式头><子表达式>")

    def LIST_CONTAIN_parser(self):
        if self.code_after_lex[self.cur_pos][1] in CONSTANT_NUM_FIRST_LIST:
            self.CONSTANT_NUM_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("列表项之间缺少,")
            self.LIST_CONTAIN_parser()
            print("<列表内容>::=<常数>,<列表内容>")
        elif self.code_after_lex[self.cur_pos][1]==constant_dict["CONSTANT_STR"] or self.code_after_lex[self.cur_pos][1]==constant_dict["FORMAT_STR"]:
            self.STR_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_COMMA"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("列表项之间缺少,")
            self.LIST_CONTAIN_parser()
            print("<列表内容>::=<字符串>,<列表内容>")
        elif self.code_after_lex[self.cur_pos][1] in LIST_CONTAIN_FOLLOW_LIST:
            print("<列表内容>::=空")
            return
        else:
            raise File_Process_Language_Syntaxerror("出现<列表内容>错误")

    def SUB_LIST_parser(self):
        if self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_RBRACKET"]:
            self.cur_pos+=1
            self.RPE_generator.finish_list()
            print("<子列表常量>::=]")
        elif self.code_after_lex[self.cur_pos][1] in LIST_CONTAIN_FIRST_LIST:
            self.LIST_CONTAIN_parser()
            if self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_RBRACKET"]:
                self.cur_pos+=1
                self.RPE_generator.finish_list()
                print("<子列表常量>::=<列表内容>]")
            else:
                raise File_Process_Language_Syntaxerror("列表末尾缺少]")
        else:
            raise File_Process_Language_Syntaxerror("出现<子列表常量>错误")

    def CONSTANT_LIST_parser(self):
        if self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_LBRACKET"]:
            self.RPE_generator.begin_list()
            self.cur_pos+=1
            self.SUB_LIST_parser()
            print("<列表常量>::=[子列表常量")
        else:
            raise File_Process_Language_Syntaxerror("列表缺少[")

    def CONSTANT_NUM_parser(self):
        if self.code_after_lex[self.cur_pos][1]==constant_dict["CONSTANT_INT"]:
            self.RPE_generator.process_operand(self.code_after_lex[self.cur_pos])
            self.cur_pos+=1
            print("<常数>::=<自然数>")
        elif self.code_after_lex[self.cur_pos][1]==constant_dict["CONSTANT_FLOAT"]:
            self.RPE_generator.process_operand(self.code_after_lex[self.cur_pos])
            self.cur_pos+=1
            print("<常数>::=<正浮点数>")
        elif self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_MINUS"]:
            self.cur_pos+=1
            self.CONSTANT_NUM_parser()
            self.RPE_generator.process_operand(MINUS_OPERATION_NUMBER)
            print("<常数>::=-<常数>")
        else:
            raise File_Process_Language_Syntaxerror("出现<常数>错误")

    def CONSTANT_parser(self):
        if self.code_after_lex[self.cur_pos][1] in CONSTANT_NUM_FIRST_LIST:
            self.CONSTANT_NUM_parser()
            print("<常量>::=<常数>")
        elif self.code_after_lex[self.cur_pos][1]==constant_dict["CONSTANT_STR"] or self.code_after_lex[self.cur_pos][1]==constant_dict["FORMAT_STR"]:
            self.STR_parser()
            print("<常量>::=<字符串>")
        elif self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_LBRACKET"]:
            self.CONSTANT_LIST_parser()
            print("<常量>::=<列表常量>")
        else:
            print("出现<常量>错误")

    def SUB_ASSIGNABLE_OBJECT_parser(self):
        if self.code_after_lex[self.cur_pos][1] in SUB_ASSIGNABLE_OBJECT_FIRST_LIST:
            self.cur_pos+=1
            if self.code_after_lex[self.cur_pos][1]==constant_dict["CONSTANT_INT"]:
                self.RPE_generator.process_operand(self.code_after_lex[self.cur_pos])
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("缺少大于0的整数索引")
            if self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_RBRACKET"]:
                self.RPE_generator.process_operator(INDEX_OPERATION_NUMBER)
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("缺少]")
            print("<子可赋值对象>::=[自然数]")
        elif self.code_after_lex[self.cur_pos][1] in SUB_ASSIGNABLE_OBJECT_FOLLOW_LIST:
            print("<子可赋值对象>::=空")
            return
        else:
            raise File_Process_Language_Syntaxerror("出现<子可赋值对象>错误")

    def SUB_DECLARE_SENTENCE_parser(self):
        if self.code_after_lex[self.cur_pos][1]==operator_dict["OPERATOR_ASSIGNMENT"]:
            self.RPE_generator.code.append(self.RPE_generator.last_process_variable)
            self.RPE_generator.process_operator(self.code_after_lex[self.cur_pos][1])
            self.cur_pos+=1
            self.EXPRESSION_SENTENCE_parser()
            print("<子声明语句>::==<表达式>")
        elif self.code_after_lex[self.cur_pos][1] in SUB_DECLARE_SENTENCE_FOLLOW_LIST:
            print("<子声明语句>::=空")
            return
        else:
            raise File_Process_Language_Syntaxerror("出现<子声明语句>错误")

    def DECLARE_SENTENCE_parser(self):
        if self.code_after_lex[self.cur_pos][1] in DECLARE_SENTENCE_FIRST_LIST:
            self.RPE_generator.process_operator(self.code_after_lex[self.cur_pos][1])
            self.cur_pos+=1  #数据类型
            if self.code_after_lex[self.cur_pos][1]==identifier_dict["IDENTIFIER"]:
                self.RPE_generator.process_operand(self.code_after_lex[self.cur_pos])
                self.cur_pos+=1
            else:
                raise DECLARE_SENTENCE_FIRST_LIST("<声明语句>缺少<变量名>")
            self.RPE_generator.finish_one_sentence()
            self.SUB_DECLARE_SENTENCE_parser()
        else:
            raise File_Process_Language_Syntaxerror("出现<声明语句>错误")
        print("<声明语句>::=<数据类型><变量名><子声明语句>")

    def NORMAL_SENTENCE_parser(self):
        if self.code_after_lex[self.cur_pos][1] in DECLARE_SENTENCE_FIRST_LIST:
            self.DECLARE_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_SEMICOLON"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("声明语句后缺少分号")
            print("<普通语句>::=<声明语句>;")
        elif self.code_after_lex[self.cur_pos][1] in COMMAND_SENTENCE_FIRST_LIST:
            self.COMMAND_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_SEMICOLON"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("命令语句后缺少分号")
            print("<普通语句>::=<命令语句>;")
        elif self.code_after_lex[self.cur_pos][1] in ASSIGNMENT_SENTENCE_FIRST_LIST:
            self.ASSIGNMENT_SENTENCE_parser()
            if self.code_after_lex[self.cur_pos][1]==border_dict["BORDER_SEMICOLON"]:
                self.cur_pos+=1
            else:
                raise File_Process_Language_Syntaxerror("赋值语句后缺少分号")
            print("<普通语句>::=<赋值语句>;")
        else:
            raise File_Process_Language_Syntaxerror("出现<语句>错误")

    def SENTENCE_parser(self):
        if self.code_after_lex[self.cur_pos][1] in NORMAL_SENTENCE_FIRST_LIST:
            self.NORMAL_SENTENCE_parser()
            print("<语句>::=<普通语句>")
            self.RPE_generator.finish_one_sentence()
        elif self.code_after_lex[self.cur_pos][1] in BRANCH_SENTENCE_FIRST_LIST:
            self.BRANCH_SENTENCE_parser()
            print("<语句>::=<循环语句>")
        elif self.code_after_lex[self.cur_pos][1] in LOOP_SENTENCE_FIRST_LIST:
            self.LOOP_SENTENCE_parser()
            print("<语句>::=<分支语句>")
        else:
            raise File_Process_Language_Syntaxerror("出现<语句>错误")

    def SUB_BODY_parser(self):    #这里是子程序体
        if self.code_after_lex[self.cur_pos][1] in SUB_BODY_FIRST_LIST:
            self.BODY_parser()
            print("<子程序体>::=<程序体>")
        elif self.code_after_lex[self.cur_pos][1] in SUB_BODY_FOLLOW_LIST:
            print("<子程序体>::=空")
            return
        else:
            raise File_Process_Language_Syntaxerror("出现<子程序体>错误")

    def BODY_parser(self):
        if self.code_after_lex[self.cur_pos][1] in SENTENCE_FIRST_LIST:
            self.SENTENCE_parser()
            self.SUB_BODY_parser()
            print("<程序体>::=<语句><子程序体>")
        else:
            raise File_Process_Language_Syntaxerror("出现<程序体>错误")

    def SUBPROGRAM_parser(self):
        if self.code_after_lex[self.cur_pos][1] in BODY_FIRST_LIST:
            self.BODY_parser()
            if self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_@END"]:
                self.cur_pos+=1
                print("<子程序>::=<程序体>@end")
                return
            else:
                raise File_Process_Language_Syntaxerror("程序尾没有@end")

        elif self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_@END"]:
            self.cur_pos+=1
            print("<子程序>::=@end")
            return #完成分析
        else:
            raise File_Process_Language_Syntaxerror("缺少程序体或@end")

    def PROGRAM_parser(self):
        if self.code_after_lex[self.cur_pos][1]==reserved_dict["RESERVED_@START"]:
            self.cur_pos+=1
            self.SUBPROGRAM_parser()
            print("<程序>::=@start<子程序>")
        else:
            raise File_Process_Language_Syntaxerror("程序开始缺少@start")

    def parse(self):
        self.PROGRAM_parser()
