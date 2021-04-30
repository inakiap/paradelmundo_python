class Entrada:
    # id = 0
    # autor = ''
    # fecha = ''
    # ultimo_cambio = ''
    # titulo = ''
    # contenido = ''
    # categorias = ''
    # etiquetas = ''
    # num_comentarios = 0
    # comentarios = []

    def __init__(self, id, autor, fecha, ultimo_cambio, titulo, contenido, categorias, etiquetas, num_comentarios, comentarios):
        self.id = id
        self.titulo = titulo
        self.fecha = fecha
        self.ultimo_cambio = ultimo_cambio
        self.autor = autor
        self.contenido = contenido
        self.categorias = categorias
        self.etiquetas = etiquetas
        self.num_comentarios = num_comentarios
        self.comentarios = comentarios

    def __str__(self):
        return '%s, %s, %s, %s, %s, %s' % (self.id, self.titulo, self.autor, self.fecha, self.ultimo_cambio, self.num_comentarios)

class Comentario:
    # estado = ''
    # fecha_comentario = ''
    # autor_comentario = ''
    # email = ''
    # contenido_comentario = ''
    
    def __init__(self, estado, fecha_comentario, autor_comentario, email, contenido_comentario):
        self.estado = estado
        self.fecha_comentario = fecha_comentario
        self.autor_comentario = autor_comentario
        self.email = email
        self.contenido_comentario = contenido_comentario
    
    def __str__(self):
        return '%d, %d, %d, %d, %d' % (self.autor_comentario, self.fecha_comentario, self.email, self.estado, self.contenido_comentario)
