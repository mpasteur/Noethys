#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#------------------------------------------------------------------------
# Application :    Noethys, gestion multi-activit�s
# Site internet :  www.noethys.com
# Auteur:           wolf29f
# Licence:         Licence GNU GPL
#------------------------------------------------------------------------

import os


class DataType(object):
    """
    Classe permetant la conversion facile vers le format souhait� (nombre de caract�res, alignement, d�cimales)
    """

    def __init__(self,type=int,length=1,align="<",precision=2):
        """
        initialise l'objet avec les param�tres souhait�
        """
        self.type = type
        self.length = length
        self.align = align
        self.precision = precision

    def convert(self,data):
        """
        convertis la donn�e fournie dans le format souhait�
        """
        ret_val = ""

        if type(data) is str:                       #s'assure que la donn�e soit bien en unicode
            data=unicode(data.decode("iso-8859-15"))

        if self.type == int:                        #si l'on veux des entier
            if data!="":
                try:                                #on v�rifie qu'il s'agit bien d'un nombre
                    data=int(data)
                except ValueError as e:
                    print("/!\ Erreur de format, impossible de convertir en int /!\\")
                    print(e)
                    data=0
                ret_val = u"{0: {align}0{length}d}".format(data,align=self.align,length=self.length)
            else:
                ret_val = u"{0: {align}0{length}s}".format(data,align=self.align,length=self.length)
        elif self.type == str:                      #si l'on veux des chaines de caract�res
            data = data.replace("\"","")
            ret_val = u"{0: {align}0{length}s}".format(data,align=self.align,length=self.length)
        
        elif self.type == float:                    #si l'on veux un nombre a virgule
            if data!="":
                try:
                    data=float(data)                #on v�rifie qu'il s'agit bien d'un nombre
                except ValueError as e:
                    print("/!\ Erreur de format, impossible de convertir en float /!\\")
                    print(e)
                    data=0
                ret_val = u"{0: {align}0{length}.{precision}f}".format(data,align=self.align,length=self.length,precision=self.precision)
            else:
                ret_val = u"{0: {align}0{length}s}".format(data,align=self.align,length=self.length)

        if len(ret_val)>self.length:                #on tronc si la chaine est trop longue
            ret_val=ret_val[:self.length]
        return ret_val

#d�finition des differents formats souhait� pour les diff�rentes donn�es
# dataTypes = {"num_mvnt":DataType(int,5,">"),
#              "journal":DataType(str,2,"<"),
#              "date_ecriture":DataType(int,8,">"),
#              "date_echeance":DataType(int,8,">"),
#              "num_piece":DataType(str,12,"<"),
#              "compte":DataType(str,11,"<"),
#              "libelle":DataType(str,25,"<"),
#              "montant":DataType(float,13,">"),
#              "isDebit":DataType(str,1,"<"),
#              "numPointage":DataType(str,12,"<"),
#              "code_analyt":DataType(str,6,"<"),
#              "libelle_compte":DataType(str,34,"<"),
#              "devise":DataType(str,1,"<")}

dataTypes = {"num_mvnt":DataType(int,10,">"),
             "journal":DataType(str,6,"<"),
             "date_ecriture":DataType(int,8,">"),
             "date_echeance":DataType(int,8,">"),
             "num_piece":DataType(str,15,"<"),
             "compte":DataType(str,13,"<"),
             "libelle":DataType(str,50,"<"),
             "montant":DataType(float,13,">"),
             "isDebit":DataType(str,1,"<"),
             "numPointage":DataType(str,15,"<"),
             "code_analyt":DataType(str,13,"<"),
             "libelle_compte":DataType(str,35,"<"),
             "devise":DataType(str,1,"<")}


class XImportLine(object):
    """
    D�finie une ligne telle que format� dans un fichier XImport
    """

    def __init__(self,data,dictParametres,num_ligne,typeComptable=None):
        """
        R�cup�re les donn�e utiles fournis en param�tres, les convertis et les enregistre 
        """
        values = dict()         #contient les valeurs fournies et non converties
        self.values = dict()    #contiendra les valeurs convertie

        values["num_mvnt"]=num_ligne #le num�ro de mouvement est le num�ro de la ligne ?           

        values["montant"]=data["montant"] 
        values["devise"]=u"�"

        if "type" in data:                  #on r�cup�re ce qui nous interesse selon le type de donn�e
            
            if data["type"] == "total_prestations":
                values["isDebit"]=u"D"
                values["libelle"]=data["libelle"]
                values["date_ecriture"]=dictParametres["date_fin"].strftime("%Y%m%d")
                values["journal"]=dictParametres["journal_ventes"]
                values["compte"] = dictParametres["code_clients"]   #+
                
                # values["code_analyt"]=dictParametres["code_clients"]  #-

            elif data["type"] == "prestation":
                values["isDebit"]=u"C"
                values["libelle"]=data["intitule"]
                values["compte"] = data["code_compta"]
                values["journal"]=dictParametres["journal_ventes"]
                values["date_ecriture"]=dictParametres["date_fin"].strftime("%Y%m%d")                
                # values["code_analyt"]=data["code_compta"] #-

            elif data["type"] == "depot":
                values["isDebit"]=u"D"
                values["date_ecriture"]=data["date_depot"].strftime("%Y%m%d")
                values["journal"]=dictParametres["journal_%s" % typeComptable]
                values["compte"]=data["code_compta"] #+
                # values["compte"] = data["numeroCompte"] #-
                values["libelle"] = data["libelle"]
                # values["libelle_compte"] = data["nomCompte"] #-
                # values["code_analyt"]=data["code_compta"]    #-

            elif data["type"] == "total_reglements":
                values["isDebit"]=u"C"
                values["date_ecriture"]=dictParametres["date_fin"].strftime("%Y%m%d")
                values["journal"]=dictParametres["journal_%s" % typeComptable]
                values["compte"]=dictParametres["code_clients"]
                values["libelle"] = data["libelle"]
                # values["code_analyt"]=dictParametres["code_clients"] #-

            elif data["type"] == "total_mode":
                values["isDebit"]=u"D"
                values["date_ecriture"]=dictParametres["date_fin"].strftime("%Y%m%d")
                values["journal"]=dictParametres["journal_%s" % typeComptable]
                values["compte"] = data["code_compta"]
                values["libelle"] = data["libelle"]
                values["code_analyt"]=data["code_compta"]

        else:       #Si aucun type n'est renseign�, il y a un probl�me
            raise ValueError("'type' not in data")
        
        for i in dataTypes.keys():  #Convertie toutes les donn�e
            if i in values:         #Si la donn�e a bien �t� fournie, on la converti 
                self.values[i]=dataTypes[i].convert(values[i])
            else:                   #Sinon on remplis de blanc, pour respecter la largeur des colones
                self.values[i]=dataTypes[i].convert("")

    def __getattr__(self,name):
        """
        g�re l'acces aux attributs, pour plus de souplesse, les attributs inconnus renvoient None
        """
        if name in self.values:
            return self.values[name]
        else:
            return None
        


    def __str__(self):
        """
        Renvois la liste des donn�e et leur valeur (appel� lors d'un print ou d'une convertion str)
        """
        return "LigneXImport : \n\t"+\
               "num_mvnt :"+unicode(self.num_mvnt)+"\n\t"+\
               "journal :"+unicode(self.journal)+"\n\t"+\
               "date_ecriture :"+unicode(self.date_ecriture)+"\n\t"+\
               "date_echeance :"+unicode(self.date_echeance)+"\n\t"+\
               "num_piece :"+unicode(self.num_piece)+"\n\t"+\
               "compte :"+unicode(self.compte)+"\n\t"+\
               "libelle :"+unicode(self.libelle)+"\n\t"+\
               "montant :"+unicode(self.montant)+"\n\t"+\
               "isDebit :"+unicode(self.isDebit)+"\n\t"+\
               "numPointage :"+unicode(self.numPointage)+"\n\t"+\
               "code_analyt :"+unicode(self.code_analyt)+"\n\t"+\
               "libelle_compte :"+unicode(self.libelle_compte)+"\n\t"+\
               "devise :"+unicode(self.devise)+"\n"
    
    def getData(self):
        """
        Retourne la ligne telle qu'elle doit �tre enregistr� dans le fichier XImport
        """
        return unicode(self.num_mvnt)+\
                unicode(self.journal)+\
                unicode(self.date_ecriture)+\
                unicode(self.date_echeance)+\
                unicode(self.num_piece)+\
                unicode(self.compte)+\
                unicode(self.libelle)+\
                unicode(self.montant)+\
                unicode(self.isDebit)+\
                unicode(self.numPointage)+\
                unicode(self.code_analyt)+\
                unicode(self.libelle_compte)+\
                unicode(self.devise)

