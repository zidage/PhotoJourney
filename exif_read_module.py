import exifread
import os
import csv
from PyQt5.QtWidgets import QApplication

class exif_reader:

    def __init__(self, cl, fn, op, opt):
        self.count = 0
        self.file_name = fn
        self.output_path = op
        self.client = cl
        self.option = opt


    def find_file(self, curr_path, csv_writer, types, desired_metadata):
        files = os.listdir(curr_path)
        for file in files:
            if os.path.isdir(curr_path+'\\'+file):
                next_path = curr_path+'\\'+file
                self.find_file(next_path, csv_writer, types, desired_metadata)
            else:
                curr_file_path = curr_path+'\\'+file
                file_type = os.path.splitext(curr_file_path)[1]
                if file_type in types:
                    f = open(curr_file_path, 'rb')
                    tags = exifread.process_file(f)
                    metadata_set = []
                    analyze_message = ""
                    if "Focal Length" in desired_metadata:
                        if "EXIF FocalLength" in tags:
                            focal_length = eval(str(tags["EXIF FocalLength"]))
                            metadata_set.append(focal_length)
                            analyze_message += ("Focal Length: " + str(focal_length) + "mm ")
                    if "Aperture F Stop" in desired_metadata:
                        if "EXIF FNumber" in tags:
                            aperture_val = eval(str(tags["EXIF FNumber"]))
                            metadata_set.append(aperture_val)
                            analyze_message += ("f:/" + str(aperture_val) + " ")
                    if "Camera Model" in desired_metadata:
                        if "Image Make" in tags and "Image Model" in tags:
                            camera_model = str(tags["Image Make"]) + " " + str(tags["Image Model"])
                            metadata_set.append(camera_model)
                            analyze_message += ("Camera: " + camera_model + " ")
                    if "Lens Model" in desired_metadata:
                        if "EXIF LensModel" in tags:
                            lens_model = str(tags["EXIF LensModel"])
                            metadata_set.append(lens_model)
                            analyze_message += ("Lens: " + lens_model)

                    if len(metadata_set) > 0:
                        csv_writer.writerow(metadata_set)
                        self.client.browser_label.append(str(file_type[1:]+" File:" + curr_file_path + " Analyzed!\nResult:\n" + analyze_message + "\n"))
                        QApplication.processEvents()
                        self.count += 1
                    
                    else:
                        self.client.browser_label.append("No valid metadata in file: %s!\n" % curr_file_path)
                        QApplication.processEvents()
                        

    def reader(self, path):
        types = ['.JPG', '.jpg', '.NEF', '.ARW',
                '.CR2', '.CR3', '.tif', '.dng']
        
        metadata = ["Focal Length", "Aperture F Stop", "Camera Model", "Lens Model"]

        desired_metadata = []

        option = self.option

        i = 1
        j = 0
        while i <= 8:
            if i & option:
                desired_metadata.append(metadata[j])
            j += 1
            i = i << 1


        csv_file = open(self.output_path + '\\%s.csv' % self.file_name,
                        'w+', encoding='utf-8', newline='')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(desired_metadata)

        self.find_file(path, csv_writer, types, desired_metadata)
        self.client.browser_label.append('Done!')
