import csv
import html
import logging
import re
import codecs

from html.parser import HTMLParser
from datetime import datetime
from dominate import document
from dominate.tags import *
from dominate.util import raw
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from bs4 import BeautifulSoup
import limpiarContenidoCSV
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

def csv_en_entradas(filas):
    logging.info(f'csv_en_entradas')
    libro = []
    comentarios = []
    if filas is not None:
        id_comentario = -1
        numero_comentarios = -1
        logging.info(f'Número de filas en el CSV: {len(filas)}')
        for fila in filas:
            if id_comentario != fila[0]:
                id_comentario = fila[0]
                numero_comentarios = int(fila[8])
                if numero_comentarios > 1:
                    numero_comentarios,comentarios = rellenar_comentarios(fila, numero_comentarios, comentarios)
                elif numero_comentarios == 1:
                    numero_comentarios,comentarios = rellenar_comentarios(fila, numero_comentarios, comentarios)                    
                    libro, comentarios = rellenar_libro(fila, libro, comentarios)
                else:
                    libro, comentarios = rellenar_libro(fila, libro, comentarios)
            else:  
                if numero_comentarios > 1:
                    numero_comentarios,comentarios = rellenar_comentarios(fila, numero_comentarios, comentarios)                    
                else:
                    numero_comentarios,comentarios = rellenar_comentarios(fila, numero_comentarios, comentarios)                    
                    libro, comentarios = rellenar_libro(fila, libro, comentarios)
    else:
        logging.error('Error no hay archivo')
    logging.info(f'Número de entradas: {len(libro)}')
    return libro

def rellenar_comentarios(fila, indice_comentario, comentarios):
    logging.info(f'rellenar_comentarios')
    comentarios.append(Comentario(fila[9],fila[10],fila[11],fila[12],fila[13]))
    indice_comentario -= 1
    linea = f'  ~ [{fila[10]}] Comentario de {fila[11]}'
    print(linea)
    logging.debug(linea)
    return indice_comentario, comentarios

def rellenar_libro(fila, entradas, comentarios):
    logging.info('rellenar_libro')
    contenido = maquetar_contenido(fila[5])
    fecha = formato_fecha(fila[2])
    categorias = formato_categorias(fila[6])
    etiquetas = formato_etiquetas(fila[7])
    entradas.append(Entrada(fila[0],fila[1],fecha,fila[3],fila[4],contenido,categorias, etiquetas,fila[8],comentarios))
    comentarios = []
    linea = f'Entrada [{fila[0]}] [{fila[3]}] {fila[4]} de {fila[1]}'
    print(linea)
    logging.debug(linea)
    return entradas, comentarios 

def maquetar_contenido(texto):
    print(texto)
    resultado = clean_links(texto)
    # resultado = clean_caption(resultado)
    resultado = tratar_imagenes(resultado)
    return resultado

def formato_fecha(fecha):
    dt_format = datetime.strptime(fecha,'%Y-%m-%d %H:%M:%S')
    resultado = datetime.strftime(dt_format, '%d/%m/%Y')
    return resultado

def formato_categorias(texto):
    if texto == 'NULL':
        texto = ''
    return texto

def formato_etiquetas(texto):
    if texto == 'NULL':
        texto = ''
    return texto

def clean_links(raw_html):
  cleanr = re.compile('</a>|<a.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def clean_caption(raw_html):
  cleanr = re.compile('[caption .*?]')
#   cleanr = re.compile('[/caption]|[caption .*?]')
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
    contenido = data
    if len(parser.imgs) > 0:
        for img in parser.imgs:
            for attr in img:
                if attr[0] == 'src':
                    x = list(attr)
                    img_ori = x[1]
                    img_corregida = corregir_img(img_ori)
                    x[1] = img_corregida
                    attr = tuple(x)
                    contenido = contenido.replace(img_ori,img_corregida)
                elif attr[0] == 'height' or attr[0] == 'width' or attr[0] == 'alt' or attr[0] == 'class':
                    x = f'{attr[0]}="{attr[1]}" '
                    contenido = contenido.replace(x,'')
    print(contenido)
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

def generar_marca():
    t = datetime.now()
    return f'{t.year}{t.month:02d}{t.day:02d}{t.hour:02d}{t.minute:02d}{t.second:02d}'

def escribir_txt(entradas, archivo):
    logging.info('escribir_txt')
    if archivo is not None:
        with open(archivo, 'w') as r:
            for entrada in entradas:
                logging.debug(entrada)
                r.write(entrada)

def escribir_html(html, archivo):
    logging.info('escribir_html')
    if archivo is not None:
        html_file = open(archivo,"w")
        html_file.write(html)
        html_file.close()

def limpiar_entradas(libro):
    logging.info('limpiar entradas')
    #tomar el contenido y limpiar el formato html y listar los elementos gráficos

    return libro

def main():
    logging.basicConfig(filename = f'paradelmundo2PDF_{generar_marca()}.log', level=logging.DEBUG)
    logging.info(f'main')
    csv = 'entradas_Limpias.csv'
    #csv = 'contenidos_tratados_2021620592.csv'
    filas = leer_csv(csv)
    libro_bruto = csv_en_entradas(filas)
    entradas_limpiadas = limpiar_entradas(libro_bruto)


    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('showentradas2.html')
    output = template.render(entradas=libro_bruto)
    #print(output)

    soup = BeautifulSoup(output)
    output = soup.prettify()
    
    # file_name = f'paradelHTML_Temp.html'
    file_name = f'paradelHTML_{generar_marca()}.html'

    #output = limpiarContenidoCSV.limpiar_contenidos(output)    
    #escribir_txt(output, file_name)
    escribir_html(output, file_name)

    #HTML(string=output).write_pdf(pdf_name)

if __name__ == '__main__':
    main()

