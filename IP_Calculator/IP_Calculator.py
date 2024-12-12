import tkinter as tk
from tkinter import messagebox
import ipaddress

class CalculadoraIP:
    def __init__(self, master):
        self.master = master
        master.title("Calculadora IP")
        master.config(bg="#2c3e50")  # Cor de fundo
        master.geometry("600x550")
        master.resizable(False, False)

        # Estilo de Inputs
        label_style = {'bg': '#34495e', 'fg': 'white', 'font': ('Arial', 10, 'bold')}

        # Inputs
        self.label_ip = tk.Label(master, text="Endereço de Rede:", **label_style)
        self.label_ip.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.entry_ip = tk.Entry(master, font=('Arial', 12), width=20)
        self.entry_ip.grid(row=0, column=1, padx=20, pady=10)

        self.label_mascara = tk.Label(master, text="Máscara de Sub-rede (CIDR):", **label_style)
        self.label_mascara.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.entry_mascara = tk.Entry(master, font=('Arial', 12), width=20)
        self.entry_mascara.grid(row=1, column=1, padx=20, pady=10)

        # Botão para calcular
        self.calcular_button = tk.Button(master, text="Calcular", command=self.calcular_subredes, 
                                          bg="#1abc9c", fg="white", font=("Arial", 12, "bold"), relief="raised")
        self.calcular_button.grid(row=2, columnspan=2, pady=20)

        # Área de resultados
        self.resultados_frame = tk.Frame(master, bg="#34495e")
        self.resultados_frame.grid(row=3, columnspan=2, padx=20, pady=10)

        self.scrollbar = tk.Scrollbar(self.resultados_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.resultados_text = tk.Text(self.resultados_frame, height=15, width=70, yscrollcommand=self.scrollbar.set, 
                                       font=("Courier", 10), bg="#2c3e50", fg="white", bd=2, relief="solid")
        self.resultados_text.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.resultados_text.yview)

        self.resultados_text.config(state='disabled')

    def calcular_subredes(self):
        ip = self.entry_ip.get()
        mascara = self.entry_mascara.get()

        try:
            rede = ipaddress.ip_network(f"{ip}/{mascara}", strict=False)

            # Resultados
            self.resultados_text.config(state='normal')  # Habilita a edição temporariamente
            self.resultados_text.delete(1.0, tk.END)

            endereco_rede = rede.network_address
            primeiro_host = list(rede.hosts())[0] if rede.num_addresses > 2 else "N/A"
            ultimo_host = list(rede.hosts())[-1] if rede.num_addresses > 2 else "N/A"
            endereco_broadcast = rede.broadcast_address
            qtd_hosts_validos = rede.num_addresses - 2 if rede.num_addresses > 2 else 0

            # Classe de endereço IP
            primeiro_octeto = int(str(rede.network_address).split('.')[0])
            if primeiro_octeto <= 127:
                classe = 'A'
                bits_iniciais = 8
            elif primeiro_octeto <= 191:
                classe = 'B'
                bits_iniciais = 16
            else:
                classe = 'C'
                bits_iniciais = 24

            # Número de bits usados para sub-redes
            bits_subrede = rede.prefixlen - bits_iniciais

            # Número de subredes
            if bits_subrede < 0:
                num_subredes = 0  # Caso a máscara seja inválida para a classe
            else:
                num_subredes = 2 ** bits_subrede

            # Cálculo de hosts por subrede
            qtd_hosts_por_subrede = qtd_hosts_validos

            # Classificação do endereço IP (privado ou público)
            classificacao = "Privado" if rede.is_private else "Público"

            # Resultados
            self.resultados_text.insert(tk.END, f"Endereço IP: {ip}\n")
            self.resultados_text.insert(tk.END, f"Máscara de Sub-rede: {mascara}\n")
            self.resultados_text.insert(tk.END, f"Endereço de Rede: {endereco_rede}\n")
            self.resultados_text.insert(tk.END, f"Primeiro Host: {primeiro_host}\n")
            self.resultados_text.insert(tk.END, f"Último Host: {ultimo_host}\n")
            self.resultados_text.insert(tk.END, f"Endereço de Broadcast: {endereco_broadcast}\n")
            self.resultados_text.insert(tk.END, f"Classe do Endereço: {classe}\n")
            self.resultados_text.insert(tk.END, f"Endereço Público/Privado: {classificacao}\n")
            self.resultados_text.insert(tk.END, f"Número de Sub-redes Possíveis: {num_subredes}\n")
            self.resultados_text.insert(tk.END, f"Hosts válidos por Sub-rede: {qtd_hosts_por_subrede}\n")

            self.resultados_text.config(state='disabled')  # Desabilita a edição após inserir os resultados

        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    calculadora_ip = CalculadoraIP(root)
    root.mainloop()
