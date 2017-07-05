# -*- coding: utf-8 -*-

import argparse
import os
import random
from PIL import Image


def make_image(images, filename, width, init_height):
    
    margin_size = 2

    while True:

        images_list = images[:]
        images_line = []
        coefficient_edge = []
        real_width = 0

        while images_list:

            img_path = images_list.pop(0)
            img = Image.open(img_path)
            img.thumbnail((width, init_height))

            if real_width > width:
                coefficient_edge.append((float(real_width) / width, images_line))
                images_line = []
                real_width = 0
            real_width += img.size[0] + margin_size
            images_line.append(img_path)

        coefficient_edge.append((float(real_width) / width, images_line))

        if len(coefficient_edge) <= 1:
            break

        if any(map(lambda c: len(c[1]) <= 1, coefficient_edge)):
            init_height -= 10
        else:
            break

    out_height = 0
    for coef, imgs_line in coefficient_edge:
        if imgs_line:
            out_height += int(init_height / coef) + margin_size
    
    family_image = Image.new('RGB', (width, int(out_height)), (35, 35, 35))
    y = 0
    for coef, imgs_line in coefficient_edge:
        if imgs_line:
            real_width = 0
            for img_path in imgs_line:
                img = Image.open(img_path)
                k = (init_height / coef) / img.size[1]
                if k > 1:
                    img = img.resize((int(img.size[0] * k), int(img.size[1] * k)), Image.ANTIALIAS)
                else:
                    img.thumbnail((int(width / coef), int(init_height / coef)), Image.ANTIALIAS)
                if family_image:
                    family_image.paste(img, (int(real_width), int(y)))
                real_width += img.size[0] + margin_size
            y += int(init_height / coef) + margin_size
    family_image.save(filename)
    return True


def create(source = "data", destination_file="family.jpg" , width=2000, init_height=200):
   
    files = [os.path.join(source, fn) for fn in os.listdir(source)]
    images = [fn for fn in files if os.path.splitext(fn)[1].lower() in ('.jpg', '.jpeg', '.png')]
    
    res = make_image(images, destination_file, width, init_height)
    print('Image is ready. Enjoy!')


if __name__ == '__main__':
    create()
