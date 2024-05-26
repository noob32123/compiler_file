import definition
import re
from definition import *

class File_Process_Language_Worderror(Exception):
    def __init__(self, message):
        super().__init__(message)

class FileProcessor:
    def __init__(self,path):
        self.path=path
        self.code=self.read_file()

    def read_file(self):
        with open(self.path, 'r') as f:
            code = f.read()
            return code

    def get_processed_file(self):    #不进行预处理
        return self.code

class Lexical_Analysor:
    def __init__(self,code):
        self.code=code
        self.mode="INITIAL"
        self.cur_pos=0
        self.inline_pos=0
        self.line=0
        self.temp_word=""
        self.length=len(self.code)
        #存储格式：
        self.already_processed_words=[]

    #这里还漏了一个cur_pos++
    def INITIAL_status_processor(self):
        try:
            while self.code[self.cur_pos] in skip_list:
                if self.code[self.cur_pos]=="\n":
                    self.line+=1
                    self.inline_pos=0
                    self.cur_pos+=1
                else:
                    self.cur_pos+=1
                    self.inline_pos+=1
        except IndexError:
            return
        if re.match(r"[a-zA-Z]",self.code[self.cur_pos]):
            self.mode="IDENTIFIER_TEMP"
            self.temp_word+=self.code[self.cur_pos]
        elif re.match(r"[0-9]",self.code[self.cur_pos]):
            self.mode = "INTEGER_OR_FLOAT"
            self.temp_word += self.code[self.cur_pos]
        elif self.code[self.cur_pos]=='\"':
            self.mode = "STRING"
            self.temp_word += self.code[self.cur_pos]
        elif self.code[self.cur_pos]=='@':
            self.mode = "START_OR_END"
        elif self.code[self.cur_pos] in initial_directly_add_dict:
            self.already_processed_words.append([self.code[self.cur_pos],initial_directly_add_dict[self.code[self.cur_pos]]])
        elif self.code[self.cur_pos]==">":
            self.mode="ALREADY_READ_GT"
        elif self.code[self.cur_pos]=="<":
            self.mode="ALREADY_READ_LT"
        elif self.code[self.cur_pos]=="=":
            self.mode="ALREADY_READ_EQ"
        elif self.code[self.cur_pos]=="!":
            self.mode="ALREADY_READ_NOT"
        elif self.code[self.cur_pos]=="&":
            self.mode="ALREADY_READ_AND"
        elif self.code[self.cur_pos]=="|":
            self.mode="ALREADY_READ_OR"
        else:
            raise File_Process_Language_Worderror("不合法的输入字符{}".format(self.code[self.cur_pos]))
        self.cur_pos+=1
        self.inline_pos+=1

    def IDENTIFIER_TEMP_status_processor(self):
        try:
            while re.match(r"[0-9a-zA-Z_]",self.code[self.cur_pos]):
                self.temp_word+=self.code[self.cur_pos]
                self.cur_pos+=1
                self.inline_pos+=1
        except IndexError:
            if self.temp_word in reserved_dict_template:
                self.already_processed_words.append([self.temp_word, reserved_dict_template[self.temp_word]])
            else:
                self.already_processed_words.append([self.temp_word, identifier_dict["IDENTIFIER"]])
            return
        if self.code[self.cur_pos] not in break_list:
            raise File_Process_Language_Worderror("{}不是保留字，也不符合标识符的命名规范 {}:{}".format(self.code[self.cur_pos],self.line,self.inline_pos))
        if self.temp_word in reserved_dict_template:
            self.already_processed_words.append([self.temp_word,reserved_dict_template[self.temp_word]])
        else:
            self.already_processed_words.append([self.temp_word,identifier_dict["IDENTIFIER"]])
        self.temp_word=""
        self.mode="INITIAL"

    def INTEGER_OR_FLOAT_status_processor(self):
        try:
            while re.match(r"[0-9]",self.code[self.cur_pos]):
                self.temp_word+=self.code[self.cur_pos]
                self.cur_pos+=1
                self.inline_pos+=1
        except IndexError:
            self.already_processed_words.append([self.temp_word, constant_dict["CONSTANT_INT"]])
            return
        if self.code[self.cur_pos]==".":
            self.temp_word+=self.code[self.cur_pos]
            self.cur_pos+=1
            self.inline_pos+=1
            self.mode="FLOAT"
        else:
            if self.code[self.cur_pos] not in break_list:
                raise File_Process_Language_Worderror("{}在整数中不合法 {}:{}".format(self.code[self.cur_pos],self.line,self.inline_pos))
            self.already_processed_words.append([self.temp_word,constant_dict["CONSTANT_INT"]])
            self.temp_word=""
            self.mode="INITIAL"

    def FLOAT_status_processor(self):
        try:
            while re.match(r"[0-9]",self.code[self.cur_pos]):
                self.temp_word+=self.code[self.cur_pos]
                self.cur_pos+=1
                self.inline_pos+=1
        except IndexError:
            self.already_processed_words.append([self.temp_word, constant_dict["CONSTANT_FLOAT"]])
            return
        if self.code[self.cur_pos] not in break_list:
            raise File_Process_Language_Worderror("{}在浮点数中不合法 {}:{}".format(self.code[self.cur_pos],self.line,self.inline_pos))
        self.already_processed_words.append([self.temp_word, constant_dict["CONSTANT_FLOAT"]])
        self.temp_word=""
        self.mode="INITIAL"

    def STRING_status_processor(self):
        try:
            while 1:
                self.temp_word += self.code[self.cur_pos]
                self.cur_pos+=1
                self.inline_pos+=1
                if (self.code[self.cur_pos-1]=="\"" and self.code[self.cur_pos-2]!="\\"):
                    if re.search('[$][{].*[}]',self.temp_word):
                        self.already_processed_words.append([self.temp_word, constant_dict["FORMAT_STR"]])
                    else:
                        self.already_processed_words.append([self.temp_word, constant_dict["CONSTANT_STR"]])
                    self.temp_word = ""
                    self.mode = "INITIAL"
                    break
                if self.code[self.cur_pos]=="\n":
                    raise File_Process_Language_Worderror("字符串表达式缺少右引号 {}:{}".format(self.line,self.inline_pos))
        except IndexError:
            raise File_Process_Language_Worderror("字符串表达式缺少右引号 {}:{}".format(self.line, self.inline_pos))

    def START_OR_END_status_processor(self):
        try:
            while self.code[self.cur_pos] not in break_list:
                self.temp_word+=self.code[self.cur_pos]
                self.cur_pos+=1
                self.inline_pos+=1
        except IndexError:
            pass
        if self.temp_word=="start":
            self.already_processed_words.append(["@start",reserved_dict["RESERVED_@START"]])
            self.temp_word=""
        elif self.temp_word=="end":
            self.already_processed_words.append(["@end",reserved_dict["RESERVED_@END"]])
            self.temp_word=""
        else:
            raise File_Process_Language_Worderror("只有在@start,@end或字符串中@才是合法的 {}:{}".format(self.line,self.inline_pos))
        self.temp_word=""
        self.mode="INITIAL"

    def ALREADY_READ_GT_status_processor(self):
        if self.code[self.cur_pos]=="=":
            self.already_processed_words.append([">=",operator_dict["OPERATOR_GE"]])
            self.cur_pos+=1
            self.inline_pos+=1
        else:
            self.already_processed_words.append([">",operator_dict["OPERATOR_GT"]])
        self.temp_word=""
        self.mode="INITIAL"

    def ALREADY_READ_LT_status_processor(self):
        if self.code[self.cur_pos]=="=":
            self.already_processed_words.append(["<=",operator_dict["OPERATOR_LE"]])
            self.cur_pos+=1
            self.inline_pos+=1
        else:
            self.already_processed_words.append(["<",operator_dict["OPERATOR_LT"]])
        self.temp_word=""
        self.mode="INITIAL"

    def ALREADY_READ_EQ_status_processor(self):
        if self.code[self.cur_pos]=="=":
            self.already_processed_words.append(["==",operator_dict["OPERATOR_EQ"]])
            self.cur_pos+=1
            self.inline_pos+=1
        else:
            self.already_processed_words.append(["=",operator_dict["OPERATOR_ASSIGNMENT"]])
        self.temp_word=""
        self.mode="INITIAL"

    def ALREADY_READ_NOT_status_processor(self):
        if self.code[self.cur_pos]=="=":
            self.already_processed_words.append(["!=", operator_dict["OPERATOR_NE"]])
            self.cur_pos += 1
            self.inline_pos += 1
        else:
            raise File_Process_Language_Worderror("目前!只支持与=连用表示不等关系，不支持!作为非运算的使用 {}:{}".format(self.line,self.inline_pos))
        self.temp_word=""
        self.mode="INITIAL"

    def ALREADY_READ_AND_status_processor(self):
        if self.code[self.cur_pos]=="&":
            self.already_processed_words.append(["&&", operator_dict["OPERATOR_AND"]])
            self.cur_pos += 1
            self.inline_pos += 1
        else:
            raise File_Process_Language_Worderror("目前只支持&&表示逻辑且，不支持&作为与运算的使用 {}:{}".format(self.line,self.inline_pos))
        self.temp_word=""
        self.mode="INITIAL"

    def ALREADY_READ_OR_status_processor(self):
        if self.code[self.cur_pos]=="|":
            self.already_processed_words.append(["||", operator_dict["OPERATOR_AND"]])
            self.cur_pos += 1
            self.inline_pos += 1
        else:
            raise File_Process_Language_Worderror("目前只支持||表示逻辑或，不支持|作为或运算的使用 {}:{}".format(self.line,self.inline_pos))
        self.temp_word=""
        self.mode="INITIAL"

    def lexical_analysis(self):
        while self.cur_pos<self.length:
            if self.mode=="INITIAL":
                self.INITIAL_status_processor()
            elif self.mode=="IDENTIFIER_TEMP":
                self.IDENTIFIER_TEMP_status_processor()
            elif self.mode=="INTEGER_OR_FLOAT":
                self.INTEGER_OR_FLOAT_status_processor()
            elif self.mode=="FLOAT":
                self.FLOAT_status_processor()
            elif self.mode=="STRING":
                self.STRING_status_processor()
            elif self.mode=="START_OR_END":
                self.START_OR_END_status_processor()
            elif self.mode=="ALREADY_READ_GT":
                self.ALREADY_READ_GT_status_processor()
            elif self.mode=="ALREADY_READ_LT":
                self.ALREADY_READ_LT_status_processor()
            elif self.mode=="ALREADY_READ_EQ":
                self.ALREADY_READ_EQ_status_processor()
            elif self.mode=="ALREADY_READ_NOT":
                self.ALREADY_READ_NOT_status_processor()
            else:
                raise File_Process_Language_Worderror("错误，没有这样的状态 {}".format(self.mode))

    def show_analyse_result(self):
        for item in self.already_processed_words:
            print("{:<40}|{:<10}".format(item[0],item[1]))
