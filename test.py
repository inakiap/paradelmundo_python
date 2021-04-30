
import csv
from html.parser import HTMLParser
from datetime import datetime

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Etiqueta inicial:", tag)
        for attr in attrs:
            print(">> atributo:", attr)

    def handle_endtag(self, tag):
        print("Etiqueta final  :", tag)

    def handle_data(self, data):
        print(">>>> Contenido:", data)

    def handle_comment(self, data):
        print("Comment  :", data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)

    def handle_decl(self, data):
        print("Decl     :", data)


def leer_csv(archivo):
    
    filas = []

    with open(archivo) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{", ".join(row)}')
                filas.append(row)
                line_count += 1
        print(f'Processed {line_count} lines.')
    return filas

def procesar_contenido(filas):
    return filas

def escribir_archivo(filas, archivo):
    if archivo is not None:
        with open(archivo, 'w') as r:
            for fila in filas:
                r.write(fila)

def nombre_archivo():
    t = datetime.now()
    marca = f'{t.year}{t.month}{t.day}{t.hour}{t.minute}{t.second}'
    return f'{marca}_contenido_entradas_paradelmundo.txt'

def main():
    csv = 'todoslosposts.csv'
    filas = leer_csv(csv)
    filas = procesar_contenido(filas)
    nombre = nombre_archivo()
    escribir_archivo(filas, nombre)


if __name__ == '__main__':
    main()
 