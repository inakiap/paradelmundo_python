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

def tratar_imagenes(data):
    logging.info('tratar_imagenes')
    contenido = data
    parser = ImgsParser()
    parser.feed(data)
    if len(parser.enlaces) > 0:
        for enlace in parser.enlaces:
            for attr in enlace:
                print(attr)
    if len(parser.imgs) > 0:
        for img in parser.imgs:
            for attr in img:
                if attr[0] == 'src':
                    img_corregida = corregir_img(attr[1])
                    contenido = data.replace(attr[1],img_corregida)
    return contenido

def corregir_img(img):
    logging.info('corregir_img')
    resultado = ''
    ruta_local = '/home/inakiap/Projects/backupParadelmundo/'
    if img is not None:
        if "uploads" in img:
            resultado = f'{ruta_local}{img[img.find("uploads"):]}'
    return resultado

def formatear_entrada(entrada):
    logging.info('formatear_entrada')
    #Corregir la dirección de las imágenes
    entrada.contenido = borrar_enlaces(entrada.contenido)
    entrada.contenido = tratar_imagenes(entrada.contenido)
    #Dar formato HTML a la entrada, crear una página de cada una
    resultado = formato_HTML(entrada)
    return resultado

def borrar_enlaces(contenido):
    logging.info('borrar_enlaces')
    #if contenido is not None:
        # if '<a ' in contenido:
        #     pos_inicial = contenido.find('<a ')
        #     control = True
        #     while control:
        #         if pos_inicial > 0:
        #             logging.debug(f'Enlace posición: {pos_inicial}')
        #             pos_fin = contenido.find('>',pos_inicial)
        #             cadena_a_borrar = contenido[pos_inicial:pos_fin+1]
        #             logging.debug(f'Se borrará: {cadena_a_borrar}')
        #             contenido = contenido.replace(cadena_a_borrar,'')
        #             pos_cierre = contenido.find('</a',pos_fin)
        #             pos_cierre_fin = contenido.find('>',pos_cierre)
        #             cadena_a_borrar = contenido[pos_cierre:pos_cierre_fin+1]
        #             logging.debug(f'Se borrará: {cadena_a_borrar}')
        #             contenido = contenido.replace(cadena_a_borrar,'')
        #             pos_inicial = contenido.find('<a ')
        #         else:
        #             control = False

    return contenido

def formato_HTML(entrada):
    logging.info('formato_HTML')
    entrada_html = div(cls='col-md-12', id=f'entrada_{entrada.id}')
    with entrada_html:
        footer  = entrada_html.add(div(id='comentarios'))
        if len(entrada.comentarios) > 0:
            comentario_html = footer.add(div(id='comentario'))
            for comentario in entrada.comentarios:
                comentario_html.add(h5(comentario.autor_comentario))
                comentario_html.add(p(comentario.fecha_comentario))
                comentario_html.add(p(comentario.contenido_comentario))
        div(raw(entrada.contenido),id='contenido')
        
        descrip = address()
        descrip.add(strong(entrada.autor))
        descrip.add(br())
        descrip.add(raw(f'Fecha: {entrada.fecha} Último cambio: {entrada.ultimo_cambio}'))
        header = div(id='header')
        header.add(h3(entrada.titulo))
        header.add(descrip)
        
        
        
    #return f'{entrada.id} {entrada.titulo} {entrada.autor} {entrada.fecha} {entrada.ultimo_cambio} {entrada.numero_comentarios} \n   {entrada.contenido}\n'
    return f'{entrada_html}\n'

def formato_final(entradas):
    logging.info('formato_final')
    doc = document(title='Paradelmundoquenosbajamos')
    with doc.head:
        link(rel='stylesheet', href='css/style.css')
        link(rel='stylesheet', href='css/bootstrap.min.css')
        meta(charset='utf-8')
        meta(name='viewport', content='width=device-width, initial-scale=1')
    with doc:
        if entradas is not None:
            with div(cls='container-fluid'):
                for entrada in entradas:
                    with div(cls='row'):
                        entrada_formateada = formato_HTML(entrada)
                        raw(entrada_formateada)
        
    return doc.render()

def generar_marca():
    t = datetime.now()
    return f'{t.year}{t.month}{t.day}{t.hour}{t.minute}{t.second}'

def escribir_txt(entradas, archivo):
    logging.info('escribir_txt')
    if archivo is not None:
        with open(archivo, 'w') as r:
            for entrada in entradas:
                # linea = formatear_entrada(entrada)
                # r.write(linea)
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
    csv = 'todoslosposts.csv'
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

