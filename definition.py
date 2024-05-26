#定义保留字从0-100
reserved_dict={
    "RESERVED_INT":0,
    "RESERVED_FLOAT":1,
    "RESERVED_STR":2,
    "RESERVED_LIST":3,
    "RESERVED_MAKE":4,
    "RESERVED_COPY":5,
    "RESERVED_DELETE":6,
    "RESERVED_MOVE":7,
    "RESERVED_CHANGE":8,
    "RESERVED_WRITE":9,
    "RESERVED_COMPUTE":10,
    "RESERVED_SPLIT":11,
    "RESERVED_READ":12,
    "RESERVED_PRINT":13,
    "RESERVED_@START":14,
    "RESERVED_@END":15,
    "RESERVED_IF":16,
    "RESERVED_WHILE":17,
    "RESERVED_AGGREGATE":18
}

#定义常量 从100-200
constant_dict={
    "CONSTANT_INT":100,
    "CONSTANT_FLOAT":101,
    "CONSTANT_STR":102,
    "FORMAT_STR":103
}

#定义界限符 300
border_dict={
    "BORDER_SEMICOLON":300,
    "BORDER_COMMA":301,
    "BORDER_DQUATATION_MARK":302,
    "BORDER_LCURLYBRASE": 303,  # {
    "BORDER_RCURLYBRASE": 304,  # }
}

#定义标识符 400
identifier_dict={
    "IDENTIFIER":400
}

#定义运算符 500+
operator_dict={
    "OPERATOR_PLUS":500,
    "OPERATOR_MINUS":501,
    "OPERATOR_MUL":502,
    "OPERATOR_DIV":503,
    "OPERATOR_MOD":504,
    "OPERATOR_GT":505,
    "OPERATOR_LT":506,
    "OPERATOR_GE":507,
    "OPERATOR_LE":508,
    "OPERATOR_EQ":509,
    "OPERATOR_NE":510,
    "OPERATOR_AND":511,
    "OPERATOR_OR":512,
    "OPERATOR_ASSIGNMENT":513,
    "OPERATOR_GETVALUE":514,
    "OPERATOR_LPAREN": 515,  # (
    "OPERATOR_RPAREN": 516,  # )
    "OPERATOR_LBRACKET": 517,  # [   认为列表是一个算符
    "OPERATOR_RBRACKET": 518,  # ]
}

initial_directly_add_dict={"+":operator_dict["OPERATOR_PLUS"],
                           "-":operator_dict["OPERATOR_MINUS"],
                           "*":operator_dict["OPERATOR_MUL"],
                           "/":operator_dict["OPERATOR_DIV"],
                           "%":operator_dict["OPERATOR_MOD"],
                           "(":operator_dict["OPERATOR_LPAREN"],
                           ")":operator_dict["OPERATOR_RPAREN"],
                           "[":operator_dict["OPERATOR_LBRACKET"],
                           "]":operator_dict["OPERATOR_RBRACKET"],
                           ";":border_dict["BORDER_SEMICOLON"],
                           "{":border_dict["BORDER_LCURLYBRASE"],
                           "}":border_dict["BORDER_RCURLYBRASE"],
                           ",":border_dict["BORDER_COMMA"]
                           }
reserved_dict_template={
    "int":reserved_dict["RESERVED_INT"],
    "float":reserved_dict["RESERVED_FLOAT"],
    "str":reserved_dict["RESERVED_STR"],
    "list":reserved_dict["RESERVED_LIST"],
    "make":reserved_dict["RESERVED_MAKE"],
    "copy":reserved_dict["RESERVED_COPY"],
    "delete":reserved_dict["RESERVED_DELETE"],
    "move":reserved_dict["RESERVED_MOVE"],
    "change":reserved_dict["RESERVED_CHANGE"],
    "write":reserved_dict["RESERVED_WRITE"],
    "compute":reserved_dict["RESERVED_COMPUTE"],
    "split":reserved_dict["RESERVED_SPLIT"],
    "read":reserved_dict["RESERVED_READ"],
    "print":reserved_dict["RESERVED_PRINT"],
    "@start":reserved_dict["RESERVED_@START"],
    "@end":reserved_dict["RESERVED_@END"],
    "if":reserved_dict["RESERVED_IF"],
    "while":reserved_dict["RESERVED_WHILE"],
    "aggregate":reserved_dict["RESERVED_AGGREGATE"]
}
skip_list=[" ","\n"]
break_list=[" ","\n","(",")","[","]","{","}","&","|","!","+","-","*","%","/",">","<","=",";",","]


BODY_FIRST_LIST=[reserved_dict["RESERVED_INT"],reserved_dict["RESERVED_FLOAT"],reserved_dict["RESERVED_STR"],
                 reserved_dict["RESERVED_LIST"],reserved_dict["RESERVED_MAKE"],reserved_dict["RESERVED_COPY"],
                 reserved_dict["RESERVED_DELETE"],reserved_dict["RESERVED_MOVE"],reserved_dict["RESERVED_CHANGE"],
                 reserved_dict["RESERVED_WRITE"],reserved_dict["RESERVED_COMPUTE"],reserved_dict["RESERVED_SPLIT"],
                 reserved_dict["RESERVED_READ"],reserved_dict["RESERVED_PRINT"],identifier_dict["IDENTIFIER"],
                 reserved_dict["RESERVED_IF"],reserved_dict["RESERVED_WHILE"],reserved_dict["RESERVED_AGGREGATE"]]
BODY_FOLLOW_LIST=[border_dict["BORDER_LCURLYBRASE"],reserved_dict["RESERVED_@END"]]
SENTENCE_FIRST_LIST=[reserved_dict["RESERVED_INT"],reserved_dict["RESERVED_FLOAT"],reserved_dict["RESERVED_STR"],
                 reserved_dict["RESERVED_LIST"],reserved_dict["RESERVED_MAKE"],reserved_dict["RESERVED_COPY"],
                 reserved_dict["RESERVED_DELETE"],reserved_dict["RESERVED_MOVE"],reserved_dict["RESERVED_CHANGE"],
                 reserved_dict["RESERVED_WRITE"],reserved_dict["RESERVED_COMPUTE"],reserved_dict["RESERVED_SPLIT"],
                 reserved_dict["RESERVED_READ"],reserved_dict["RESERVED_PRINT"],identifier_dict["IDENTIFIER"],
                 reserved_dict["RESERVED_IF"],reserved_dict["RESERVED_WHILE"],reserved_dict["RESERVED_AGGREGATE"]]
SUB_BODY_FIRST_LIST=[reserved_dict["RESERVED_INT"],reserved_dict["RESERVED_FLOAT"],reserved_dict["RESERVED_STR"],
                 reserved_dict["RESERVED_LIST"],reserved_dict["RESERVED_MAKE"],reserved_dict["RESERVED_COPY"],
                 reserved_dict["RESERVED_DELETE"],reserved_dict["RESERVED_MOVE"],reserved_dict["RESERVED_CHANGE"],
                 reserved_dict["RESERVED_WRITE"],reserved_dict["RESERVED_COMPUTE"],reserved_dict["RESERVED_SPLIT"],
                 reserved_dict["RESERVED_READ"],reserved_dict["RESERVED_PRINT"],identifier_dict["IDENTIFIER"],
                 reserved_dict["RESERVED_IF"],reserved_dict["RESERVED_WHILE"],reserved_dict["RESERVED_AGGREGATE"]]
SUB_BODY_FOLLOW_LIST=[reserved_dict["RESERVED_@END"],border_dict["BORDER_RCURLYBRASE"]]
NORMAL_SENTENCE_FIRST_LIST=[reserved_dict["RESERVED_INT"],reserved_dict["RESERVED_FLOAT"],reserved_dict["RESERVED_STR"],
                             reserved_dict["RESERVED_LIST"],identifier_dict["IDENTIFIER"],reserved_dict["RESERVED_MAKE"],reserved_dict["RESERVED_COPY"],
                             reserved_dict["RESERVED_DELETE"],reserved_dict["RESERVED_MOVE"],reserved_dict["RESERVED_CHANGE"],
                             reserved_dict["RESERVED_WRITE"],reserved_dict["RESERVED_COMPUTE"],reserved_dict["RESERVED_SPLIT"],
                             reserved_dict["RESERVED_READ"],reserved_dict["RESERVED_PRINT"],reserved_dict["RESERVED_AGGREGATE"]]
LOOP_SENTENCE_FIRST_LIST=[reserved_dict["RESERVED_WHILE"]]
BRANCH_SENTENCE_FIRST_LIST=[reserved_dict["RESERVED_IF"]]
DECLARE_SENTENCE_FIRST_LIST=[reserved_dict["RESERVED_INT"],reserved_dict["RESERVED_FLOAT"],reserved_dict["RESERVED_STR"],
                             reserved_dict["RESERVED_LIST"]]
ASSIGNMENT_SENTENCE_FIRST_LIST=[identifier_dict["IDENTIFIER"]]
COMMAND_SENTENCE_FIRST_LIST=[reserved_dict["RESERVED_MAKE"],reserved_dict["RESERVED_COPY"],
                             reserved_dict["RESERVED_DELETE"],reserved_dict["RESERVED_MOVE"],reserved_dict["RESERVED_CHANGE"],
                             reserved_dict["RESERVED_WRITE"],reserved_dict["RESERVED_COMPUTE"],reserved_dict["RESERVED_SPLIT"],
                             reserved_dict["RESERVED_READ"],reserved_dict["RESERVED_PRINT"],reserved_dict["RESERVED_AGGREGATE"]]
SUB_DECLARE_SENTENCE_FOLLOW_LIST=[border_dict["BORDER_SEMICOLON"]]
SUB_ASSIGNABLE_OBJECT_FIRST_LIST=[operator_dict["OPERATOR_LBRACKET"]]
SUB_ASSIGNABLE_OBJECT_FOLLOW_LIST=[operator_dict["OPERATOR_ASSIGNMENT"],operator_dict["OPERATOR_PLUS"],operator_dict["OPERATOR_MINUS"],operator_dict["OPERATOR_MUL"],operator_dict["OPERATOR_DIV"],operator_dict["OPERATOR_MOD"],
               operator_dict["OPERATOR_GT"],operator_dict["OPERATOR_LT"],operator_dict["OPERATOR_GE"],operator_dict["OPERATOR_LE"],operator_dict["OPERATOR_EQ"],
               operator_dict["OPERATOR_NE"],operator_dict["OPERATOR_AND"],operator_dict["OPERATOR_OR"],border_dict["BORDER_SEMICOLON"],border_dict["BORDER_COMMA"],operator_dict["OPERATOR_RPAREN"]]
CONSTANT_NUM_FIRST_LIST=[constant_dict["CONSTANT_INT"],operator_dict["OPERATOR_MINUS"],constant_dict["CONSTANT_FLOAT"]]
LIST_CONTAIN_FIRST_LIST=[constant_dict["CONSTANT_INT"],operator_dict["OPERATOR_MINUS"], constant_dict["CONSTANT_FLOAT"],
                            constant_dict["CONSTANT_STR"],constant_dict["FORMAT_STR"]]
LIST_CONTAIN_FOLLOW_LIST=[operator_dict["OPERATOR_RBRACKET"]]
CONSTANT_FIRST_LIST=[constant_dict["CONSTANT_INT"],operator_dict["OPERATOR_MINUS"],constant_dict["CONSTANT_FLOAT"],constant_dict["CONSTANT_STR"],
                         constant_dict["FORMAT_STR"],operator_dict["OPERATOR_LBRACKET"]]
SUB_EXPRESSION_FOLLOW_LIST=[border_dict["BORDER_SEMICOLON"],operator_dict["OPERATOR_RPAREN"],border_dict["BORDER_COMMA"]]
OPERATOR_LIST=[operator_dict["OPERATOR_PLUS"],operator_dict["OPERATOR_MINUS"],operator_dict["OPERATOR_MUL"],operator_dict["OPERATOR_DIV"],operator_dict["OPERATOR_MOD"],
               operator_dict["OPERATOR_GT"],operator_dict["OPERATOR_LT"],operator_dict["OPERATOR_GE"],operator_dict["OPERATOR_LE"],operator_dict["OPERATOR_EQ"],
               operator_dict["OPERATOR_NE"],operator_dict["OPERATOR_AND"],operator_dict["OPERATOR_OR"]]
FILEMOVE_COMMAND_LIST=[reserved_dict["RESERVED_MAKE"],reserved_dict["RESERVED_MOVE"],reserved_dict["RESERVED_DELETE"],reserved_dict["RESERVED_COPY"]]
FILEREADWRITE_COMMAND_LIST=[reserved_dict["RESERVED_WRITE"],reserved_dict["RESERVED_READ"],reserved_dict["RESERVED_CHANGE"]]
OTHER_COMMAND_LIST=[reserved_dict["RESERVED_COMPUTE"],reserved_dict["RESERVED_SPLIT"],reserved_dict["RESERVED_AGGREGATE"],reserved_dict["RESERVED_PRINT"]]
