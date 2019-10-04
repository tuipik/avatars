import os
from PIL import Image
from math import sqrt, ceil


class Collage:
    def __init__(self, list_of_images):
        self.list_of_images = list_of_images
        self.repo = 'repos/'+list_of_images[0].split('/')[1]
        self.collage_width_hight = 800
        self.cols_rows = int(ceil(sqrt(len(self.list_of_images))))
        self.thumbnail_width_height = self.collage_width_hight // self.cols_rows
        self.collage = Image.new('RGB', (self.collage_width_hight,
                                         self.collage_width_hight),
                                 (255, 255, 255))
        self.i = 0
        self.x = 0
        self.y = 0
        self.thumbnail_images = []
        self.run()

    def make_thumbnails(self, images, repo):
        for p in self.list_of_images:
            image = Image.open(p)
            if image.size < (self.thumbnail_width_height,
                             self.thumbnail_width_height):
                image = image.resize((self.thumbnail_width_height,
                                      self.thumbnail_width_height))
            image.thumbnail((self.thumbnail_width_height,
                             self.thumbnail_width_height))
            self.thumbnail_images.append(image)
        return self.thumbnail_images

    def make_collage(self, thumbnails):
        try:
            for col in range(self.cols_rows):
                for row in range(self.cols_rows):
                    self.collage.paste(self.thumbnail_images[self.i],
                                       (self.x, self.y))
                    self.i += 1
                    self.x += self.thumbnail_width_height
                self.y += self.thumbnail_width_height
                self.x = 0
        except IndexError:
            pass
        self.collage.save(f"{self.repo}/Collage.jpg")

    def run(self):
        self.make_collage(self.make_thumbnails(self.list_of_images, self.repo))
        print(f'Done collage {self.repo}')


if __name__ == '__main__':
    list_of_repos = [f'repos/{i}' for i in os.listdir(path="repos")]
    for repo in list_of_repos:
        list_of_images = [f'{repo}/{i}' for i in os.listdir(path=repo)]
        Collage(list_of_images)
