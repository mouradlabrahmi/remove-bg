from PIL import Image as PILImage
from rembg import remove


def removebg(input_path, Output_path):
    input = PILImage.open(input_path)
    output = remove(input)
    output.save(Output_path)
