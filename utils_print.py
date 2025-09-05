from termcolor import colored

verbose_level    = 3
enable_info_flag = False
enable_ultra_info= False

def enable_info(e: bool):
    global enable_info_flag 
    global enable_ultra_info
    enable_info_flag = e
    enable_ultra_info = e
    
def log(*msg_args):
    if verbose_level >1 : return
    print("LOG:", *msg_args)

def info(*msg_args):
    global enable_info_flag
    if enable_info_flag:
        print("INFO:", *msg_args)

def info2(*msg_args):
    global enable_ultra_info
    if enable_ultra_info:
        print("INFO2:", *msg_args)

def warning(*msg_args: str):
    print(colored("WARN!", "yellow"), *msg_args)

def error(*msg_args: str):
    print(colored("ERROR", "red"), *msg_args)

def critical(*msg_args: str, err_code=1):
    print(colored("ERROR", "red"), *msg_args)
    exit(err_code)