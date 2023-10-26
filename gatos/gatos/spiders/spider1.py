import scrapy


class Spider1Spider(scrapy.Spider):
    name = "spider1"
    allowed_domains = ["es.wikipedia.org"]
    start_urls = ["https://es.wikipedia.org/wiki/Anexo:Razas_de_gatos"]

    # Nombre de archivo
    contador_txt = 1
    enlaces = []
    enlacesNuevos = []
    
    def parse(self, response):
        ''' Función para parsear una página '''
        # Obtener el texto de todas las etiquetas <p>
        contenido_div = response.css('div#mw-content-text')
        parrafos =  contenido_div.css('p::text, b::text, a::text').getall()
        # Obtener enlaces
        self.enlaces = response.css('div#mw-content-text a::attr(href)').getall()
        
        # Imprimir o guardar los párrafos según tus necesidades
        for parrafo in parrafos:
            print(parrafo)
        
        contador_formato = str(self.contador_txt).zfill(2)

        # Guardar pagina principal en un archivo
        nombre_txt = 'Doc' + contador_formato + '.txt'
        
        with open(nombre_txt, 'w', encoding='utf-8') as archivo:
            for parrafo in parrafos:
                archivo.write(parrafo + ' ')
        self.contador_txt += 1
        
        # # Guardar enlaces en un archivo
        # with open('Enlaces.txt', 'w', encoding='utf-8') as archivo:
        #     for enlace in self.enlaces:
        #         archivo.write(enlace + '\n')
        input()         
        
        # Crawling profundo
        for _ in range(0, 1):
            # Sigue enlaces a n páginas
            for enlace in self.enlaces:
                yield response.follow(enlace, self.parse_pagina)
                
            self.enlaces = self.enlacesNuevos
            self.enlacesNuevos = []
            
                
    # Función para parsear una página
    def parse_pagina(self, response):        
        # Obtener el texto de todas las etiquetas <p>
        parrafos = response.css('p::text, b::text, a::text').getall()
        # Obtener enlaces
        enlaces = response.css('a::attr(href)').getall()

        # Imprimir o guardar los párrafos según tus necesidades
        for parrafo in parrafos:
            print(parrafo)
        
        contador_formato = str(self.contador_txt).zfill(2)

        nombre_txt = 'Doc' + contador_formato + '.txt'
        
        # Guardar los párrafos en un archivo
        with open(nombre_txt, 'w', encoding='utf-8') as archivo:
            for parrafo in parrafos:
                archivo.write(parrafo + ' ')
        
        # Concatenar enlaces
        self.enlacesNuevos += enlaces
        # Incrementamos contador de txt
        self.contador_txt += 1