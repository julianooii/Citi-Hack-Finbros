import pytesseract
from PIL import Image


image_path = 'picture1.png'
image = Image.open(image_path)
text = pytesseract.image_to_string(image)

print(text)


