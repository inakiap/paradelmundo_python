import csv
import html
import logging
from html.parser import HTMLParser
from datetime import datetime
from dominate import document
from dominate.tags import *
from dominate.util import raw
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
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

  def handle_starttag(self, tag, attributes):
    if tag == 'img':
        self.imgs.append(attributes)
    elif tag == 'a':
        self.enlaces.append(attributes)
    else:
        return

  def handle_endtag(self, tag):
      pass
    # if tag == 'div' and self.recording:
    #   self.recording -= 1

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
    entradas.append(Entrada(fila[0],fila[1],fila[2],fila[3],fila[4],fila[5],fila[6],fila[7],fila[8],comentarios))
    comentarios = []
    linea = f'Entrada [{fila[0]}] [{fila[3]}] {fila[4]} de {fila[1]}'
    print(linea)
    logging.debug(linea)
    return entradas, comentarios 

def generar_marca():
    t = datetime.now()
    return f'{t.year}{t.month}{t.day}{t.hour}{t.minute}{t.second}'

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

def main():
    logging.basicConfig(filename = f'paradelmundo2PDF_{generar_marca()}.log', level=logging.DEBUG)
    logging.info(f'main')
    # csv = 'todoslosposts.csv'
    csv = 'seleccion_contenidos_tratados.csv'
    filas = leer_csv(csv)
    libro_bruto = csv_en_entradas(filas)
    #libro_final = formato_final(libro_bruto)
    #for entrada in libro_final:
    #    print(entrada)
    # escribir_txt(libro_final, f'resumenPDF_{generar_marca()}.html')
    #escribir_html(libro_final, f'resumenPDF_{generar_marca()}.html')
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('showentradas.txt')
    output = template.render(entradas=libro_bruto)
    #print(output)
    file_name = f'testTXT_{generar_marca()}.html'
    escribir_txt(output, file_name)
    #escribir_html(output, file_name)

    #HTML(string=output).write_pdf(pdf_name)

if __name__ == '__main__':
    main()

