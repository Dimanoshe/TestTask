import sqlite3
import re

import requests
from django.http import HttpResponse
from django.shortcuts import render

from django.views.generic import CreateView
from django.urls import reverse_lazy

from PIL import Image

from TestTask2.settings import MEDIA_URL
from .forms import PostForm, TestForm
from .models import Original

'''class Home(ListView):
    model = Original
    template_name = 'list.html'''


class AddOriginal(CreateView):
    model = Original
    form_class = PostForm
    template_name = 'add_original.html'
    success_url = reverse_lazy('image_form')


def home(request):
    images = Original.objects.values()
    for i in images:
        if i['image'] != '':
            i['image'] = i['image'].split('/')[1]
    context = {'images': images}

    return render(request, 'list.html', context)

def image_form(request):
    images = Original.objects.values()
    image = images[len(images) - 1]
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    if image['image'] == '' and image['image_url'] == '':
        cursor.execute("DELETE FROM uploader_original  WHERE id={}".format(len(images)))
        conn.commit()
        conn.close()
        return HttpResponse('<h1>Файл не выбран.<h1>')
    if image['image'] != '' and image['image_url'] != '':
        cursor.execute("DELETE FROM uploader_original  WHERE id={}".format(len(images)))
        conn.commit()
        conn.close()
        return HttpResponse('<h1>Обе формы оказались заполнены.<h1>')

    if image['image_url'] != '' and request.method != 'POST':
        url = image['image_url']
        resp = requests.get(url, stream=True).raw
        img = Image.open(resp)
        pattern = r'/[^\/]*.png|/[^\/]*.jpg'
        name_url_file = re.findall(pattern, url)
        name_url_file = str(name_url_file[0][1:])
        img.save('media\\Original_img\\' + name_url_file)

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("UPDATE uploader_original SET image_url='{0}' WHERE id={1}".format(name_url_file, len(images)))
        conn.commit()
        conn.close()

        images = Original.objects.values()
        image = images[len(images) - 1]

    if image['image_url'] != '' and request.method == 'POST':
        url = image['image_url']
        pattern = r'/[^\/]*.png|/[^\/]*.jpg'
        name_url_file = re.findall(pattern, url)
        name_url_file = str(name_url_file[0][1:])

    if len(image['image']) > 0:
        img_mod = Image.open('media\\' + str(image['image']))
    else:
        img_mod = Image.open('media\\Original_img\\' + name_url_file)

    width, height = img_mod.size
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("UPDATE uploader_original SET width={0}, height={1} WHERE id={2}".format(width, height, len(images)))
    conn.commit()

    if request.method == 'POST':
        form = TestForm(request.POST)

        width = form.data.get('width')
        height = form.data.get('height')

    else:
        width, height = img_mod.size
        form = TestForm()

    if width == '':
        print('Условие1')
        cursor.execute(
            "SELECT width FROM uploader_original  WHERE id={}".format(len(images)))
        width = cursor.fetchall()[0][0]
        cursor.execute(
            "SELECT height FROM uploader_original  WHERE id={}".format(len(images)))
        old_height = cursor.fetchall()[0][0]
        k = int(height) / int(old_height)
        width *= k
        img_mod = img_mod.resize((int(width), int(height)), Image.ANTIALIAS)

    elif height == '':
        cursor.execute(
            "SELECT height FROM uploader_original  WHERE id={}".format(len(images)))
        height = cursor.fetchall()[0][0]
        cursor.execute(
            "SELECT width FROM uploader_original  WHERE id={}".format(len(images)))
        old_width = cursor.fetchall()[0][0]
        k = int(width) / int(old_width)
        height *= k
        img_mod = img_mod.resize((int(width), int(height)), Image.ANTIALIAS)

    elif height != '' and width != '':
        """
        cursor.execute(
            "SELECT height FROM uploader_original  WHERE id={}".format(len(images)))
        old_height = cursor.fetchall()[0][0]
        print('ДЕЛИМ: ', height, '/', old_height)
        k_height = int(height) / int(old_height)
        print(k_height)
        width = int(width)
        width *= round(k_height, 4)
        print('ШИРИНА ', width)
        cursor.execute(
            "SELECT width FROM uploader_original  WHERE id={}".format(len(images)))
        old_width = cursor.fetchall()[0][0]
        k_width = int(width) / int(old_width)
        print('K_w', k_width)
        height = int( height)
        height *= round(k_width, 4)
        print('ВЫСОТА: ', height)
        img_mod = img_mod.resize((int(width), int(height)), Image.ANTIALIAS)

        """
        img_mod = img_mod.resize((int(width), int(height)), Image.ANTIALIAS)

    conn.close()

    if len(image['image']) > 0:
        name_mod = image['image'].split('/')[1]
        img_mod.save('media\\Modified_img\\' + str(name_mod))
    else:
        name_mod = name_url_file
        img_mod.save('media\\Modified_img\\' + str(name_mod))

    context = {'name_mod': name_mod, 'MEDIA_URL': MEDIA_URL, 'width': width, 'height': height, 'form': form}

    return render(request, 'image.html', context)

