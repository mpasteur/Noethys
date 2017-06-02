#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#------------------------------------------------------------------------
# Application :    Noethys, gestion multi-activit�s
# Site internet :  www.noethys.com
# Auteur:           Ivan LUCAS
# Copyright:       (c) 2010-15 Ivan LUCAS
# Licence:         Licence GNU GPL
#------------------------------------------------------------------------


import Chemins
from Utils.UTILS_Traduction import _
import wx
import GestionDB
from Utils import UTILS_Dates
from Utils.UTILS_Decimal import FloatToDecimal as FloatToDecimal
import datetime
from Utils import UTILS_Config
SYMBOLE = UTILS_Config.GetParametre("monnaie_symbole", u"�")


from Utils import UTILS_Interface
from ObjectListView import FastObjectListView, ColumnDefn, Filter, CTRL_Outils, PanelAvecFooter

  
class Track(object):
    def __init__(self, index=0, label="", valeur=""):
        self.index = index
        self.label = label
        self.valeur = valeur


# ----------------------------------------------------------------------------------------------------------------------------------------

class ListView(FastObjectListView):
    def __init__(self, *args, **kwds):
        # R�cup�ration des param�tres perso
        self.clsbase = kwds.pop("clsbase", None)
        self.selectionID = None
        self.selectionTrack = None
        self.criteres = ""
        self.itemSelected = False
        self.popupIndex = -1
        self.listeFiltres = []
        # Initialisation du listCtrl
        FastObjectListView.__init__(self, *args, **kwds)
        # Binds perso
        self.Bind(wx.EVT_CONTEXT_MENU, self.OnContextMenu)
        self.donnees = []
        self.listeDonnees = []
        self.InitObjectListView()

    def InitObjectListView(self):
        # Couleur en alternance des lignes
        self.oddRowsBackColor = UTILS_Interface.GetValeur("couleur_tres_claire", wx.Colour(240, 251, 237))
        self.evenRowsBackColor = wx.Colour(255, 255, 255)
        self.useExpansionColumn = True

        liste_Colonnes = [
            ColumnDefn(_(u""), "left", 0, "index", typeDonnee="texte"),
            ColumnDefn(_(u"Label"), "left", 100, "label", typeDonnee="texte", isSpaceFilling=True),
            ColumnDefn(_(u"Valeur"), 'center', 140, "valeur", typeDonnee="texte"),
            ]
        
        self.SetColumns(liste_Colonnes)
        self.SetEmptyListMsg(_(u"Aucune donn�e"))
        self.SetEmptyListMsgFont(wx.FFont(11, wx.DEFAULT, False, "Tekton"))
        self.SetSortColumn(0)
        
    def MAJ(self):
        listeDonnees = [
            {"label" : _(u"Nombre de jours pr�vus"), "code" : "nbre_dates", "format" : "entier", "suffixe" : _(u"jours"), "defaut" : 0},
            {"label" : _(u"Nombre de semaines pr�vues"), "code" : "nbre_semaines", "format" : "entier", "suffixe" : _(u"semaines"), "defaut" : 0},
            {"label" : _(u"Nombre de mois pr�vus"), "code" : "nbre_mois", "format" : "entier", "suffixe" : _(u"mois"), "defaut" : 0},
            {"label" : _(u"Nombre moyen d'heures pr�vues par jour"), "code" : "moy_heures_jour", "format" : "duree", "suffixe" : _(u""), "defaut" : datetime.timedelta(0)},
            {"label" : _(u"Nombre moyen d'heures pr�vues par semaine"), "code" : "moy_heures_semaine", "format" : "duree", "suffixe" : _(u""), "defaut" : datetime.timedelta(0)},
            {"label" : _(u"Nombre moyen d'heures pr�vues par mois"), "code" : "moy_heures_mois", "format" : "duree", "suffixe" : _(u""), "defaut" : datetime.timedelta(0)},
            {"label" : _(u"Nombre d'heures pr�vues arrondies"), "code" : "duree_heures_brut", "format" : "duree", "suffixe" : _(u""), "defaut" : datetime.timedelta(0)},
            {"label" : _(u"Nombre d'heures RTT pr�vues"), "code" : "duree_absences_prevues", "format" : "duree", "suffixe" : _(u""), "defaut" : datetime.timedelta(0)},
            {"label" : _(u"Nombre d'heures RTT prises"), "code" : "duree_absences_prises", "format" : "duree", "suffixe" : _(u""), "defaut" : datetime.timedelta(0)},
            {"label" : _(u"Nombre d'heures RTT restantes"), "code" : "duree_absences_solde", "format" : "duree", "suffixe" : _(u""), "defaut" : datetime.timedelta(0)},
            {"label" : _(u"Nombre d'heures de r�gularisation"), "code" : "duree_heures_regularisation", "format" : "duree", "suffixe" : _(u""), "defaut" : datetime.timedelta(0)},
            {"label" : _(u"Nombre total d'heures factur�es"), "code" : "duree_heures_contrat", "format" : "duree", "suffixe" : _(u""), "defaut" : datetime.timedelta(0)},
            {"label" : _(u"Heures factur�es chaque mois"), "code" : "forfait_horaire_mensuel", "format" : "duree", "suffixe" : _(u""), "defaut" : datetime.timedelta(0)},
            {"label" : _(u"Heures factur�es le dernier mois"), "code" : "forfait_horaire_dernier_mois", "format" : "duree", "suffixe" : _(u""), "defaut" : datetime.timedelta(0)},
            {"label" : _(u"Nombre de mensualit�s"), "code" : "nbre_mensualites", "format" : "entier", "suffixe" : _(u"mensualit�s"), "defaut" : 0},
            {"label" : _(u"Montant total factur�"), "code" : "total_mensualites", "format" : "montant", "suffixe" : "", "defaut" : FloatToDecimal(0.0)},
        ]

        self.donnees = []
        index = 0
        for dictDonnee in listeDonnees :
            valeur = self.clsbase.GetValeur(dictDonnee["code"], dictDonnee["defaut"])
            if dictDonnee["format"] == "montant" :
                valeur = u"%.2f %s" % (valeur, SYMBOLE)
            if dictDonnee["format"] == "entier" :
                valeur = u"%d" % valeur
            if dictDonnee["format"] == "decimal" :
                valeur = u"%.2f" % valeur
            if dictDonnee["format"] == "duree" :
                valeur = UTILS_Dates.DeltaEnStr(valeur)
            if dictDonnee.has_key("suffixe") and dictDonnee["suffixe"] != "" :
                valeur += " " + dictDonnee["suffixe"]
            self.donnees.append(Track(index, dictDonnee["label"], valeur))
            index += 1

        self.SetObjects(self.donnees)
        self._ResizeSpaceFillingColumns() 

    def GetTracks(self):
        return self.GetObjects()

    def Selection(self):
        return self.GetSelectedObjects()

    def OnContextMenu(self, event):
        """Ouverture du menu contextuel """        
        # Cr�ation du menu contextuel
        menuPop = wx.Menu()

        if len(self.Selection()) == 0:
            noSelection = True
        else:
            noSelection = False
                
        # Cr�ation du menu contextuel
        menuPop = wx.Menu()

        # Item Apercu avant impression
        item = wx.MenuItem(menuPop, 40, _(u"Aper�u avant impression"))
        bmp = wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Apercu.png"), wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Apercu, id=40)
        
        # Item Imprimer
        item = wx.MenuItem(menuPop, 50, _(u"Imprimer"))
        bmp = wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Imprimante.png"), wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.Imprimer, id=50)
        
        menuPop.AppendSeparator()
    
        # Item Export Texte
        item = wx.MenuItem(menuPop, 600, _(u"Exporter au format Texte"))
        bmp = wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Texte2.png"), wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.ExportTexte, id=600)
        
        # Item Export Excel
        item = wx.MenuItem(menuPop, 700, _(u"Exporter au format Excel"))
        bmp = wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Excel.png"), wx.BITMAP_TYPE_PNG)
        item.SetBitmap(bmp)
        menuPop.AppendItem(item)
        self.Bind(wx.EVT_MENU, self.ExportExcel, id=700)

        self.PopupMenu(menuPop)
        menuPop.Destroy()
            
    def Apercu(self, event):
        from Utils import UTILS_Printer
        prt = UTILS_Printer.ObjectListViewPrinter(self, titre=_(u"R�capitulatif des donn�es du contrat"), format="A", orientation=wx.PORTRAIT)
        prt.Preview()

    def Imprimer(self, event):
        from Utils import UTILS_Printer
        prt = UTILS_Printer.ObjectListViewPrinter(self, titre=_(u"R�capitulatif des donn�es du contrat"), format="A", orientation=wx.PORTRAIT)
        prt.Print()

    def ExportTexte(self, event):
        from Utils import UTILS_Export
        UTILS_Export.ExportTexte(self, titre=_(u"R�capitulatif des donn�es du contrat"), autoriseSelections=False)
        
    def ExportExcel(self, event):
        from Utils import UTILS_Export
        UTILS_Export.ExportExcel(self, titre=_(u"R�capitulatif des donn�es du contrat"), autoriseSelections=False)


# -------------------------------------------------------------------------------------------------------------------------------------------


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        panel = wx.Panel(self, -1, name="test1")
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(panel, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer_1)
        
        ctrl = ListviewAvecFooter(panel, kwargs={})
        listview = ctrl.GetListview()
        listview.MAJ() 
        
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(ctrl, 1, wx.ALL|wx.EXPAND, 10)
        panel.SetSizer(sizer_2)
        self.Layout()
        self.SetSize((800, 400))

if __name__ == '__main__':
    app = wx.App(0)
    #wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "OL TEST")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
