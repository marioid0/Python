import tkinter as tk
from tkinter import messagebox
import os
import re
import subprocess

hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect_ip = "127.0.0.1"

# function to validate the url
def is_valid_url(url):
    url_pattern = re.compile(r"^(?!localhost)(?!\d+\.\d+\.\d+\.\d+)(?!.*\s)[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?$")
    return bool(url_pattern.match(url))

# simple function to clean dns_cache
def clear_dns_cache():
    try:
        result = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            messagebox.showinfo("Cache de DNS", "Cache de DNS limpo com sucesso!")
        else:
            messagebox.showwarning("Cache de DNS", f"Falha ao limpar o cache de DNS.\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao limpar o cache de DNS: {e}")

def block_site():
    site = site_entry.get().strip().replace("https://", "").replace("http://", "").replace("www.", "")
    if site:
        if is_valid_url(site):
            try:
                with open(hosts_path, "r+") as file:
                    content = file.read()
                    base_entry = f"{redirect_ip} {site}\n"
                    www_entry = f"{redirect_ip} www.{site}\n"
                    if base_entry not in content and www_entry not in content:
                        file.write(base_entry)
                        file.write(www_entry)
                        if site not in [listbox.get(i) for i in range(listbox.size())]:
                            listbox.insert(tk.END, site)
                        site_entry.delete(0, tk.END)
                        messagebox.showinfo("Sucesso", f"O site '{site}' foi bloqueado!")
                        clear_dns_cache()
                    else:
                        messagebox.showwarning("Aviso", f"O site '{site}' já está bloqueado.")
            except PermissionError:
                messagebox.showerror("Erro", "Permissões insuficientes para modificar o arquivo hosts. Execute como administrador.")
        else:
            messagebox.showwarning("Aviso", "Digite um site válido (exemplo: www.exemplo.com).")
    else:
        messagebox.showwarning("Aviso", "Digite um site para bloquear.")

# Função de desbloqueio de sites
def unblock_site():
    selected_site = listbox.get(tk.ACTIVE)
    if selected_site:
        try:
            with open(hosts_path, "r+") as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if selected_site not in line and f"www.{selected_site}" not in line:
                        file.write(line)
                file.truncate()
            listbox.delete(tk.ACTIVE)
            messagebox.showinfo("Sucesso", f"O site '{selected_site}' foi desbloqueado!")
            clear_dns_cache()  # Limpa o cache de DNS após desbloquear
        except PermissionError:
            messagebox.showerror("Erro", "Permissões insuficientes para modificar o arquivo hosts. Execute como administrador.")
    else:
        messagebox.showwarning("Aviso", "Selecione um site para desbloquear.")

# Tkinter
root = tk.Tk()
root.title("BlockBlocker")
root.geometry("600x600")
root.configure(bg="#1a1a2e")  # Cor de fundo

# Função de mouse hover no botão de desbloqueio
def animate_button(button):
    original_color = button.cget("background")
    button.config(background="#f54291")
    button.after(100, lambda: button.config(background=original_color))

# Personalizated font
try:
    pixel_font = ("Minecraftia", 14)
except:
    pixel_font = ("Courier", 14)  # Fallback para uma fonte semelhante

header_frame = tk.Frame(root, bg="#1a1a2e")
header_frame.pack(pady=20)
header_label = tk.Label(header_frame, text="BlockBlocker", font=("Arial", 30, "bold"), bg="#1a1a2e", fg="#f54291")
header_label.pack()

entry_frame = tk.Frame(root, bg="#1a1a2e")
entry_frame.pack(pady=10)
entry_label = tk.Label(entry_frame, text="Digite o site para bloquear:", font=pixel_font, bg="#1a1a2e", fg="#ffffff")
entry_label.pack()
site_entry = tk.Entry(entry_frame, font=pixel_font, width=30, relief="solid", highlightbackground="#f54291", highlightcolor="#4db8ff", highlightthickness=2)
site_entry.pack(pady=5)

button_frame = tk.Frame(root, bg="#1a1a2e")
button_frame.pack(pady=20)
block_button = tk.Button(button_frame, text="Bloquear", command=block_site, bg="#f54291", fg="white", font=pixel_font, relief="flat", width=15)
block_button.grid(row=0, column=0, padx=10)
unblock_button = tk.Button(button_frame, text="Desbloquear", command=unblock_site, bg="#4db8ff", fg="white", font=pixel_font, relief="flat", width=15)
unblock_button.grid(row=0, column=1, padx=10)

block_button.bind("<Enter>", lambda e: animate_button(block_button))
unblock_button.bind("<Enter>", lambda e: animate_button(unblock_button))

list_frame = tk.Frame(root, bg="#1a1a2e")
list_frame.pack(pady=10, fill="both", expand=True)
list_label = tk.Label(list_frame, text="Sites Bloqueados:", font=pixel_font, bg="#1a1a2e", fg="#ffffff")
list_label.pack(anchor="w", pady=(0, 5))

listbox = tk.Listbox(list_frame, font=pixel_font, height=10, bg="#33334d", fg="#ffffff", relief="flat", selectbackground="#f54291", selectforeground="white")
listbox.pack(fill="both", padx=10, pady=5, expand=True)

def add_blocked_sites():
    if os.path.exists(hosts_path):
        with open(hosts_path, "r") as file:
            for line in file:
                if line.startswith(redirect_ip):
                    parts = line.split()
                    if len(parts) > 1:
                        site = parts[1].replace("www.", "")
                        if is_valid_url(site) and site not in [listbox.get(i) for i in range(listbox.size())]:
                            listbox.insert(tk.END, site)

add_blocked_sites()

root.mainloop()
