import os
import sys
class example_json():
    def __init__(self):
        cur_dir=os.getcwd()
        json_path=os.path.join(cur_dir,"example_json")
        json_ab_files=[]
        for _,_,files in os.walk(json_path):
            for file in files:

                path=os.path.join(json_path,file)
                json_ab_files.append(path)
                pass
        self.json_ab_files=json_ab_files
        self.json_path=json_path
    def json_list(self):

        for nu in range(len(self.json_ab_files)):
            print(f"[{nu}] : {self.json_ab_files[nu]}")
    def get_json_path(self,nu):
        return self.json_ab_files[nu]
    def new_json_path(self,filename):

        new_path= os.path.join(self.json_path,filename)
        #self.json_ab_files.append(new_path)
        return new_path
