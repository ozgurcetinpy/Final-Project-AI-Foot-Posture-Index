import os

folder_path = r"C:\Users\ozgur\bitirmeprojesi\YoloV8\NewFormat2\NewFormat\6_Sol\-1" 
prefix = "sol_-1_" # İsimlendirme için ön ek belirleyin
counter = 1 # Başlangıç sayısını belirleyin

for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        new_filename = prefix + str(counter) + ".jpg"
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
        counter += 1
