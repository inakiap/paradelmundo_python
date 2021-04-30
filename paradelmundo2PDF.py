import csv
import html
import logging
from html.parser import HTMLParser
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

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Etiqueta inicial:", tag)
        logging.debug(f'starttag {tag}')
        for attr in attrs:
            print(">> atributo:", attr)
            logging.debug(f'attr {attr}')
        return tag, attrs

    def handle_endtag(self, tag):
        print("Etiqueta final  :", tag)
        logging.debug(f'endtag {tag}')
        return tag

    def handle_data(self, data):
        print(">>>> Contenido:", data)
        logging.debug(f'data {data}')
        return data

    def handle_comment(self, data):
        print("Comment  :", data)
        logging.debug(f'comment {data}')
        return data

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)
        logging.debug(f'entityref {c}')
        return c

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)
        logging.debug(f'charref {c}')

    def handle_decl(self, data):
        print("Decl     :", data)
        logging.debug(f'decl {data}')

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
    parser = MyHTMLParser()
    parser.feed(contenido)
    #print(f'[{contenido}]')
    return contenido

def formatear_entrada(entrada):
    contenido = tratar_imagenes(entrada.contenido)
    return f'{entrada.id} {entrada.titulo} {entrada.autor} {entrada.fecha} {entrada.ultimo_cambio} {entrada.numero_comentarios} \n      {contenido}\n'

def generar_marca():
    t = datetime.now()
    return f'{t.year}{t.month}{t.day}{t.hour}{t.minute}{t.second}'

def escribir_archivo(entradas, archivo):
    if archivo is not None:
        with open(archivo, 'w') as r:
            for entrada in entradas:
                linea = formatear_entrada(entrada)
                r.write(linea)

def main():
    logging.basicConfig(filename = f'paradelmundo2PDF_{generar_marca()}.log', level=logging.DEBUG)
    logging.info(f'main')
    csv = 'todoslosposts.csv'
    filas = leer_csv(csv)
    libro_bruto = csv_en_entradas(filas)
    for entrada in libro_bruto:
        print(entrada)
    escribir_archivo(libro_bruto, f'resumenPDF_{generar_marca()}.txt')
        

if __name__ == '__main__':
    main()

