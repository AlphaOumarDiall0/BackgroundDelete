import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from rembg import remove

def select_image():
    global img_path
    img_path = filedialog.askopenfilename(
        title="Sélectionner une image",
        filetypes=(("Image Files", "*.jpg;*.jpeg;*.png"), ("All Files", "*.*"))
    )
    if img_path:
        load_image(img_path)

def load_image(path):
    global img, img_display
    img = Image.open(path)
    img_display = img.copy()
    img_display.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img_display)
    img_label.config(image=img_tk)
    img_label.image = img_tk

def remove_background():
    global result, result_display
    if not img_path:
        messagebox.showerror("Erreur", "Vous n'avez sélectionné aucune image !")
        return

    try:
        img = Image.open(img_path)
        result = remove(img)
        result_display = result.copy()
        result_display.thumbnail((300, 300))
        show_result(result_display)
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue: {e}")

def show_result(result_img):
    result_tk = ImageTk.PhotoImage(result_img)
    img_label.config(image=result_tk)
    img_label.image = result_tk


def save_result():
    if result is None:
        messagebox.showerror("Erreur", "Il n'y a aucun résultat à enregistrer!")
        return

    output_path = filedialog.asksaveasfilename(
        title="Enregistrer l'image",
        defaultextension=".png",
        filetypes=(("PNG Files", "*.png"), ("All Files", "*.*"))
    )

    if output_path:
        # Redimensionner l'image avant de la sauvegarder
        result_resized = result.resize((int(result.width * 0.3), int(result.height * 0.3)), Image.Resampling.LANCZOS)
        result_resized.save(output_path, optimize=True, quality=70)
        messagebox.showinfo("Succès", f"L'image a été enregistrée avec succès dans {output_path}")

def toggle_mode():
    global is_night_mode
    if is_night_mode:
        root.config(bg=day)
        main_frame.config(bg=day)
        button_frame.config(bg=day)
        img_label.config(bg=day)
        #result_label.config(bg=day)
        #footer_label.config(bg="white", fg="black")
        welcome_label.config(bg=day, fg="#4CB7E4")
        btn_toggle_mode.config(image=iconMoon)
    else:
        root.config(bg=night)
        main_frame.config(bg=night)
        button_frame.config(bg=night)
        img_label.config(bg=night)
        #result_label.config(bg=night)
        #footer_label.config(bg="#4CB7E4", fg="white")
        welcome_label.config(bg=night, fg="#4CB7E4")
        btn_toggle_mode.config(image=iconSun)
    is_night_mode = not is_night_mode


# Initialiser la fenêtre principale Tkinter
root = tk.Tk()
root.title("Supprimer l'arrière plan")
root.resizable(False, False)
icon = tk.PhotoImage(file='icon.ico')
root.iconphoto(False, icon)

# Définir la taille initiale de la fenêtre principale
root.geometry('670x600')

# Initialiser les variables globales
img_path = ""
img = None
img_display = None
result = None
result_display = None
is_night_mode = False
night = "#2D2D2D"
day = "white"


# Créer le cadre principal
main_frame = tk.Frame(root, bg='white')
main_frame.pack(fill='both', expand=True)

# Message de bienvenue en haut
welcome_label = tk.Label(main_frame, text="Bienvenue dans l'application de suppression de fond", font=("times new roman", 20, 'bold'), fg='#4CB7E4', bg='white')
welcome_label.pack(pady=10, anchor='center')

# Créer les éléments de l'interface graphique
button_frame = tk.Frame(main_frame, bg='white')
button_frame.pack(pady=20, anchor='center')

iconSelect = ImageTk.PhotoImage(Image.open('select.png').resize((50, 50)))
iconDelete = ImageTk.PhotoImage(Image.open('delete.png').resize((50, 50)))
iconSave = ImageTk.PhotoImage(Image.open('save.png').resize((50, 50)))
iconProduct = ImageTk.PhotoImage(Image.open('product.png').resize((30, 30)))
iconSun = ImageTk.PhotoImage(Image.open('sun.png').resize((30, 30)))
iconMoon = ImageTk.PhotoImage(Image.open('moon.png').resize((30, 30)))

# Bouton pour sélectionner une image
btn_select = tk.Button(button_frame, text="Sélectionner l'image", font=("times new roman", 15, "bold"), image=iconSelect, compound='top', border=0, cursor='hand2', bg='#4CB7E4', fg='#FFF', command=select_image)
btn_select.grid(row=0, column=0, padx=10)

# Bouton pour enlever l'arrière-plan
btn_remove_bg = tk.Button(button_frame, text="Supprimer l'arrière plan", font=("times new roman", 15, "bold"), image=iconDelete, compound='top', border=0, cursor='hand2', bg='red', fg='#FFF', command=remove_background)
btn_remove_bg.grid(row=0, column=1, padx=10)

# Bouton pour sauvegarder le résultat
btn_save = tk.Button(button_frame, text="Enregistrer le résultat", font=("times new roman", 15, "bold"), image=iconSave, compound='top', border=0, cursor='hand2', bg='#3CBA26', fg='#FFF', command=save_result)
btn_save.grid(row=0, column=2, padx=10)

# Label pour afficher l'image sélectionnée et résultante
img_label = tk.Label(main_frame, bg='white')
img_label.pack(pady=10, anchor='center')

# Label pour afficher l'image résultante
#result_label = tk.Label(main_frame, bg='white')
#result_label.pack(pady=10, anchor='center')

# Pied de page
footer_label = tk.Label(root, text="  Produit par AOD Copyright (C) 2024 tous droits réservés", image=iconProduct, compound='left', width='670', pady='10', font=("times new roman", 15), bg=("#4CB7E4"), fg="white")
footer_label.pack(pady=0)

btn_toggle_mode = tk.Button(footer_label, image=iconMoon, bg=("#4CB7E4"), border=0, cursor='hand2', command=toggle_mode)
btn_toggle_mode.place(x=600, y=8)

# Démarrer la boucle principale de Tkinter
root.mainloop()
