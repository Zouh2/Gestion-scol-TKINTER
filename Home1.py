import sys
from datetime import datetime
from tkinter import *
from tkinter import ttk, messagebox
from subprocess import call
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import os

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
import mysql.connector
import mysql

if len(sys.argv) > 1:
    id_user = sys.argv[1]
else:
    messagebox.showerror("Error", "id_user not provided!")
    sys.exit(1)
def Ajouter():
    matricule = txtNumero.get()
    nom = txtnom.get()
    prenom = txtprenom.get()
    sexe = valeurSexe.get()
    classe = comboClasse.get()
    montant = txtMontant.get()

    maBase = mysql.connector.connect(host="localhost", user="root", password="", database="scolarite")
    meConnect = maBase.cursor()

    try:

        print(f"ID utilisateur à vérifier : {matricule}")


        meConnect.execute("SELECT * FROM etudiants WHERE code = %s", (matricule,))
        resultat = meConnect.fetchone()


        print(f"Résultat de la requête : {resultat}")

        if resultat:
            messagebox.showwarning("Attention", "Le paiement pour cet utilisateur a déjà été effectué.")
        else:

            sql = "INSERT INTO etudiants (code, nom, prenom, sexe, classe, Montant, id_user) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (matricule, nom, prenom, sexe, classe, montant, id_user)
            meConnect.execute(sql, val)
            maBase.commit()
            messagebox.showinfo("Information", "Paiement effectué avec succès!")
            root.destroy()
            call(["python", "Home1.py", str(id_user)])

    except Exception as e:
        print(f"Erreur rencontrée : {e}")
        messagebox.showerror("Erreur", "Une erreur s'est produite lors de l'ajout.")
        maBase.rollback()
    finally:
        maBase.close()


def imprimer():

    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un étudiant dans le tableau.")
        return

    item = table.item(selected_item)
    values = item['values']

    if not values:
        messagebox.showwarning("Avertissement", "Informations de l'étudiant non trouvées.")
        return

    student_code = values[0]
    pdf_path = f"C:\\Users\\DELL\\Desktop\\REcu scolarite\\{student_code}.pdf"

    # Vérifiez si le fichier PDF existe déjà
    if os.path.exists(pdf_path):
        messagebox.showwarning("Avertissement", "Ce reçu a déjà été imprimé.")
        return

    c = canvas.Canvas(pdf_path, pagesize=letter)


    y = 750
    line_height = 40

    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, y, "Reçu de Paiement")
    y -= line_height * 2

    c.setFont("Helvetica", 12)
    c.drawString(100, y, f"Code étudiant : {values[0]}")
    y -= line_height
    c.drawString(100, y, f"Nom étudiant : {values[1]}")
    y -= line_height
    c.drawString(100, y, f"Prenom étudiant: {values[2]}")
    y -= line_height
    c.drawString(100, y, f"Sexe : {values[3]}")
    y -= line_height
    c.drawString(100, y, f"Classe: {values[4]}")
    y -= line_height
    c.drawString(100, y, f"Montant paye : {values[5]} DH ")
    y -= line_height
    current_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    c.drawString(350, y , f"Date d'impression: {current_date}")
    y -= line_height * 1.5
    c.drawString(100, y, f"signature :  ")
    y -= line_height - 20
    signature_path = f"C:\\Users\\DELL\\Downloads\\imagesignature.png"
    if os.path.exists(signature_path):
        signature_image = ImageReader(signature_path)
        c.drawImage(signature_image, 300, 150, width=150,
                    height=150)


    c.save()
    messagebox.showinfo("Succès", f"Reçu sauvegardé sous: {pdf_path}")

def Modifer():
    matricule = txtNumero.get()
    nom = txtnom.get()
    prenom = txtprenom.get()
    sexe = valeurSexe.get()
    classe = comboClasse.get()
    montant  = txtMontant.get()

    maBase = mysql.connector.connect(host="localhost", user="root",password="", database="scolarite")
    meConnect = maBase.cursor()

    try:
        sql = "update etudiants set  nom=%s,prenom= %s,sexe= %s,classe=%s,montant= %s where code= %s "
        val = (nom,prenom, sexe,classe,montant, matricule )
        meConnect.execute(sql, val)
        maBase.commit()
        derniereMatricule = meConnect.lastrowid
        messagebox.showinfo("information", "Payement  modifier")
        root.destroy()
        call(["python", "Home1.py", str(id_user)])

    except Exception as e:
        print(e)
        #retour
        maBase.rollback()
        maBase.close()


def on_table_click(event):
    selected_item = table.selection()[0]
    values = table.item(selected_item, 'values')
    txtNumero.delete(0, END)
    txtNumero.insert(0, values[0])
    txtnom.delete(0, END)
    txtnom.insert(0, values[1])
    txtprenom.delete(0, END)
    txtprenom.insert(0, values[2])
    valeurSexe.set(values[3])
    comboClasse.set(values[4])
    txtMontant.delete(0, END)
    txtMontant.insert(0, values[5])

def Supprimer():
    matricule = txtNumero.get()

    maBase = mysql.connector.connect(host="localhost", user="root",password="", database="scolarite")
    meConnect = maBase.cursor()

    try:
        sql = "delete from etudiants where code= %s "
        val = ( matricule,)
        meConnect.execute(sql, val)
        maBase.commit()
        derniereMatricule = meConnect.lastrowid
        messagebox.showinfo("information", " Payement Supprimer")
        root.destroy()
        call(["python", "Home1.py", str(id_user)])

    except Exception as e:
        print(e)
        #retour
        maBase.rollback()
        maBase.close()


def chercher():

    code_client = lblcherche.get()

    maBase = mysql.connector.connect(host="localhost", user="root", password="", database="scolarite")
    meConnect = maBase.cursor()

    try:
        # Vider le tableau actuel
        for row in table.get_children():
            table.delete(row)

        if not code_client:
            meConnect.execute("SELECT code, nom, prenom, sexe, classe, Montant FROM etudiants")
        else:
            meConnect.execute("SELECT code, nom, prenom, sexe, classe, Montant FROM etudiants WHERE code = %s",
                              (code_client,))


        for row in meConnect:
            table.insert('', END, value=row)

    except Exception as e:
        print(f"Erreur lors de la recherche : {e}")
        messagebox.showerror("Erreur", "Une erreur s'est produite lors de la recherche.")
    finally:
        maBase.close()
def exit():
    root.destroy()

def validate_number(event):
    """Validate if the entered value is a number."""
    value = txtMontant.get()

    if not value.isdigit() and value != "":
        txtMontant.delete(len(value) - 1)

root = Tk()
root.title("Gestion de scolarité")
root.geometry("1350x700+0+0")
root.configure(background="#7BD3EA")

lbltitre = Label(root, borderwidth=3, relief=SUNKEN, text="Gestion de scolarité", font="Times 24 bold italic",
                 background="#FCFCFC", fg="#756AB6")
lbltitre.place(x=0, y=0, width=1350, height=70)




lblNumero = Label(root, text="Id", font=("Arial", 18), bg="#7BD3EA", fg="black")
lblNumero.place(x=70, y=100, width=150)
txtNumero = Entry(root, bd=4, font=("Arial", 14))
txtNumero.place(x=250, y=100, width=150)

lblnom = Label(root, text="Nom", font=("Arial", 14), bg="#7BD3EA", fg="black")
lblnom.place(x=70, y=150, width=150)
txtnom = Entry(root, bd=4, font=("Arial", 14))
txtnom.place(x=250, y=150, width=300)


lblprenom = Label(root, text="Prenom", font=("Arial", 14), bg="#7BD3EA", fg="black")
lblprenom.place(x=70, y=200, width=150)
txtprenom = Entry(root, bd=4, font=("Arial", 14))
txtprenom.place(x=250, y=200, width=300)


valeurSexe = StringVar()
lblSexeMasculin = Radiobutton(root, text="MASCULIN", value="M", variable=valeurSexe, indicatoron=0,
                              font=("Arial", 14), bg="#7BD3EA", fg="#696969")
lblSexeMasculin.place(x=250, y=250, width=130)
txtSexeFeminin = Radiobutton(root, text="FEMININ", value="F", variable=valeurSexe, indicatoron=0,
                             font=("Arial", 14), bg="#7BD3EA", fg="#696969")
txtSexeFeminin.place(x=420, y=250, width=130)


lblClasse = Label(root, text="Classe", font=("Arial", 18), bg="#7BD3EA", fg="black")
lblClasse.place(x=70, y=300, width=150)
comboClasse = ttk.Combobox(root, font=("Arial", 14))
comboClasse['values'] = ['INE1', 'INE2', 'INE3','Master']
comboClasse.place(x=250, y=300, width=130)


lblMontant = Label(root, text="Montant", font=("Arial", 18), bg="#7BD3EA", fg="black")
lblMontant.place(x=70, y=350, width=150)


txtMontant = Entry(root, bd=4, font=("Arial", 14))
txtMontant.place(x=250, y=350, width=200)

txtMontant.bind("<KeyRelease>", validate_number)


btnenregistrer = Button(root, text="Enregistrer", font="times 14 bold", bg="#ffa245", fg="white",command=Ajouter)
btnenregistrer.place(x=130, y=440, width=150)

btnmodofier = Button(root, text="Modifier", font="times 14 bold", bg="#ffa245", fg="white",command=Modifer)
btnmodofier.place(x=380, y=440, width=150)

btnSupprimer = Button(root, text="Supprimer", font="times 14 bold", bg="#ffa245", fg="white",command=Supprimer)
btnSupprimer.place(x=130, y=500, width=150)
btnimprimer = Button(root, text="Imprimer", font="times 14 bold", bg="#ffa245", fg="white",command=imprimer)
btnimprimer.place(x=380, y=500, width=150)

btcherche = Button(root, text="Chercher", font="times 14 bold", bg="#ffa245", fg="white",command=chercher)
btcherche.place(x=130, y= 580, width=150)
lblcherche = Entry(root, bd=4, font=("Arial", 14))
lblcherche.place(x=380, y=580, width=150)

Exit = Button(root, text="Quitter", font="times 14 bold ", fg="white", bg="#ffa245", command=exit, border=2)
Exit.place(x=230, y=650, width=200)


table = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6, 7), height=5, show="headings")
table.place(x=560, y=100, width=790, height=450)


table.heading(1, text="Code")
table.heading(2, text="NOM")
table.heading(3, text="PRENOM")
table.heading(4, text="SEXE")
table.heading(5, text="CLASSE")
table.heading(6, text="montant")



table.column(1, width=150)
table.column(2, width=150)
table.column(3, width=150)
table.column(4, width=100)
table.column(5, width=100)
table.column(6, width=150)

table.bind("<ButtonRelease-1>", on_table_click)

maBase = mysql.connector.connect(host="localhost", user="root", password="", database="scolarite")
meConnect = maBase.cursor()
meConnect.execute("SELECT code, nom, prenom, sexe, classe, Montant FROM etudiants WHERE id_user = %s", (id_user,))
for row in meConnect:
    table.insert('', END, value=row)
maBase.close()

root.mainloop()
