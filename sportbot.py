import wikipast as wp
import text_gen as tg


from sys import argv, exit
import pandas as pd
from os.path import exists

def parse_arguments(args):
    input_file = ""
    output_pre_process = ""
    
    valid_parameter = ["--preprocessing", "--output-file-preprocessing", "--input-file"]
    need_pre_processing = False
    get_input_file = False
    
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
                if val == "1":
                    need_pre_processing = True
                elif val == "0":
                    need_pre_processing = False
                else:
                    print("An incorrect parameter value has been encountered for parameter --preprocessing")
                    exit(1)
            elif (arg ==  "--output-file-preprocessing"):
                output_pre_process = val
                
            elif (arg == "--input-file"):
                if not exists(val): 
                    print("The input file doesn't exist")
                    exit(1)
                
                input_file = val
                get_input_file = True
                
        if not get_input_file:
            print("The --input-file parameter is required")
            exit(1)
            
    return need_pre_processing, input_file ,output_pre_process

def main(argv):
    need_pre_processing, input_file, output_pre_process = parse_arguments(argv)
    
    if need_pre_processing:
        if output_pre_process == "":
            out_file="preprocess-"+input_file
        else:
            out_file = output_pre_process
    #    preprocess()
       
    load_file = out_file if need_pre_processing else input_file
    data = tg.generate_all_lines(load_file)
    # wk.import_data(data)
    
if __name__ == "__main__":
    main(argv)
