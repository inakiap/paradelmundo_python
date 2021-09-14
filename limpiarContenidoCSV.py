import csv
import logging
import re
import os
import shutil
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from datetime import datetime

class Entrada:
    def __init__(self, id, autor, fecha, ultimo_cambio, titulo, contenido, categorias, etiquetas, numero_comentarios, comentarios):
        self.id = id
        self.titulo = titulo
        self.fecha = fecha
        self.ultimo_cambio = ultimo_cambio
        self.autor = autor
        self.contenido = contenido
        self.categorias = categorias
        self.etiquetas = etiquetas
        self.numero_comentarios = numero_comentarios
        self.comentarios = comentarios

    def __str__(self):
        return '%s, %s, %s, %s, %s, %s' % (self.id, self.titulo, self.autor, self.fecha, self.ultimo_cambio, self.numero_comentarios)
class Comentario:
    def __init__(self, estado, fecha_comentario, autor_comentario, email, contenido_comentario):
        self.estado = estado
        self.fecha_comentario = fecha_comentario
        self.autor_comentario = autor_comentario
        self.email = email
        self.contenido_comentario = contenido_comentario
    
    def __str__(self):
        return '%d, %d, %d, %d, %d' % (self.autor_comentario, self.fecha_comentario, self.email, self.estado, self.contenido_comentario)
class ImgsParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.imgs = []
    self.enlaces = []
    self.enlaces_end = []

  def handle_starttag(self, tag, attributes):
    if tag == 'img':
        self.imgs.append(attributes)
    elif tag == 'a':
        self.enlaces.append(tag)
    else:
        return

  def handle_endtag(self, tag):
      
    if tag == 'a':
        self.enlaces_end.append(tag)

  def handle_data(self, data):
      pass
    # if self.recording:
    #   self.data.append(data)

def leer_csv(archivo):
    logging.info(f'leer_csv [{archivo}]')
    if archivo is not None:
        filas = []
        with open(archivo) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    filas.append(row)
                    line_count += 1
    else:
        logging.error('No hay archivo para leer')
    return filas

def clean_links(raw_html):
  cleanr = re.compile('</a>|<a.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

  #[caption
def clean_caption(raw_html):
  cleanr = re.compile('[/caption]|[caption.*?]')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def tratar_imagenes(data):
    logging.info('tratar_imagenes')
    contenido = data
    parser = ImgsParser()
    parser.feed(data)
    # if len(parser.enlaces) > 0:
    #     for enlace in parser.enlaces:
    #         for attr in enlace:
    #             logging.debug(f'enlace attr {attr}')
    if len(parser.imgs) > 0:
        for img in parser.imgs:
            for attr in img:
                if attr[0] == 'src':
                    x = list(attr)
                    img_ori = x[1]
                    img_corregida = corregir_img(img_ori)
                    x[1] = img_corregida
                    attr = tuple(x)
                    #contenido = data.replace(img_ori,img_corregida)
    return contenido

def corregir_img(img):
    logging.info(f'corregir_img {img}')
    resultado = img
    ruta_local = '/home/inakiap/Projects/backupParadelmundo/'
    ruta_local2 = '/home/inakiap/Imágenes/imgBlogRescatadas'
    if img is not None:
        if "wp-content/uploads" in img:
            resultado = f'{ruta_local}{img[img.find("uploads"):]}'

        if "ggpht.com" in img:
            resultado = f'{ruta_local2}{img[img.rfind("/"):]}'

        if "/galaxy.jpg" in img:
            resultado = '/home/inakiap/Imágenes/galaxy.jpg'
    
    logging.info(f'resultado {resultado}')
    return resultado

def corregir_tildes(texto):
    palabras = re.findall(r'\w+', texto)
    # for palabra in palabras:
    return texto

def formatear_contenido(texto):
    logging.info('formatear_contenido')

    return texto

def corregir_videos(texto):
    return texto

def generar_marca():
    t = datetime.now()
    return f'{t.year:02d}{t.month:02d}{t.day:02d}{t.hour:02d}{t.minute:02d}{t.second:02d}'

def escribir_csv(filas, archivo):
    logging.info('escribir_csv')
    if archivo is not None:
        with open(archivo, 'w') as r:
            writer = csv.writer(r)
            writer.writerows(filas)

def limpiar_contenidos(html):
    logging.info(f'Inicio de limpiarContenidoCSV')
    html = clean_links(html)
    #html = clean_caption(html)
    html = tratar_imagenes(html)
    html = corregir_videos(html)
    html = corregir_tildes(html)
    return html

# def main():
#     logging.basicConfig(filename = f'limpiarcontenidos_{generar_marca()}.log', level=logging.DEBUG)
#     logging.info(f'Inicio de limpiarContenidoCSV')
#     csv = 'todoslosposts.csv'
#     filas = leer_csv(csv)
#     for fila in filas:
#         fila[5] = formatear_contenido(fila[5])
#     file_name = f'contenidos_tratados_{generar_marca()}.csv'
#     escribir_csv(filas, file_name)



# if __name__ == '__main__':
#     main()

