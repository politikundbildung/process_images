# process_images
Takes a folder of images, binarizes and deskews them and converts them to a PDF for OCRing

It uses the deskew function from [wand](https://docs.wand-py.org/en/0.6.12/) and the iSauvola algorithm from [doxapy](https://github.com/brandonmpetty/doxa).

Usage: python3 -i input_folder -o output_file.pdf

The resulting PDF can then be processed with [OCRMyPDF](https://ocrmypdf.readthedocs.io/en/latest/). OCRMyPDF also has its own deskewing algorithm, but I've found that using it increases the file size considerably. 
