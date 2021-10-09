import os
import sys
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
    
def compress_file(input_file: str, output_file: str):
    """Compress PDF file"""
    if not output_file:
        output_file = input_file
    initial_size = os.path.getsize(input_file)
    try:
        PDFNet.Initialize()
        doc = PDFDoc(input_file)
        doc.InitSecurityHandler()
        Optimizer.Optimize(doc)
        doc.Save(output_file, SDFDoc.e_linearized)
        doc.Close()
    except Exception as e:
        print("Error compress_file=", e)
        doc.Close()
        return False
    compressed_size = os.path.getsize(output_file)
    summary = {
        "Input File": input_file, "Initial Size": get_size_format(initial_size),
        "Output File": output_file, f"Compressed Size": get_size_format(compressed_size)
    }
    # Printing Summary
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return True
