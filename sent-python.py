"""
    Reimplementation of sent https://github.com/hoijui/sent using Python.
    Requires: PIL.
    Usage: python sent-python.py config input.txt output.pdf

"""

from PIL import Image, ImageDraw, ImageFont
import sys
FILENAME_CONFIG     = sys.argv[1]
FILENAME_INPUT      = sys.argv[2]
FILENAME_OUTPUT     = sys.argv[3]


def slideType(slideTXT):
    if slideTXT[0]=="@":
        return "PICTURE"
    return "NORMAL"

def createSlide(slideTXT, parameters):
    #returns a PIL picture
    width  = int(parameters["width"])
    height = int(parameters["height"])
    image  = Image.new(mode  = "RGB",
                          size  = (width, height),
                          color = parameters["background-color"])
    draw = ImageDraw.Draw(image)
    sType=slideType(slideTXT)
    fontsize = 1
    arial = ImageFont.truetype("arial.ttf", fontsize)
    if sType=="NORMAL":
        img_fraction = 1
        while max(arial.getsize(slideTXT)[0:1]) < min([img_fraction*image.size[0],img_fraction*image.size[1]]):
            fontsize += 100
            arial = ImageFont.truetype("arial.ttf", fontsize)
        draw.text((width/2, height/2), slideTXT, font=arial, fill=parameters["text-color"], anchor="mm")
    if sType=="PICTURE":
        #load picture
        picture_URL   = slideTXT[1:]
        slide_picture = Image.open(picture_URL)
        slide_picture.thumbnail((width, height))
        slide_picture_height = slide_picture.size[1]
        slide_picture_width = slide_picture.size[0]
        image.paste(slide_picture, (int((width-slide_picture_width)/2), int((height-slide_picture_height)/2)))
        #draw.text((width/2, height/2), slideTXT, font=arial, fill=parameters["text-color"], anchor="mm")
    return image

#load parameters
with open(FILENAME_CONFIG, 'r') as f:
    data   = [l[:-1] for l in f.readlines() if not len(l)<1]
PARAMETERS = {}
for line in data:
    couple = line.split(",")
    name   = couple[0]
    value  = couple[1]
    PARAMETERS[name] = value

#load document
SLIDES = []
with open(FILENAME_INPUT, 'r') as f:
    data = f.read()
SLIDES = data.split("\n\n")
counter = 0
images = []
for slideTXT in SLIDES:
    counter+=1
    image = createSlide(slideTXT, PARAMETERS)
    images.append(image)
    #image.save(str(counter).zfill(3)+'.png')
images[0].save(
    FILENAME_OUTPUT, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
)    