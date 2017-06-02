#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#------------------------------------------------------------------------
# Application :    Noethys, gestion multi-activit�s
# Site internet :  www.noethys.com
# Auteur:           Ivan LUCAS
# Copyright:       (c) 2010-11 Ivan LUCAS
# Licence:         Licence GNU GPL
#------------------------------------------------------------------------


import Chemins
from Utils.UTILS_Traduction import _
import wx
from Ctrl import CTRL_Bouton_image
import datetime

import GestionDB
from Ctrl import CTRL_Bandeau
from Ol import OL_Liste_quotients
from Ctrl import CTRL_Saisie_date
import DLG_calendrier_simple
from Ctrl import CTRL_Selection_activites
from Utils import UTILS_Dates



class CTRL_Type_quotient(wx.Choice):
    def __init__(self, parent):
        wx.Choice.__init__(self, parent, -1, size=(150, -1))
        self.parent = parent
        self.MAJ()
        self.Select(0)

    def MAJ(self):
        listeItems = self.GetListeDonnees()
        if len(listeItems) == 0 :
            self.Enable(False)
        else :
            self.Enable(True)
        self.SetItems(listeItems)

    def GetListeDonnees(self):
        db = GestionDB.DB()
        req = """SELECT IDtype_quotient, nom
        FROM types_quotients
        ORDER BY nom;"""
        db.ExecuterReq(req)
        listeDonnees = db.ResultatReq()
        db.Close()
        listeItems = []
        self.dictDonnees = {}
        index = 0
        for IDtype_quotient, nom in listeDonnees :
            self.dictDonnees[index] = { "ID" : IDtype_quotient, "nom " : nom}
            listeItems.append(nom)
            index += 1
        return listeItems

    def SetID(self, ID=0):
        if ID == None :
            self.SetSelection(0)
        for index, values in self.dictDonnees.iteritems():
            if values["ID"] == ID :
                 self.SetSelection(index)

    def GetID(self):
        index = self.GetSelection()
        if index == -1 : return None
        return self.dictDonnees[index]["ID"]



class Options(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=-1, name="panel_presents", style=wx.TAB_TRAVERSAL)
        self.parent = parent

        self.label_date = wx.StaticText(self, -1, _(u"Date de situation :"))
        self.ctrl_date = CTRL_Saisie_date.Date(self)
        self.ctrl_date.SetDate(datetime.date.today())
        self.bouton_date = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath(u"Images/16x16/Calendrier.png"), wx.BITMAP_TYPE_ANY))

        self.radio_toutes = wx.RadioButton(self, -1, _(u"Toutes les familles"), style=wx.RB_GROUP)
        self.radio_avec = wx.RadioButton(self, -1, _(u"Uniquement familles avec QF"))
        self.radio_sans = wx.RadioButton(self, -1, _(u"Uniquement familles sans QF"))
        
        self.radio_inscrits = wx.RadioButton(self, -1, _(u"Tous les inscrits"), style=wx.RB_GROUP)
        self.radio_presents = wx.RadioButton(self, -1, _(u"Uniquement les pr�sents"))
        self.label_date_debut = wx.StaticText(self, -1, u"Du")
        self.ctrl_date_debut = CTRL_Saisie_date.Date(self)
        self.bouton_date_debut = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Calendrier.png"), wx.BITMAP_TYPE_ANY))
        self.label_date_fin = wx.StaticText(self, -1, _(u"Au"))
        self.ctrl_date_fin = CTRL_Saisie_date.Date(self)
        self.bouton_date_fin = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Calendrier.png"), wx.BITMAP_TYPE_ANY))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnBoutonDate, self.bouton_date)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, self.radio_inscrits)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio, self.radio_presents)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonDateDebut, self.bouton_date_debut)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonDateFin, self.bouton_date_fin)
        
        self.OnRadio(None)

    def __set_properties(self):
        self.ctrl_date.SetToolTip(wx.ToolTip(_(u"Saisissez la date de situation")))
        self.bouton_date.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour s�lectionner la date de situation dans un calendrier")))
        self.ctrl_date_debut.SetToolTip(wx.ToolTip(_(u"Saisissez ici une date de d�but")))
        self.bouton_date_debut.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour saisir une date de d�but")))
        self.ctrl_date_fin.SetToolTip(wx.ToolTip(_(u"Saisissez ici une date de fin")))
        self.bouton_date_fin.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour saisir une date de fin")))

    def __do_layout(self):
        grid_sizer_base = wx.FlexGridSizer(rows=9, cols=1, vgap=5, hgap=5)

        # Date de r�f�rence
        grid_sizer_periode = wx.FlexGridSizer(rows=1, cols=3, vgap=5, hgap=5)
        grid_sizer_periode.Add(self.label_date, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_periode.Add(self.ctrl_date, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_periode.Add(self.bouton_date, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_base.Add(grid_sizer_periode, 1, wx.RIGHT|wx.EXPAND, 5)
        grid_sizer_base.Add( (5, 5), 0, 0, 0)

        grid_sizer_base.Add(self.radio_toutes, 0, 0, 0)
        grid_sizer_base.Add(self.radio_avec, 0, 0, 0)
        grid_sizer_base.Add(self.radio_sans, 0, 0, 0)
        grid_sizer_base.Add( (5, 5), 0, 0, 0)
        
        grid_sizer_base.Add(self.radio_inscrits, 0, 0, 0)
        grid_sizer_base.Add(self.radio_presents, 0, 0, 0)
        
        grid_sizer_dates = wx.FlexGridSizer(rows=2, cols=3, vgap=5, hgap=5)
        grid_sizer_dates.Add(self.label_date_debut, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_dates.Add(self.ctrl_date_debut, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_dates.Add(self.bouton_date_debut, 0, 0, 0)
        grid_sizer_dates.Add(self.label_date_fin, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_dates.Add(self.ctrl_date_fin, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        grid_sizer_dates.Add(self.bouton_date_fin, 0, 0, 0)
        grid_sizer_base.Add(grid_sizer_dates, 1, wx.LEFT|wx.EXPAND, 18)
        
        self.SetSizer(grid_sizer_base)
        grid_sizer_base.Fit(self)
        grid_sizer_base.AddGrowableCol(0)

    def OnBoutonDate(self, event):
        dlg = DLG_calendrier_simple.Dialog(self)
        if dlg.ShowModal() == wx.ID_OK :
            date = dlg.GetDate()
            self.ctrl_date.SetDate(date)
        dlg.Destroy()

    def OnRadio(self, event): 
        if self.radio_inscrits.GetValue() == True :
            etat = False
        else:
            etat = True
        self.label_date_debut.Enable(etat)
        self.label_date_fin.Enable(etat)
        self.ctrl_date_debut.Enable(etat)
        self.ctrl_date_fin.Enable(etat)
        self.bouton_date_debut.Enable(etat)
        self.bouton_date_fin.Enable(etat)

    def OnBoutonDateDebut(self, event): 
        dlg = DLG_calendrier_simple.Dialog(self)
        if dlg.ShowModal() == wx.ID_OK :
            date = dlg.GetDate()
            self.ctrl_date_debut.SetDate(date)
        dlg.Destroy()

    def OnBoutonDateFin(self, event): 
        dlg = DLG_calendrier_simple.Dialog(self)
        if dlg.ShowModal() == wx.ID_OK :
            date = dlg.GetDate()
            self.ctrl_date_fin.SetDate(date)
        dlg.Destroy()
    
    def GetFamilles(self):
        if self.radio_toutes.GetValue() : return "TOUTES"
        if self.radio_avec.GetValue() : return "AVEC"
        if self.radio_sans.GetValue() : return "SANS"
    
    def GetPresents(self):
        if self.radio_inscrits.GetValue() == True :
            # Tous les inscrits
            return None
        else:
            # Uniquement les pr�sents
            date_debut = self.ctrl_date_debut.GetDate()
            if self.ctrl_date_debut.FonctionValiderDate() == False or date_debut == None :
                dlg = wx.MessageDialog(self, _(u"La date de d�but ne semble pas valide !"), _(u"Erreur de saisie"), wx.OK | wx.ICON_EXCLAMATION)
                dlg.ShowModal()
                dlg.Destroy()
                self.ctrl_date_debut.SetFocus()
                return False
            
            date_fin = self.ctrl_date_fin.GetDate()
            if self.ctrl_date_fin.FonctionValiderDate() == False or date_fin == None :
                dlg = wx.MessageDialog(self, _(u"La date de fin ne semble pas valide !"), _(u"Erreur de saisie"), wx.OK | wx.ICON_EXCLAMATION)
                dlg.ShowModal()
                dlg.Destroy()
                self.ctrl_date_fin.SetFocus()
                return False
            
            if date_debut > date_fin :
                dlg = wx.MessageDialog(self, _(u"La date de d�but est sup�rieure � la date de fin !"), _(u"Erreur de saisie"), wx.OK | wx.ICON_EXCLAMATION)
                dlg.ShowModal()
                dlg.Destroy()
                self.ctrl_date_fin.SetFocus()
                return False
            
            return (date_debut, date_fin)

# -------------------------------------------------------------------------------------------------------------------------

class Parametres(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=-1, name="panel_parametres", style=wx.TAB_TRAVERSAL)
        self.parent = parent
        
        # Type de quotient
        self.staticbox_type_quotient_staticbox = wx.StaticBox(self, -1, _(u"Type de quotient"))
        self.ctrl_type_quotient = CTRL_Type_quotient(self)

        # Activit�s
        self.staticbox_activites_staticbox = wx.StaticBox(self, -1, _(u"Activit�s"))
        self.ctrl_activites = CTRL_Selection_activites.CTRL(self)
        self.ctrl_activites.SetMinSize((-1, 90))
        
        # Inscrits / Pr�sents
        self.staticbox_presents_staticbox = wx.StaticBox(self, -1, _(u"Options"))
        self.ctrl_options = Options(self)
        
        # Boutons afficher
        self.bouton_afficher = CTRL_Bouton_image.CTRL(self, texte=_(u"Rafra�chir la liste"), cheminImage="Images/32x32/Actualiser.png")
        self.bouton_afficher.SetMinSize((-1, 30))

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_BUTTON, self.OnBoutonAfficher, self.bouton_afficher)

    def __set_properties(self):
        self.bouton_afficher.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour afficher la liste en fonction des param�tres s�lectionn�s")))
        self.ctrl_type_quotient.SetToolTip(wx.ToolTip(_(u"S�lectionnez un type de quotient dans la liste")))

    def __do_layout(self):
        grid_sizer_base = wx.FlexGridSizer(rows=5, cols=1, vgap=10, hgap=10)

        # Type de quotient
        staticbox_type_quotient = wx.StaticBoxSizer(self.staticbox_type_quotient_staticbox, wx.VERTICAL)
        staticbox_type_quotient.Add(self.ctrl_type_quotient, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_base.Add(staticbox_type_quotient, 1, wx.RIGHT|wx.EXPAND, 5)

        # Activit�s
        staticbox_activites = wx.StaticBoxSizer(self.staticbox_activites_staticbox, wx.VERTICAL)
        staticbox_activites.Add(self.ctrl_activites, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_base.Add(staticbox_activites, 1, wx.RIGHT|wx.EXPAND, 5)
        
        # Inscrits / Pr�sents
        staticbox_presents = wx.StaticBoxSizer(self.staticbox_presents_staticbox, wx.VERTICAL)
        staticbox_presents.Add(self.ctrl_options, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_base.Add(staticbox_presents, 1, wx.RIGHT|wx.EXPAND, 5)
        
        # Bouton Afficher
        grid_sizer_base.Add(self.bouton_afficher, 1, wx.RIGHT|wx.EXPAND, 5)

        self.SetSizer(grid_sizer_base)
        grid_sizer_base.Fit(self)
        grid_sizer_base.AddGrowableRow(1)
        grid_sizer_base.AddGrowableCol(0)

    def OnBoutonAfficher(self, event):
        """ Validation des donn�es saisies """
        # V�rifie le type de quotient
        IDtype_quotient = self.ctrl_type_quotient.GetID()
        if IDtype_quotient == None :
            dlg = wx.MessageDialog(self, _(u"Vous devez s�lectionner obligatoirement un type de quotient dans la liste !"), _(u"Erreur de saisie"), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            self.ctrl_type_quotient.SetFocus()
            return False

        # V�rifie date de r�f�rence
        date_reference = self.ctrl_options.ctrl_date.GetDate()
        if self.ctrl_options.ctrl_date.FonctionValiderDate() == False or date_reference == None :
            dlg = wx.MessageDialog(self, _(u"La date de situation ne semble pas valide !"), _(u"Erreur de saisie"), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            self.ctrl_options.ctrl_date.SetFocus()
            return False
                
        # V�rifie les activit�s s�lectionn�es
        listeActivites = self.ctrl_activites.GetActivites()
        if len(listeActivites) == 0 :
            dlg = wx.MessageDialog(self, _(u"Vous n'avez s�lectionn� aucune activit� !"), _(u"Erreur de saisie"), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return False
        
        # Uniquement les familles avec ou sans ?
        familles = self.ctrl_options.GetFamilles() 
        
        # V�rifie Inscrits / Pr�sents
        presents = self.ctrl_options.GetPresents()
        if presents == False : return
        
        # Envoi des donn�es
        self.parent.MAJ(date_reference=date_reference, listeActivites=listeActivites, presents=presents, familles=familles, IDtype_quotient=IDtype_quotient)
        
        return True
    


# --------------------------------------------------------------------------------------------------------------------------------------------------

class Dialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX)
        self.parent = parent
        
        intro = _(u"Vous pouvez ici consulter et imprimer la liste des quotients familiaux/revenus � la date de r�f�rence donn�e pour la ou les activit�s s�lectionn�es. Commencez par saisir une date de r�f�rence puis s�lectionnez un ou plusieurs groupes d'activit�s ou certaines activit�s avant de cliquer sur le bouton 'Rafra�chir la liste'.")
        titre = _(u"Liste des quotients familiaux/revenus")
        self.SetTitle(titre)
        self.ctrl_bandeau = CTRL_Bandeau.Bandeau(self, titre=titre, texte=intro, hauteurHtml=30, nomImage="Images/32x32/Calculatrice.png")
        
        self.ctrl_parametres = Parametres(self)
        self.ctrl_listview = OL_Liste_quotients.ListView(self, id=-1, style=wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL|wx.LC_HRULES|wx.LC_VRULES)
        self.ctrl_listview.SetMinSize((100, 100))
        self.ctrl_recherche = OL_Liste_quotients.CTRL_Outils(self, listview=self.ctrl_listview)
        
        self.bouton_ouvrir_fiche = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Famille.png"), wx.BITMAP_TYPE_ANY))
        self.bouton_apercu = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Apercu.png"), wx.BITMAP_TYPE_ANY))
        self.bouton_imprimer = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Imprimante.png"), wx.BITMAP_TYPE_ANY))
        self.bouton_texte = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Texte2.png"), wx.BITMAP_TYPE_ANY))
        self.bouton_excel = wx.BitmapButton(self, -1, wx.Bitmap(Chemins.GetStaticPath("Images/16x16/Excel.png"), wx.BITMAP_TYPE_ANY))
        
        self.bouton_aide = CTRL_Bouton_image.CTRL(self, texte=_(u"Aide"), cheminImage="Images/32x32/Aide.png")
        self.bouton_fermer = CTRL_Bouton_image.CTRL(self, id=wx.ID_CANCEL, texte=_(u"Fermer"), cheminImage="Images/32x32/Fermer.png")

        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_BUTTON, self.OuvrirFiche, self.bouton_ouvrir_fiche)
        self.Bind(wx.EVT_BUTTON, self.Apercu, self.bouton_apercu)
        self.Bind(wx.EVT_BUTTON, self.Imprimer, self.bouton_imprimer)
        self.Bind(wx.EVT_BUTTON, self.ExportTexte, self.bouton_texte)
        self.Bind(wx.EVT_BUTTON, self.ExportExcel, self.bouton_excel)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonAide, self.bouton_aide)
        
        self.MAJ(None)
        

    def __set_properties(self):
        self.bouton_ouvrir_fiche.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour ouvrir la fiche de la famille s�lectionn�e dans la liste")))
        self.bouton_apercu.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour cr�er un aper�u de la liste")))
        self.bouton_imprimer.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour imprimer la liste")))
        self.bouton_texte.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour exporter la liste au format Texte")))
        self.bouton_excel.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour exporter la liste au format Excel")))
        self.bouton_aide.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour obtenir de l'aide")))
        self.bouton_fermer.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour fermer")))
        self.SetMinSize((950, 700))

    def __do_layout(self):
        grid_sizer_base = wx.FlexGridSizer(rows=3, cols=1, vgap=10, hgap=10)
        
        grid_sizer_contenu = wx.FlexGridSizer(rows=1, cols=3, vgap=5, hgap=5)
        
        # Panel des param�tres
        grid_sizer_contenu.Add(self.ctrl_parametres, 1, wx.EXPAND, 0)
        
        # Liste + Barre de recherche
        grid_sizer_gauche = wx.FlexGridSizer(rows=3, cols=1, vgap=10, hgap=10)
        grid_sizer_base.Add(self.ctrl_bandeau, 0, wx.EXPAND, 0)
        grid_sizer_gauche.Add(self.ctrl_listview, 0, wx.EXPAND, 0)
        grid_sizer_gauche.Add(self.ctrl_recherche, 0, wx.EXPAND, 0)
        grid_sizer_gauche.AddGrowableRow(0)
        grid_sizer_gauche.AddGrowableCol(0)
        grid_sizer_contenu.Add(grid_sizer_gauche, 1, wx.EXPAND, 0)
        
        # Commandes
        grid_sizer_droit = wx.FlexGridSizer(rows=7, cols=1, vgap=5, hgap=5)
        grid_sizer_droit.Add(self.bouton_ouvrir_fiche, 0, 0, 0)
        grid_sizer_droit.Add( (5, 5), 0, 0, 0)
        grid_sizer_droit.Add(self.bouton_apercu, 0, 0, 0)
        grid_sizer_droit.Add(self.bouton_imprimer, 0, 0, 0)
        grid_sizer_droit.Add( (5, 5), 0, 0, 0)
        grid_sizer_droit.Add(self.bouton_texte, 0, 0, 0)
        grid_sizer_droit.Add(self.bouton_excel, 0, 0, 0)
        grid_sizer_contenu.Add(grid_sizer_droit, 1, wx.EXPAND, 0)
        
        grid_sizer_contenu.AddGrowableRow(0)
        grid_sizer_contenu.AddGrowableCol(1)
        grid_sizer_base.Add(grid_sizer_contenu, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 10)
        
        # Boutons
        grid_sizer_boutons = wx.FlexGridSizer(rows=1, cols=3, vgap=10, hgap=10)
        grid_sizer_boutons.Add(self.bouton_aide, 0, 0, 0)
        grid_sizer_boutons.Add((20, 20), 0, wx.EXPAND, 0)
        grid_sizer_boutons.Add(self.bouton_fermer, 0, 0, 0)
        grid_sizer_boutons.AddGrowableCol(1)
        grid_sizer_base.Add(grid_sizer_boutons, 1, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 10)
        self.SetSizer(grid_sizer_base)
        grid_sizer_base.Fit(self)
        grid_sizer_base.AddGrowableRow(1)
        grid_sizer_base.AddGrowableCol(0)
        self.Layout()
        self.CenterOnScreen()

    def OuvrirFiche(self, event):
        self.ctrl_listview.OuvrirFicheFamille(None)

    def Apercu(self, event):
        self.ctrl_listview.Apercu(None)
        
    def Imprimer(self, event):
        self.ctrl_listview.Imprimer(None)

    def ExportTexte(self, event):
        self.ctrl_listview.ExportTexte(None)

    def ExportExcel(self, event):
        self.ctrl_listview.ExportExcel(None)

    def OnBoutonAide(self, event): 
        from Utils import UTILS_Aide
        UTILS_Aide.Aide("Listedesquotientsfamiliaux")

    def MAJ(self, date_reference=None, listeActivites=None, presents=None, familles=None, IDtype_quotient=None):
        labelParametres = self.GetLabelParametres() 
        self.ctrl_listview.MAJ(date_reference, listeActivites, presents, familles, labelParametres, IDtype_quotient)

    def GetLabelParametres(self):
        listeParametres = []

        # Type de quotient
        nom_type_quotient = self.ctrl_parametres.ctrl_type_quotient.GetStringSelection()
        listeParametres.append(_(u"Type de quotient : %s") % nom_type_quotient)

        # Date
        date = self.ctrl_parametres.ctrl_options.ctrl_date.GetDate()
        if date != None :
            listeParametres.append(_(u"Situation au %s") % UTILS_Dates.DateEngFr(str(date)))
                
        # Activit�s
        activites = ", ".join(self.ctrl_parametres.ctrl_activites.GetLabelActivites())
        if activites == "" : 
            activites = _(u"Aucune")
        listeParametres.append(_(u"Activit�s : %s") % activites)
        
        # Options
        option = self.ctrl_parametres.ctrl_options.GetFamilles() 
        if option == "AVEC" : listeParametres.append(_(u"Uniquement les familles avec QF"))
        if option == "SANS" : listeParametres.append(_(u"Uniquement les familles sans QF"))

        # Pr�sents
        presents = self.ctrl_parametres.ctrl_options.GetPresents()
        if presents == None :
            listeParametres.append(_(u"Toutes les familles dont un des membres est inscrit"))
        else :
            listeParametres.append(_(u"Uniquement les familles dont un des membres est pr�sent du %s au %s") % (UTILS_Dates.DateEngFr(str(presents[0])), UTILS_Dates.DateEngFr(str(presents[1]))))
        
        labelParametres = " | ".join(listeParametres)
        return labelParametres



if __name__ == "__main__":
    app = wx.App(0)
    #wx.InitAllImageHandlers()
    dialog_1 = Dialog(None)
    app.SetTopWindow(dialog_1)
    dialog_1.ShowModal()
    app.MainLoop()
