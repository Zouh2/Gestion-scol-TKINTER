from tkinter import *
from tkinter import ttk, messagebox
from datetime import *
from subprocess import call
import mysql.connector

fen = Tk()
fen.title("Gestion De Scolarité")
x = (fen.winfo_screenwidth() - 800) / 2
y = (fen.winfo_screenheight() - 600) / 2
fen.geometry('%dx%d+%d+%d' % (800, 600, x, y))
LabTitre = Label(fen, text="Gestion de scolarité", font="Times 24 bold italic", fg="#756AB6", bg="#FCFCFC", width=100)
LabTitre.pack(padx=0, pady=0)


def MenuPrincipale(fen, frame=None):
    if frame:
        frame.destroy()
    LogFrame = Frame(fen)
    LogFrame.pack()
    MsgLog = Label(LogFrame, text=" connexion autant que :", font="Bahnschrift 16 bold", fg="#22B9A8")
    MsgLog.pack(pady=10)
    optionsLog = ["Responsable Regie ", "Etudiant "]
    for i in range(len(optionsLog)):
        if i == 1:
            bg = "#1199B7"
        else:
            bg = "#22B9A8"
        BT = Button(LogFrame, text=optionsLog[i].upper(), font="times 20 bold ", fg="white", bg=bg, width=25,
                    command=lambda a=i: OperationLog(fen, LogFrame, optionsLog[a]))
        BT.pack(pady=10)
    Exit = Button(LogFrame, text="Quitter", font="times 20 bold ", fg="white", bg="#ffa245", width=15,
                  command=exit, border=0)
    Exit.pack(pady=25)


def OperationLog(fen, FM, opt):
    FM.destroy()
    if opt == "Responsable Regie":
        afficherFrameConnexion(fen, opt)
    elif opt == "Etudiant ":
        Etudiant(fen)
    else:
        afficherFrameConnexion(fen, opt)


from tkinter import Frame, Label, Button, Entry


def Etudiant(fen, frame=None):
    def chercher2():
        code_client = code.get()

        maBase = mysql.connector.connect(host="localhost", user="root", password="", database="scolarite")
        meConnect = maBase.cursor()

        try:
            if not code_client:
                meConnect.execute("SELECT code, nom, prenom, sexe, classe, Montant FROM etudiants")
            else:
                meConnect.execute("SELECT code, nom, prenom, sexe, classe, Montant FROM etudiants WHERE code = %s",
                                  (code_client,))


            result = meConnect.fetchone()

            if result:

                montant_paye = result[5]
                messagebox.showinfo("Info", f"VOUS AVEZ DÉJÀ PAYÉ {montant_paye} DH.")
            else:

                messagebox.showerror("Erreur", "Vous n'avez pas payé.")

        except Exception as e:
            print(f"Erreur lors de la recherche : {e}")
            messagebox.showerror("Erreur", "Une erreur s'est produite lors de la recherche.")
        finally:
            maBase.close()

    if frame:
        frame.destroy()

    LogFrame = Frame(fen)
    LogFrame.pack(pady=50)

    MsgLog = Label(LogFrame, text="taper votre code ", font="Bahnschrift 16 bold", fg="#22B9A8")
    MsgLog.pack(pady=20)


    code = Entry(LogFrame, font="times 16")
    code.pack(pady=10)

    BT = Button(LogFrame, text="verfier", font="times 15 bold", fg="white", bg="#22B9A8", width=15, command=chercher2)
    BT.pack(side='left', padx=5, pady=5)

    Quitter = Button(LogFrame, text="Retour", font="times 15 bold", fg="white", bg="#ffa245", width=15,
                     command=lambda: MenuPrincipale(fen,
                                                    LogFrame))
    Quitter.pack(side='left', padx=5, pady=5)


def afficherFrameConnexion(fen, opt, frame=None):
    if frame:
        frame.destroy()
    frameLogin = Frame(fen, padx=5, pady=5)
    frameLogin.pack(pady=10)
    labelMsg = Label(frameLogin, text="Merci de connexion d'abord !", font="Bahnschrift 16 bold", fg="#22B9A8")
    labelMsg.grid(column=0, row=0, columnspan=2)
    if opt == "étudiant":
        formLogin(frameLogin, fen, opt)
        labeInsc = Label(frameLogin, text=" Vous n'avez inscré ? ", font="Bahnschrift 16 bold", fg="#22B9A8",
                         width=30)
        labeInsc.grid(row=6, column=0, columnspan=2, pady=5)
    else:
        formLogin(frameLogin, fen, opt)


def formLogin(frameLogin, fen, user):
    global entUser, entPass
    labeUser = Label(frameLogin, text="Nom d'utilisateur : ", font="Times 12")
    labeUser.grid(row=1, column=0, pady=5, sticky=NW)
    entUser = Entry(frameLogin, font="times 20 ", width=30, border=0)
    entUser.grid(row=2, column=0, columnspan=2, pady=5, sticky=NW)
    labePass = Label(frameLogin, text="Mot de pass : ", font="Times 12")
    labePass.grid(row=3, column=0, pady=5, sticky=NW)
    entPass = Entry(frameLogin, font="times 20 ", width=30, border=0, show="*")
    entPass.grid(row=4, column=0, columnspan=2, pady=5, sticky=NW)

    def toggle_password_visibility():
        if entPass.cget("show") == "*":
            entPass.config(show="")
            show_hide_btn.config(image=hide_img)
        else:
            entPass.config(show="*")
            show_hide_btn.config(image=show_img)

    show_img = PhotoImage(
        file=f"C:\\Users\\DELL\\Downloads\\close.PNG")
    hide_img = PhotoImage(
        file=f"C:\\Users\\DELL\\Downloads\\show.PNG")


    show_hide_btn = Button(frameLogin, image=show_img, border=0, command=toggle_password_visibility)
    show_hide_btn.grid(row=4, column=2, sticky=W, padx=(5, 0))

    annuler = Button(frameLogin, text=" Retour ", font="times 16 bold", width=15, fg="white", bg="#ffa245",
                     command=lambda: MenuPrincipale(fen, frameLogin))
    annuler.grid(row=5, column=0, pady=5)
    connex = Button(frameLogin, text="Connexion", font="times 16 bold", width=15, fg="white", bg="#22B9A8",
                    command=lambda: Connexion(fen, entUser, entPass, user))
    connex.grid(row=5, column=1, pady=5)


def Connexion(fen, entUser, entPass, user):
    surnom = entUser.get()
    mdp = entPass.get()
    maBase = mysql.connector.connect(host="localhost", user="root", password="", database="scolarite")
    meConnect = maBase.cursor()

    meConnect.execute("SELECT Id, pasword FROM users_regie WHERE Id = %s", (surnom,))
    result = meConnect.fetchone()

    meConnect.close()
    maBase.close()
    if not result:
        messagebox.showerror("", "Utilisateur non trouvé")
        entPass.delete(0, "end")
        entUser.delete(0, "end")
    elif mdp != result[1]:
        messagebox.showerror("", "Mot de passe incorrect")
        entPass.delete(0, "end")
        entPass.focus()
    else:
        entPass.delete(0, "end")
        entUser.delete(0, "end")
        fen.destroy()
        call(["python", "Home1.py", str(result[0])])


MenuPrincipale(fen)
fen.mainloop()
