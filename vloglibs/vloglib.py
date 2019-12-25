'''
   FileName: vloglib.py
   Desc: This is python function to convert between Binary Code & Gray Code
   Author: frank gao
   Email: gao.xuchao@163.com
   HomePage:
   Version: 0.0.1
   LastChange: 2019-12-24 20:25:00
   History:
'''

import re
# import os


def findModule(line):
    '''
        功能：寻找并返回模块名称
        输入：每一行的字符串
        返回：模块名或None
        约束：module 前不能有其它非空字符，模块名必须和Verilog关键字module在同一行
    '''

    # 搜索模块名：然后是多个字母或数字
    search_pattern = r"^\w+"
    # 查找module字段
    sub_pattern = r"^\s*module\s*"

    modulePattern = re.compile(sub_pattern)
    namePattern = re.compile(search_pattern)

    if modulePattern.search(line) is not None:  # 第一个字符串为module

        # 删除行中的[moudle和空格]
        moduleLine = re.sub(sub_pattern, '', line)

        if namePattern.search(moduleLine) is not None:  # 第一个字符串存在
            return namePattern.search(moduleLine).group()
        else:  # 模块名和关键字module不在同一行，抛出异常
            raise Exception("The Module Name is not on the same line as the Verilog Keyword 'module'")
    else:
        return None


def scanText(line, scanIO=True, scanParameter=True):
    '''
       扫描并提取每一行中的input、output、inout、parameter 等Verilog参数
       :param line: 一个字符串
       :param scanIO: 扫描IO使能
       :param scanParameter: 扫描parameter使能
       :return: 返回一个列表，
                list[0] ：
                         0：无参数
                         1：input
                         2：output
                         3：inout
                         4：parameter
                list[1] ：名称
                list[2] ：位宽
        约束：同一行只能有一个io端口或parameter
    '''

    inputPattern = re.compile(r"^\s*input")  # input之前有0个或多个空格

    # 删除所有注释
    lineWithoutComment = re.sub(r"[\\\\|\/\*].*", "", line)

    # 判断输入内容是否符合约束，即冒号和分号后不能有字符出现
    if re.search(r"[;|,]\s*\w+\s*", lineWithoutComment) is not None:
        raise Exception("Warning! characters appear after the end of the sentence :"+line)

    # io匹配使能为真且匹配到input关键字
    if scanIO and (inputPattern.search(lineWithoutComment) is not None):

        # put后跟0个或多个空格，并且出现[
        if re.search(r'put\s*\[', lineWithoutComment) is not None:
            # 提取位宽,[]之间的所有字符
            inputWidth = re.findall(r"\[.*\]", lineWithoutComment)[0]
            # 去除空格
            inputWidth = re.sub(r"\s", "", str(inputWidth))

            # 提取输入名称,]后面跟着0个或多个空格，然后是名称
            # 名称后跟着0个或多个空格，然后是分号或逗号
            inputName = re.findall(r"\]\s*(\w+)\s*[\;\,]", lineWithoutComment)[0]

        else:
            inputWidth = 1  # 位宽为1
            # 提取名称,put后跟0个或多个空格，然后是名称
            # 名称后跟着0个或多个空格，然后是分号或逗号
            inputName = re.findall(r"put\s*(\w+)\s*[\;\,]", lineWithoutComment)[0]

        return 1, inputName, inputWidth

    else:  # 没有匹配到IO或Parameter
        return 0, None, None
