import string
import logging

class lempel_v1:
    def comprimir(self,texto):
        texto_lista  = list(texto)
        diccionario = self.gen_diccionario()
        comprimido = []
        w = ""
        wc = ""
        code = len(diccionario)
        for c in texto_lista:
            wc = w + c
            if wc in diccionario:
                w = wc
            else:
                comprimido.append(diccionario[w])
                #Guardamos la nueva entrada
                diccionario[wc] = code
                code += 1
                #Cambiamos la premisa
                w = c

        #Hemos terminado y sobra algo
        if w:
            comprimido.append(diccionario[w])

        return comprimido


    def descomprimir(self,comprmido):
        diccionario = self.gen_diccionario()
        descomprimido = ""
        w = self.busca_clave(diccionario,comprmido.pop(0))
        descomprimido += w
        code = len(diccionario)
        for c in comprmido:
            contiene = self.busca_clave(diccionario,c)
            if not contiene and c == (len(diccionario)-1):
                contiene = w + w[0]
            elif not contiene and c != (len(diccionario)-1):
                print("ERROR")
                return
            descomprimido += contiene
            #Anadimos al diccionario
            diccionario[w+contiene[0]] = len(diccionario)
            w = contiene

        #Hemos terminado y sobra algo
        return descomprimido

    def busca_clave(self,diccionario = dict(),valor = ""):
        for clave in diccionario.keys():
            if diccionario[clave] == valor:
                return  clave
        return False

    def gen_diccionario(self):
        diccionario = dict()
        code = 0
        for elem in string.printable:
            diccionario[elem] = code
            code += 1

        logging.info("Se ha generado un diccionario con {} elementos".format(code))
        return diccionario

