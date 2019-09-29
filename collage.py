import os
from PIL import Image
from pprint import pprint
from math import sqrt, ceil


list_of_repos = [f'repos/{i}' for i in os.listdir(path="repos")]
# pprint(list_of_repos)
list_of_images = [f'repos/1_LikeButton/{i}' for i in os.listdir(path="repos/1_LikeButton")]
pprint(list_of_images)



def create_collage(listofimages):
    collage_width_hight = 800
    cols_rows = int(ceil(sqrt(len(list_of_images))))
    thumbnail_width_height = collage_width_hight//cols_rows
    collage = Image.new('RGB', (collage_width_hight, collage_width_hight),
                        (255, 255, 255))

    thumbnail_images = []
    for p in list_of_images:
        image = Image.open(p)
        image.thumbnail((thumbnail_width_height, thumbnail_width_height))
        thumbnail_images.append(image)
    i = 0
    x = 0
    y = 0
    try:
        for col in range(cols_rows):
            for row in range(cols_rows):
                print(i, x, y)
                collage.paste(thumbnail_images[i], (x, y))
                i += 1
                x += thumbnail_width_height
            y += thumbnail_width_height
            x = 0
    except IndexError:
        pass
    collage.save("repos/Collage.jpg")


create_collage(list_of_images)
