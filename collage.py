import os
from PIL import Image
from math import sqrt, ceil


def create_collage(list_of_images, repo):
    collage_width_hight = 800
    cols_rows = int(ceil(sqrt(len(list_of_images))))
    thumbnail_width_height = collage_width_hight//cols_rows
    collage = Image.new('RGB', (collage_width_hight, collage_width_hight),
                        (255, 255, 255))

    thumbnail_images = []
    for p in list_of_images:
        image = Image.open(p)
        if image.size < (thumbnail_width_height, thumbnail_width_height):
            image = image.resize((thumbnail_width_height, thumbnail_width_height))
        image.thumbnail((thumbnail_width_height, thumbnail_width_height))
        thumbnail_images.append(image)
    i = 0
    x = 0
    y = 0
    try:
        for col in range(cols_rows):
            for row in range(cols_rows):
                collage.paste(thumbnail_images[i], (x, y))
                i += 1
                x += thumbnail_width_height
            y += thumbnail_width_height
            x = 0
    except IndexError:
        pass
    collage.save(f"{repo}/Collage.jpg")


list_of_repos = [f'repos/{i}' for i in os.listdir(path="repos")]
for repo in list_of_repos:
    list_of_images = [f'{repo}/{i}' for i in os.listdir(path=repo)]
    create_collage(list_of_images, repo)
