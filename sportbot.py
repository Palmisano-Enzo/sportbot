import wikipast as wp
import text_gen as tg
import traductor as td


from sys import argv, exit
import pandas as pd
from os.path import exists

def check_binary_value(param, param_value):
    if param_value == "1":
        return True
    elif param_value == "0":
        return False
    else:
        print("An incorrect parameter value has been encountered for parameter "+param)
        exit(1)
def check_required_param(param, value):
    if not value:
        print("The "+param+" parameter is required")
        exit(1)
def parse_arguments(args):
    input_file = ""
    output_pre_process = ""
    
    valid_parameter = ["--preprocessing", "--output-file-preprocessing", "--input-file", "--translate", "--jo-type"]
    need_pre_processing = False
    get_input_file = False
    need_translation = False
    jo_type=False
    jo = ""
    
    if len(args)==1:
        print("More than one parameter is needed")
        exit(1)
    elif len(args)%2!=1:
        print("An odd number of parameters is required")
        exit(1)
    else:
        for i in range(1, len(args),2):
            arg =args[i]
            val = args[i+1]
            
            if(arg not in valid_parameter):
                print("Invalid parameter name")
                exit(1)
            if(arg == "--preprocessing"):
                need_pre_processing = check_binary_value(arg, val)
            elif (arg ==  "--output-file-preprocessing"):
                output_pre_process = val
                
            elif (arg == "--input-file"):
                if not exists(val): 
                    print("The input file doesn't exist")
                    exit(1)
                
                input_file = val
                get_input_file = True
            elif (arg == "--translate"):
                need_translation = check_binary_value(arg, val)
                
            elif(arg == "--jo-type"):
                if(val == "winter"):
                    jo = "hiver"
                elif(val == "summer"):
                    jo="été"
                else: 
                    print("Only the value winter or summer can be given for --jo-type")
                    exit(1)
                jo_type = True
                
        check_required_param("--input-file", get_input_file)
        check_required_param("--jo-type", jo_type)
            
    return need_pre_processing, input_file ,output_pre_process, need_translation, jo

def main(argv):
    need_pre_processing, input_file, output_pre_process, need_translation, jo = parse_arguments(argv)
    
    if need_pre_processing:
        if output_pre_process == "":
            out_file="preprocess-"+input_file
        else:
            out_file = output_pre_process
        td.processing(input_file, out_file, need_translation)
       
    load_file = out_file if need_pre_processing else input_file
    data = tg.generate_all_lines(load_file, jo)
    print(data)
    #wp.import_data(data) #Pour éviter les problèmes
    
if __name__ == "__main__":
    main(argv)
    