import os
import csv
from tqdm import tqdm
import shutil

def postprocess(folder_path,output_file="output.csv"):
    # open a new csv file for results
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Label'])
        file_list = os.listdir(folder_path)
        print(f"Processing {folder_path}...")
        for file_name in file_list:
            writer.writerow([file_name, file_name[0]])

def renameimgs(folder_path_list,output_dir="./images"):
    for fpindex in range(len(folder_path_list)):
        # the index is the label
        folder_path = folder_path_list[fpindex]
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            old_file_path = os.path.join(folder_path, file_name)
            new_file_path = os.path.join(output_dir, str(fpindex)+file_name)
            f = open(new_file_path,'w') # create new file name
            shutil.move(old_file_path, new_file_path)

if __name__ == "__main__":
    # for some weird reasons, working directory for this program doesn't seem to be in the crawler folder
    folder_path_list = ["./crawler/0","./crawler/1","./crawler/2","./crawler/3"]
    renameimgs(folder_path_list)
    postprocess("./images","output.csv")
    print("Done")