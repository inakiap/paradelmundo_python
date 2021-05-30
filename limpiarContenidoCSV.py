import csv
import logging
import re
import os
import shutil
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
    resultado = img
    ruta_local = '/home/inakiap/Projects/backupParadelmundo/'
    ruta_local2 = '/home/inakiap/Imágenes/imgBlogRescatadas'
    if img is not None:
        print(img)
        if "uploads" in img:
            resultado = f'{ruta_local}{img[img.find("uploads"):]}'
        if "ggpht.com" in img:
            resultado = f'{ruta_local2}{img[img.rfind("/"):]}'
    return resultado

def borrar_enlaces(contenido):
    logging.info('borrar_enlaces')
    contenido = clean_links(contenido)
    return contenido

def corregir_tildes(texto):
    palabras = re.findall(r'\w+', texto)
    # for palabra in palabras:
    return texto

def formatear_contenido(texto):
    logging.info('formatear_contenido')
    logging.info(texto)
    #Corregir la dirección de las imágenes
    texto = borrar_enlaces(texto)
    texto = tratar_imagenes(texto)
    logging.info(texto)
    return texto

def generar_marca():
    t = datetime.now()
    return f'{t.year}{t.month}{t.day}{t.hour}{t.minute}{t.second}'

def escribir_csv(filas, archivo):
    logging.info('escribir_csv')
    if archivo is not None:
        with open(archivo, 'w') as r:
            writer = csv.writer(r)
            writer.writerows(filas)

def main():
    #ppal()
    
    ruta = '/media/usb0/Imágenes/'
    buscar_imgs(ruta)

def buscar_imgs(ruta):
    dstpath = '/home/inakiap/Imágenes/imgBlogRescatadas'
    imgs = ['IMG_1176.JPG','DSC08676.JPG','IMG_1179.JPG','IMG_1182.JPG','IMG_1184.JPG','DSC08649.JPG','IMG_1274.JPG','IMG_1335.JPG','IMG_1330.JPG','IMG_1315.JPG','IMG_1266.JPG','IMG_1220.JPG','IMG_1232.JPG','IMG_1271.JPG','IMG_1300.JPG','IMG_1284.JPG','DSC08701.JPG','DSC08697.JPG','IMG_1280.JPG','IMG_1651.JPG','IMG_1168.JPG','IMG_1668.JPG','IMG_1434.JPG','DSC08709.JPG','IMG_1550.JPG','IMG_1577.JPG','IMG_1608.JPG','IMG_1630.JPG','IMG_1657.JPG','DSC08918.JPG','DSC08946.JPG','IMG_1918.JPG','DSC08890.JPG','DSC08893.JPG','DSC08897.JPG','IMG_1790.JPG','IMG_1713.JPG','DSC08866.JPG','IMG_1724.JPG','DSC08904.JPG','IMG_1516.JPG','IMG_1508.JPG','IMG_1797.JPG','autobus%20a%20Badami.JPG','IMG_2174.JPG','IMG_1904.JPG','IMG_1951.JPG','IMG_2057.JPG','IMG_2336.JPG','IMG_2258.JPG','IMG_2295.JPG','IMG_2488.JPG','IMG_2507.JPG','IMG_2492.JPG','IMG_2671.JPG','IMG_2567.JPG','IMG_2409.JPG','IMG_2627.JPG','IMG_2632.JPG','IMG_3031.JPG','IMG_3040.JPG','IMG_3043.JPG','IMG_3046.JPG','IMG_3337.JPG','IMG_3103.JPG','IMG_3094.JPG','IMG_3180.JPG','IMG_3258.JPG','IMG_3295.JPG','IMG_3411.JPG','IMG_3380.JPG','IMG_3452.JPG','IMG_3714.JPG','IMG_3887.JPG','DSC09191.JPG','IMG_4072.JPG','IMG_4058.JPG','IMG_4066.JPG','IMG_4062.JPG','IMG_4385.jpg','NepalSegUnErPapa.jpg','DSC09362.JPG','IMG_4378.JPG','IMG_4346.JPG','IMG_4601.JPG','IMG_4658.JPG','IMG_1635.JPG','IMG_5351.JPG','DSC09503.JPG','DSC09210.JPG','DSC09182.JPG','IMG_3967.JPG','DSC09386.JPG','IMG_4384.jpg','DSC09511.JPG','IMG_5979.JPG','PateadaVuelta.jpg','PateadaIDA.jpg','IMG_5687.JPG','IMG_5908.JPG','IMG_5890.JPG','IMG_5543.JPG','IMG_5688.JPG','IMG_5750.JPG','IMG_5855.JPG','IMG_5900.JPG','IMG_5996.JPG','IMG_6010.JPG','IMG_6142.JPG','IMG_6178.JPG','IMG_6258.JPG','IMG_6315.JPG','IMG_6343.JPG','DSC09622.JPG','DSC09633.JPG','DSC09638.JPG','DSC09646.JPG','IMG_6449.JPG','IMG_6385.JPG','DSC09652.JPG','DSC09656.JPG','IMG_6524.JPG','IMG_6537.JPG','IMG_6545.JPG','IMG_6580.JPG','DSC00011.JPG','IMG_6702.JPG','IMG_6709.JPG','IMG_6575.JPG','DSC00087.JPG','IMG_6907.JPG','IMG_6535.JPG','IMG_6478.JPG','DSC00065.JPG','IMG_7173.JPG','IMG_6957.JPG','DSC00167.JPG','IMG_6931.JPG','DSC00175.JPG','DSC00465.JPG','DSC00432.JPG','DSC00433.JPG','IMG_7740.JPG','IMG_7767.JPG','IMG_7729.JPG','IMG_7796.JPG','IMG_7990.JPG','IMG_8119.JPG','IMG_8198.JPG','DSC00449.JPG','DSC00640.JPG','DSC00645.JPG','IMG_8889.JPG','DSCF0447.JPG','DSC00541.JPG','IMG_8428.JPG','IMG_8550.JPG','IMG_8835.JPG','DSC00646.JPG','IMG_8959.JPG','IMG_8976.JPG','IMG_9046.JPG','IMG_9887.JPG','IMG_0632.JPG','IMG_0791.JPG','IMG_0959.JPG','DSC00718.JPG','IMG_1016.JPG','IMG_1004.JPG','IMG_1034.JPG','IMG_1053.JPG','IMG_1114.JPG','IMG_1271.JPG','IMG_1304.JPG','DSC00216.JPG','TranviaHDR.jpg','img_2024.jpg','salon.jpg','DSC00776.JPG','IMG_2509.jpg','IMG_2507.jpg','IMG_2518.jpg','IMG_2545.jpg']
    print(f'Total imgs {len(imgs)}')
    contador = 0
    contador2 = 0
    dir_path = os.path.dirname(ruta)
    archivos = []
    for root, dirs, files in os.walk(dir_path):
        print(root)
        for file in files: 
            try:
                found = imgs.index(file)
                print (root+'/'+str(file))
                src= root+'/'+str(file)
                dst = dstpath + '/' + str(file)
                contador = contador + 1
                print(f'GOOOOOL {contador}')
                if os.path.isfile(dst):
                    dst = f'{dstpath}/{str(file)}{contador}'
                shutil.copyfile(src, dst)
            except:
                contador2 = contador2 + 1
                print(contador2)

def ppal():
    logging.basicConfig(filename = f'paradelmundo2PDF_{generar_marca()}.log', level=logging.DEBUG)
    logging.info(f'main')
    csv = 'todoslosposts.csv'
    filas = leer_csv(csv)
    for fila in filas:
        fila[5] = formatear_contenido(fila[5])
    file_name = f'contenidos_tratados_{generar_marca()}.csv'
    escribir_csv(filas, file_name)
    # texto = '<p style="text-align: center;"><a href="http://www.paradelmundoquenosbajamos.com/wp-content/uploads/2008/10/img_0889.jpg"><img class="size-medium wp-image-123 aligncenter" title="img_0889" src="http://www.paradelmundoquenosbajamos.com/wp-content/uploads/2008/10/img_0889-300x199.jpg" alt="" width="300" height="199" /></a></p><p style="text-align: justify;">Chennai (antigua MadrAs) no parece una ciudad, es una aglomeraciOn de construcciones, mAs bien bajas, sin orden ni concierto la ciudad.</p>' 
    # texto2 = '<p style="text-align: justify;">Al levantarnos en nuestro primer dIa en la India para evitar atropellar o ser atropellado.</p><p style="text-align: justify;">AquI todos los vehIculos pitan para hacerse notar, es como un "aquI voy, aparta de mi camino!", o mAs bien como un "el que avisa no es traidor". Constantemente hay pitidos, clAxones, rings de todo tipo y a todo volumen.</p><p style="text-align: justify;">El sentido de la circulaciOn  y lo robustos que son, aunque ya avisa la guIa de que la tasa de accidentes...</p>'
    # texto3 = '<p style="text-align: center;"><img class="aligncenter" title="&quot;id&quot;:&quot;VideoPlayback&quot;,&quot;src&quot;:&quot;http://video.google.com/googleplayer.swf?docid=2747122089954335798&amp;hl=en&amp;fs=true&quot;" src="http://www.paradelmundoquenosbajamos.com/wp-includes/js/tinymce/plugins/media/img/trans.gif" alt="" width="100" height="100" /></p>'
    # textos = [texto, texto2, texto3]
    # for texto in textos:
    #     print(texto)

    # print('\n\n')
    # for texto in textos:
    #     texto = cleanhtml(texto)
    #     print(texto)


if __name__ == '__main__':
    main()

