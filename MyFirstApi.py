# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 20:41:03 2023

@author: HP
"""

import math
from flask import Flask, request, jsonify

dct = {"^":5, "/":4, "*":3, "a":2, "-":1, "":0}
acceptable_char_list = [48,49,50,51,52,53,54,55,56,57,46,110,112,102,115,99,116,83,67,84,69,101]

def utilFact(num):
    pro = 1
    for i in range(1,int(num)+1):
        pro*=i
    return float(pro)

def utilSin(num):
    return math.sin(num)

def utilCos(num):
    return math.cos(num)

def utilTan(num):
    return math.tan(num)

def utilAsin(num):
    return math.asin(num)

def utilAcos(num):
    return math.acos(num)

def utilAtan(num):
    return math.atan(num)

def utilLoge(num):
    return math.log(num, math.exp(1))

def utilExp(num):
    return math.exp(num)

def utilPi():
    return math.pi

def conversion(string):
    if(string[0]=='n'):
        string = string.replace("n", "")
        return -float(string)
    
    elif(string[0]=='f'):
        string = string.replace('f', '')
        temp = float(string)
        return utilFact(temp)
    
    elif(string[0]=='s'):
        string = string.replace('s', '')
        temp = float(string)
        return utilSin(temp)
    
    elif(string[0]=='c'):
        string = string.replace('c', '')
        temp = float(string)
        return utilCos(temp)
    
    elif(string[0]=='t'):
        string = string.replace('t', '')
        temp = float(string)
        return utilTan(temp)
    
    elif(string[0]=='e'):
        string = string.replace('e', '')
        temp = float(string)
        return utilExp(temp)
    
    elif(string[0]=='p'):
        string = string.replace('p', '')
        return utilPi()
    
    elif(string[0]=='S'):
        string = string.replace('S', '')
        temp = float(string)
        return utilAsin(temp)
    
    elif(string[0]=='C'):
        string = string.replace('C', '')
        temp = float(string)
        return utilAcos(temp)
    
    elif(string[0]=='T'):
        string = string.replace('T', '')
        temp = float(string)
        return utilAtan(temp)
    
    elif(string[0]=='E'):
        string = string.replace('E', '')
        temp = float(string)
        return utilLoge(temp)
    
    else:
        return float(string)
    
    
def evaluate(string):
    strg=''
    lst = []
    lstOperator = []
    for i in range(len(string)):
        
        if(ord(string[i]) in [94,42,97,45,47]):
            lstOperator.append(string[i])
            
        if(i==len(string)-1):
            lst.append(conversion(strg+string[len(string)-1]))
            strg=''   
            
        elif(ord(string[i]) in acceptable_char_list):
            strg+=string[i]    
            
        else:
            lst.append(conversion(strg))
            strg=''
    

    while(len(lst) != 1 and len(lstOperator) != 0):
        max_var = ""
        max_index = -1
        
        for i in range(len(lstOperator)):
            if(dct[max_var] < dct[lstOperator[i]]):
                max_var = lstOperator[i]
                max_index = i
      
        if(max_var == "^"):
            res = pow(lst[max_index], lst[max_index+1])
        elif(max_var == "/"):
            res = lst[max_index] / lst[max_index+1]
        elif(max_var == "*"):
            res = lst[max_index] * lst[max_index+1]
        elif(max_var == "a"):
            res = lst[max_index] + lst[max_index+1]
        elif(max_var == "-"):
            res = lst[max_index] - lst[max_index+1]    
        
        lst.pop(max_index)
        lst.pop(max_index)
        lst.insert(max_index, res)
        lstOperator.pop(max_index)
    
    return lst[0]




def separation(string):
    lst_operations = []
    strg=''
    for i in range(len(string)):
        
        if(string[i]=='('):
            lst_operations.append(strg)
            strg=''
            lst_operations.append(string[i])
            
            
        elif(string[i]==')'):
            lst_operations.append(strg)
            strg=''
            lst_operations.append(')')
        
        elif(string[i]=='^' or string[i]=='/' or string[i]=='*' or string[i]=="a" or string[i]=='-'):
            if(string[i-1]==')' and string[i+1]=='('):
                lst_operations.append(string[i])
                
            else:
                strg += string[i]
                
        else:
            if(strg == "" and (string[i]!='^' and string[i]!='/' and string[i]!='*' and string[i]!="a" and string[i]!='-')):
                strg += string[i]

            else:
                strg += string[i]
                
    return lst_operations     
    
    

def join(lst):
    strg=''
    
    for i in lst:
        strg += i
        
    return strg    



app = Flask(__name__)
@app.route("/calculator", methods = ["GET"])
def calculator():
    great_res = {}
    
    string = '(' + str(request.args['query']) + ')'
    
    list_string = separation(string)
    index_start = -1
    index_end = -1
    
    while(len(list_string) >= 1):
    
        for i in range(len(list_string)):
    
            if(list_string[i]=='('):
    
                index_start = i
    
            elif(list_string[i]==')'):
    
                index_end = i
                index_mid = (index_start + index_end)//2
                res = evaluate(list_string[index_mid])
                
                if(res < 0):
                    res = str(res)
                    res = res.replace("-", 'n')
                
                string_res = str(res)
                    
                list_string[index_mid] = string_res
                list_string.pop(index_start)
                list_string.pop(index_mid)
                
                great_res = {"output":string_res}
    
    
                if(len(list_string)==1):
                    break
                
                list_string = separation(join(list_string))
                
                break
    
    loadVar = str(conversion(great_res['output']))
    great_res['output'] = loadVar
    return great_res


if(__name__ == "__main__"):
    app.run()