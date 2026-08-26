
def mod():
    avamod = ["1. llama3.2","2. qwen3:4b","3.openai/gpt-oss-safeguard-20"]

    print("\nDefault model : llama3.2")
    print("\nAvailable models:")
    for i in avamod:
        print("\n",i)
    
    user_input  = input("\nEnter the model index [Eg. 1 (for llama3.2)] :").strip()

    if(user_input==""):
        modl = "llama3.2"
        print("\nNothing Selected [ Model set to Default ] ")
        return modl

    inx = int(user_input)


    if(inx==1):
        modl = "llama3.2"
    elif(inx==2):
        modl = "qwen3:4b"
    elif(inx==3):
        modl = "openai/gpt-oss-safeguard-20"
    else:
        modl = "llama3.2"
        print("\nEnter the valid Model index [ Model set to Default ]")
        
    
 
    return modl


