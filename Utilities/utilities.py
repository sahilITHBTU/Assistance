import os
Start_Sequence = "\033[90m"
End_Sequence = "\033[0m"
def log(text):
    if os.getenv("DEBUG_MODE").lower() == "true":
      print(f" {Start_Sequence}{text}{End_Sequence}")
     