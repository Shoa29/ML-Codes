from PIL import Image
import pandas as pd

if __name__ == '__main__':
    filename = "../assets/TEAL.jpg"
    img = Image.open(filename)
    colors = img.getpixel((20, 20))  # giving coordinates to check in image
    (red, green, blue) = colors
    url = '../assets/colors.csv'
    index = ["color", "color_name", "hex", "R", "G", "B"]
    csv = pd.read_csv(url, names=index, header=None)
    df = pd.DataFrame(csv)
    minimum = 100000
    print(red, green, blue)
    for i in range(len(csv)):
        d = abs(red - int(csv.loc[i, "R"])) + abs(green - int(csv.loc[i, "G"])) + abs(blue - int(csv.loc[i, "B"]))
        if (d < minimum):
            minimum = d
            colorName = csv.loc[i, "color_name"]
    print(colorName)



