# PhotoJourney

PhotoJourney is a batch image EXIF metadata export tool in Python. Search through all the image files under a selected folder (including subfolder) and export the desired metadata of each image into a CSV file.

## Features

- Batch EXIF metadata export
- RAW file support
- Customize your export configuration

Get to know what are your frequently used focal length, aperture value, camera model and lens model. 

Getting metadata from a single image file is simple, but it could be hard when you want to get all the metadata from whole bunch of files or scattered files in an organized folder structure since there are few programs providing such tool. 

PhotoJourney provides a rudimentary implementation of this. PhotoJourney uses `exifread` module to extract user specified EXIF metadata from digital image files, including `TIFF, JPG, NEF, ARW, CR2, CR3, DNG`, and export the data into a `CSV` file. Then user can use a spreadsheet editor (e.g. `Microsoft Excel`) to analyze the data from the `CSV` file.

## How to use

1. Click `PhotoJourney.exe` to run.

![](/tutorial_screenshots/screenshot01.png)

2. Click `Select Folder` to select the folder you want to collect the metadata from. (support select the root folder of your image gallery)

![](/tutorial_screenshots/screenshot02.png)

2. 1 Once the folder is selected, the path of it will be displayed on the label below.

![](/tutorial_screenshots/screenshot03.png)

3. Then choose the metadata you want to contain in the output `CSV` file.

![](/tutorial_screenshots/screenshot04.png)

4. Click `Start Counting`.

5. Enter the file name for the output file in the following window.

   ![](D:\Projects\photograph_journey\docs\tutorial_screenshots\screenshot05.png)

6. Select the path in which you want to store the output file.
7. Click `Start`

![](/tutorial_screenshots/screenshot06.png)

8. The current extract status will be displayed on the text browser below.

![](/tutorial_screenshots/screenshot07.png)

Notice: DO NOT click `OK` until the `Done!` message appears.

9. After the extract process ends, the total amount of the images in the folder will be displayed

   ![](/tutorial_screenshots/screenshot08.png)

10. Then you can find the output file in the path just selected.

    ![](/tutorial_screenshots/screenshot09.png)
