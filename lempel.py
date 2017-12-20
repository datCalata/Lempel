import string
import logging
import copy

class lempel_v1:

    _FINDICCIONARIO = "---\n"
    _comprimido = 0
    _custom_diccionario = 0
    _CAMBIOLINEA = "CAMBIOLINEA"
    _ESPACIOBLANCO = "ESPACIOBLANCO"
    _COMILLASIMPLE = "COMILLASIMPLE"
    
    def comprimir(self,texto,custom_diccionario = None):
        texto_lista  = list(texto)
        if custom_diccionario == None:
            diccionario = self.gen_diccionario_ascii()
        else:
            diccionario = copy.copy(custom_diccionario)
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

        self._comprimido = comprimido
        if not custom_diccionario == None:
            self._custom_diccionario = diccionario 
        return comprimido


    def descomprimir(self,comprmido,custom_diccionario = None):
        if custom_diccionario == None:
            diccionario = self.gen_diccionario_ascii()
        else:
            diccionario = copy.copy(custom_diccionario)
        descomprimido = ""
        w = self.busca_clave(diccionario,comprmido.pop(0))
        descomprimido += w
        code = len(diccionario)
        for c in comprmido:
            contiene = self.busca_clave(diccionario,c)
            if not contiene and c == (len(diccionario)):
                contiene = w + w[0]
            elif not contiene and c != (len(diccionario)):
                print("ERROR")
                return
            descomprimido += contiene
            #Anadimos al diccionario
            diccionario[w+contiene[0]] = len(diccionario)
            w = contiene
            #print(descomprimido)

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
        return diccionario

    def gen_diccionario_ascii(self):
        diccionario = dict()
        code = 0
        for i in range(256):
            diccionario[chr(i)] = i
        return diccionario

    def scan_for_diccionario(self,ruta):
        fich = open(ruta,"r")
        lineas =  fich.readlines()
        contador = 0
        diccionario = dict()
        for linea in lineas:
            for caracter in linea:
                if not caracter in diccionario:
                    diccionario[caracter] = contador
                    contador += 1
        return diccionario


    def gen_file(self, ruta, diccionario):
        fich = open(ruta,"w")
        lineatxt = ""
        for clave in diccionario.keys():
            if clave == "\n":
                fich.writelines("'{}' {}\n".format(self._CAMBIOLINEA,diccionario[clave]))
                continue
            if clave == " ":
                fich.writelines("'{}' {}\n".format(self._ESPACIOBLANCO,diccionario[clave]))
                continue
            if clave == "'":
                fich.writelines("'{}' {}\n".format(self._COMILLASIMPLE,diccionario[clave]))
                continue
            fich.writelines("'{}' {}\n".format(clave,diccionario[clave]))
        fich.writelines(self._FINDICCIONARIO)
        for elm in self._comprimido:
            lineatxt += "{} ".format(elm)
        fich.writelines(lineatxt)
        fich.close()

    def read_file(self, ruta):
        fich = open(ruta,"r")
        texto = fich.readlines()
        diccionario = dict()
        comprimido = []
        fin_diccionario = False
        for elm in texto:
            if not fin_diccionario:
                if elm == self._FINDICCIONARIO:
                    fin_diccionario = True
                    continue
                tmp = self.process_line_diccionario(elm)
                diccionario[tmp[0]]  = int(tmp[1])
                continue
            comprimido = elm.split()
        comprimido = [int(i) for i in comprimido]
        self._custom_diccionario = diccionario
        return [comprimido,diccionario]
        
    def process_line_diccionario(self, line):
        elms = line.split()
        print(elms)
        caracter = elms[0].split("'")[1]
        if caracter == self._CAMBIOLINEA:
            caracter = "\n"
        if caracter == self._ESPACIOBLANCO:
            caracter = " "
        if caracter == self._COMILLASIMPLE:
            caracter = "'"
        num = elms[1]
        return [caracter,num]



lempel = lempel_v1()
custom_diccionario = lempel.scan_for_diccionario("ascii.txt")
fich = open("ascii.txt","r")
#print(fich.read())
print(custom_diccionario)
comprimido = lempel.comprimir(fich.read(),custom_diccionario)
#print(comprimido)
lempel.gen_file("fich.txt",custom_diccionario)
elm = lempel.read_file("fich.txt")
#print(elm[1])
#print(custom_diccionario)
#print(str(len(custom_diccionario))+" "+str(len(elm[1])))
#print(type(elm[0].pop(0))
descomprimir = lempel.descomprimir(elm[0],elm[1])
#print(custom_diccionario)
#descomprimir2 = lempel.descomprimir(comprimido,custom_diccionario) 
fich = open("descomprimido.txt","w")
fich.write(descomprimir)

