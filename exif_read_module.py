import exifread
import os
import csv

class exif_reader:

    def __init__(self):
        self.count = 0
        self.file_name = None
        self.output_path = None

    def find_file(self, curr_path, csv_writer, types):
        files = os.listdir(curr_path)
        for file in files:
            if os.path.isdir(curr_path+'\\'+file):
                next_path = curr_path+'\\'+file
                self.find_file(next_path, csv_writer, types)
            else:
                curr_file_path = curr_path+'\\'+file
                file_type = os.path.splitext(curr_file_path)[1]
                if file_type in types:
                    f = open(curr_file_path, 'rb')
                    tags = exifread.process_file(f)
                    if "EXIF FocalLength" in tags:
                        focal_length = eval(str(tags["EXIF FocalLength"]))
                        aperture_val = eval(str(tags["EXIF FNumber"]))
                        csv_writer.writerow([focal_length, aperture_val])
                        print(file_type[1:]+"文件："+curr_file_path+" 解析结果：\n焦距：" +
                            str(focal_length)+"mm        光圈f/"+str(aperture_val))
                        self.count += 1
                        

    def reader(self, path):
        types = ['.JPG', '.jpg', '.NEF', '.ARW',
                '.CR2', '.CR3', '.tif', '.dng']
        #if not os.path.exists(path+"\\output"):
            #os.mkdir("output")
        
        csv_file = open(self.output_path + '\\%s.csv' % self.file_name,
                        'w+', encoding='utf-8', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["焦段", "光圈"])

        self.find_file(path, csv_writer, types)
