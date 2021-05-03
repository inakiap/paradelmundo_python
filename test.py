
import csv
from html.parser import HTMLParser
from datetime import datetime

class Imagen:
    def __init__(self, attrs):
        self.attrs = attrs

class ImgsParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.imgs = []

  def handle_starttag(self, tag, attributes):
    if tag != 'img':
        return
    self.imgs.append(Imagen(attributes))

  def handle_endtag(self, tag):
      pass
    # if tag == 'div' and self.recording:
    #   self.recording -= 1

  def handle_data(self, data):
      pass
    # if self.recording:
    #   self.data.append(data)

# class MyHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         print("Etiqueta inicial:", tag)
#         if tag != 'img':
#             return
#         attr = dict(attrs)
#         imgs.append(attr)

#     def handle_endtag(self, tag):
#         print("Etiqueta final  :", tag)
#         self.tags.append(tag)

#     def handle_data(self, data):
#         print(">>>> Contenido:", data)
#         self.datas.append(data)

#     def handle_comment(self, data):
#         print("Comment  :", data)
#         self.comments.append(data)

#     def handle_entityref(self, name):
#         c = chr(name2codepoint[name])
#         print("Named ent:", c)

#     def handle_charref(self, name):
#         if name.startswith('x'):
#             c = chr(int(name[1:], 16))
#         else:
#             c = chr(int(name))
#         print("Num ent  :", c)

#     def handle_decl(self, data):
#         print("Decl     :", data)


def leer_csv(archivo):
    
    filas = []

    with open(archivo) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                # print(f'\t{", ".join(row)}')
                filas.append(row)
                line_count += 1
        # print(f'Processed {line_count} lines.')
    return filas

def procesar_contenido(filas):
    parser = ImgsParser()
    result = []    
    for fila in filas:
        parser.feed(fila[5])
        
        for img in parser.imgs:
            for attr in img.attrs:
                if attr[0] == 'src':
                    if attr[1] not in result:
                        result.append(attr[1]) 
                        print(attr)

    return result

def escribir_archivo(filas, archivo):
    if archivo is not None:
        with open(archivo, 'w') as r:
            for fila in filas:
                r.write(f'{fila}\n')

def nombre_archivo():
    t = datetime.now()
    marca = f'{t.year}{t.month}{t.day}{t.hour}{t.minute}{t.second}'
    return f'{marca}_imgenes_paradelmundo.txt'

def main():
    csv = 'todoslosposts.csv'
    filas = leer_csv(csv)
    filas = procesar_contenido(filas)
    nombre = nombre_archivo()
    escribir_archivo(filas, nombre)


if __name__ == '__main__':
    main()
 