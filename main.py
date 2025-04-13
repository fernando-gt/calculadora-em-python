import tkinter as tk
from tkinter import StringVar, Menu, messagebox, filedialog
from PIL import Image, ImageTk
import os
import webbrowser

# Constantes para cálculos
AREA_TIJOLO = 0.2 * 0.1  # Área de um tijolo em m²
RENDIMENTO_TINTA = 10  # Rendimento da tinta em m² por litro
TENSAO = 220  # Tensão elétrica em volts

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.canvas = tk.Canvas(self, bg="#f8f9fa")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f8f9fa")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

# Funções de inicialização e utilitárias
def inicializar_variaveis():
    global resultado_concreto, resultado_tijolos, resultado_tinta, resultado_piso, resultado_eletrica, resultado_encanamento
    resultado_concreto = StringVar()
    resultado_tijolos = StringVar()
    resultado_tinta = StringVar()
    resultado_piso = StringVar()
    resultado_eletrica = StringVar()
    resultado_encanamento = StringVar()

def carregar_imagem(caminho, tamanho):
    if not os.path.exists(caminho):
        print(f"Arquivo não encontrado: {caminho}")
        return None
    try:
        imagem = Image.open(caminho)
        imagem = imagem.resize(tamanho, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagem)
    except Exception as e:
        print(f"Erro ao carregar imagem {caminho}: {e}")
        return None

def criar_botao(parent, texto, comando, imagem_caminho=None, tamanho=(30, 30)):
    imagem = None
    if imagem_caminho:
        imagem = carregar_imagem(imagem_caminho, tamanho)
    
    if not imagem:
        botao = tk.Button(parent, text=texto, command=comando, bg="#495057", 
                         fg="white", font=('Arial', 12), relief="flat", padx=10, anchor="w")
    else:
        botao = tk.Button(parent, text=texto, image=imagem, compound="left", 
                         command=comando, bg="#495057", fg="white", font=('Arial', 12), 
                         relief="flat", padx=10, anchor="w")
        botao.image = imagem
    
    botao.pack(fill="x", pady=5, padx=10)
    return botao

# Funções de navegação e interface
def mostrar_frame(frame):
    frame.pack(fill="both", expand=True)
    for f in frames.values():
        if f != frame:
            f.pack_forget()

def voltar_inicio():
    mostrar_frame(frames["inicio"])

def sobre():
    messagebox.showinfo("Sobre", "Calculadora de Materiais de Construção\nVersão 1.0\nDesenvolvido por [Seu Nome]")

def abrir_link(event):
    webbrowser.open_new("")

def abrir_planilha_orcamento():
    file_path = filedialog.askopenfilename(defaultextension=".xlsx", 
                                          filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
    if file_path:
        os.system(f'start excel "{file_path}"')

# Funções de cálculo
def calcular_concreto():
    try:
        largura = float(entry_largura_concreto.get())
        comprimento = float(entry_comprimento_concreto.get())
        altura = float(entry_altura_concreto.get())
        volume = largura * comprimento * altura
        resultado_concreto.set(f"Volume de concreto necessário: {volume:.2f} m³")
    except ValueError:
        resultado_concreto.set("Por favor, insira valores numéricos válidos.")

def calcular_tijolos():
    try:
        area_parede = float(entry_area_parede.get())
        num_tijolos = area_parede / AREA_TIJOLO
        resultado_tijolos.set(f"Número de tijolos necessários: {num_tijolos:.0f}")
    except ValueError:
        resultado_tijolos.set("Por favor, insira valores numéricos válidos.")

def calcular_tinta():
    try:
        area = float(entry_area_tinta.get())
        litros_tinta = area / RENDIMENTO_TINTA
        resultado_tinta.set(f"Litros de tinta necessários: {litros_tinta:.2f}")
    except ValueError:
        resultado_tinta.set("Por favor, insira valores numéricos válidos.")

def calcular_piso():
    try:
        largura = float(entry_largura_piso.get())
        comprimento = float(entry_comprimento_piso.get())
        area = largura * comprimento
        resultado_piso.set(f"Área de piso necessária: {area:.2f} m²")
    except ValueError:
        resultado_piso.set("Por favor, insira valores numéricos válidos.")

def calcular_eletrica():
    try:
        potencia = float(entry_potencia.get())
        corrente = potencia / TENSAO
        resultado_eletrica.set(f"Corrente necessária: {corrente:.2f} A")
    except ValueError:
        resultado_eletrica.set("Por favor, insira valores numéricos válidos.")

def calcular_encanamento():
    try:
        comprimento = float(entry_comprimento_encanamento.get())
        vazao = float(entry_vazao_encanamento.get())
        resultado_encanamento.set(f"Comprimento: {comprimento:.2f} m\nVazão: {vazao:.2f} l/s")
    except ValueError:
        resultado_encanamento.set("Por favor, insira valores numéricos válidos.")

# Configuração da Janela Principal
root = tk.Tk()
root.title("Calculadora de Materiais")
root.geometry("800x700")
root.configure(bg="#f0f4f8")

# Definindo o ícone da janela principal
logo_path = "imagens\logo.png" 
if os.path.exists(logo_path):
    try:
        logo_image = ImageTk.PhotoImage(file=logo_path)
        root.iconphoto(False, logo_image)
    except:
        pass

# Inicialização das variáveis de resultado
inicializar_variaveis()

# Menu de Navegação
menu_bar = Menu(root, bg="#343a40", fg="#ffffff")
root.config(menu=menu_bar)

# Menu "Arquivo"
menu_arquivo = Menu(menu_bar, tearoff=0, bg="#343a40", fg="#ffffff")
menu_arquivo.add_command(label="Sair", command=root.quit, accelerator="Ctrl+Q")
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)

# Menu "Cálculos"
menu_calculos = Menu(menu_bar, tearoff=0, bg="#343a40", fg="#ffffff")
menu_calculos.add_command(label="Cálculo de Concreto", command=lambda: mostrar_frame(frames["concreto"]), accelerator="Ctrl+1")
menu_calculos.add_command(label="Cálculo de Tijolos", command=lambda: mostrar_frame(frames["tijolos"]), accelerator="Ctrl+2")
menu_calculos.add_command(label="Cálculo de Tinta", command=lambda: mostrar_frame(frames["tinta"]), accelerator="Ctrl+3")
menu_calculos.add_command(label="Cálculo de Piso", command=lambda: mostrar_frame(frames["piso"]), accelerator="Ctrl+4")
menu_calculos.add_command(label="Cálculo Elétrica", command=lambda: mostrar_frame(frames["eletrica"]), accelerator="Ctrl+5")
menu_calculos.add_command(label="Cálculo Encanamento", command=lambda: mostrar_frame(frames["encanamento"]), accelerator="Ctrl+6")
menu_bar.add_cascade(label="Cálculos", menu=menu_calculos)

# Menu "Ajuda"
menu_ajuda = Menu(menu_bar, tearoff=0, bg="#343a40", fg="#ffffff")
menu_ajuda.add_command(label="Sobre", command=sobre)
menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)

# Adicionando atalhos de teclado
root.bind_all("<Control-q>", lambda event: root.quit())
root.bind_all("<Control-1>", lambda event: mostrar_frame(frames["concreto"]))
root.bind_all("<Control-2>", lambda event: mostrar_frame(frames["tijolos"]))
root.bind_all("<Control-3>", lambda event: mostrar_frame(frames["tinta"]))
root.bind_all("<Control-4>", lambda event: mostrar_frame(frames["piso"]))
root.bind_all("<Control-5>", lambda event: mostrar_frame(frames["eletrica"]))
root.bind_all("<Control-6>", lambda event: mostrar_frame(frames["encanamento"]))

# Frame de Navegação Lateral
frame_navegacao = tk.Frame(root, bg="#343a40", width=200)
frame_navegacao.pack(side="left", fill="y")

# Container principal para os frames
container = tk.Frame(root, bg="#f0f4f8")
container.pack(side="right", fill="both", expand=True)

# Dicionário para armazenar os frames
frames = {}

# Criar todos os frames
for nome in ["inicio", "concreto", "tijolos", "tinta", "piso", "eletrica", "encanamento"]:
    frame = ScrollableFrame(container)
    frame.pack(fill="both", expand=True)
    frames[nome] = frame
    frame.pack_forget()  # Esconder todos inicialmente

# Frame de Início
label_inicio = tk.Label(frames["inicio"].scrollable_frame, 
                       text="Bem-vindo à Calculadora de Materiais de Construção", 
                       font=("Arial", 24, "bold"), bg="#f0f4f8", fg="#343a40")
label_inicio.pack(pady=50)

# Frame de Concreto
label_concreto = tk.Label(frames["concreto"].scrollable_frame, 
                         text="Cálculo de Concreto", 
                         font=("Arial", 24, "bold"), bg="#f0f4f8", fg="#343a40")
label_concreto.pack(pady=20)

tk.Label(frames["concreto"].scrollable_frame, text="Largura (m):", bg="#f0f4f8", fg="#343a40", font=("Arial", 14)).pack(pady=5)
entry_largura_concreto = tk.Entry(frames["concreto"].scrollable_frame, font=("Arial", 14))
entry_largura_concreto.pack(pady=5)

tk.Label(frames["concreto"].scrollable_frame, text="Comprimento (m):", bg="#f0f4f8", fg="#343a40", font=("Arial", 14)).pack(pady=5)
entry_comprimento_concreto = tk.Entry(frames["concreto"].scrollable_frame, font=("Arial", 14))
entry_comprimento_concreto.pack(pady=5)

tk.Label(frames["concreto"].scrollable_frame, text="Altura (m):", bg="#f0f4f8", fg="#343a40", font=("Arial", 14)).pack(pady=5)
entry_altura_concreto = tk.Entry(frames["concreto"].scrollable_frame, font=("Arial", 14))
entry_altura_concreto.pack(pady=5)

btn_calcular_concreto = tk.Button(frames["concreto"].scrollable_frame, text="Calcular", command=calcular_concreto, 
                                 font=("Arial", 14), bg="#007bff", fg="white")
btn_calcular_concreto.pack(pady=20)

resultado_concreto_label = tk.Label(frames["concreto"].scrollable_frame, textvariable=resultado_concreto, 
                                   font=("Arial", 14), bg="#f0f4f8", fg="#343a40")
resultado_concreto_label.pack(pady=10)

btn_planilha_concreto = tk.Button(frames["concreto"].scrollable_frame, text="Abrir Planilha", 
                                 command=abrir_planilha_orcamento, font=("Arial", 14), bg="#28a745", fg="white")
btn_planilha_concreto.pack(pady=10)

btn_voltar_inicio_concreto = tk.Button(frames["concreto"].scrollable_frame, text="Voltar", 
                                      command=voltar_inicio, font=("Arial", 14), bg="#dc3545", fg="white")
btn_voltar_inicio_concreto.pack(pady=10)

# Frame de Tijolos (padrão similar para os outros frames)
label_tijolos = tk.Label(frames["tijolos"].scrollable_frame, 
                        text="Cálculo de Tijolos", 
                        font=("Arial", 24, "bold"), bg="#f0f4f8", fg="#343a40")
label_tijolos.pack(pady=20)

tk.Label(frames["tijolos"].scrollable_frame, text="Área da parede (m²):", bg="#f0f4f8", fg="#343a40", font=("Arial", 14)).pack(pady=5)
entry_area_parede = tk.Entry(frames["tijolos"].scrollable_frame, font=("Arial", 14))
entry_area_parede.pack(pady=5)

btn_calcular_tijolos = tk.Button(frames["tijolos"].scrollable_frame, text="Calcular", command=calcular_tijolos, 
                                font=("Arial", 14), bg="#007bff", fg="white")
btn_calcular_tijolos.pack(pady=20)

resultado_tijolos_label = tk.Label(frames["tijolos"].scrollable_frame, textvariable=resultado_tijolos, 
                                  font=("Arial", 14), bg="#f0f4f8", fg="#343a40")
resultado_tijolos_label.pack(pady=10)

btn_planilha_tijolos = tk.Button(frames["tijolos"].scrollable_frame, text="Abrir Planilha", 
                                command=abrir_planilha_orcamento, font=("Arial", 14), bg="#28a745", fg="white")
btn_planilha_tijolos.pack(pady=10)

btn_voltar_inicio_tijolos = tk.Button(frames["tijolos"].scrollable_frame, text="Voltar", 
                                     command=voltar_inicio, font=("Arial", 14), bg="#dc3545", fg="white")
btn_voltar_inicio_tijolos.pack(pady=10)

# [Continuação similar para os outros frames: tinta, piso, eletrica, encanamento]

# Adicionando botões de navegação
criar_botao(frame_navegacao, "Início", lambda: mostrar_frame(frames["inicio"]), "imagens/home.jpg")
criar_botao(frame_navegacao, "Concreto", lambda: mostrar_frame(frames["concreto"]), "imagens/concreto.jpg")
criar_botao(frame_navegacao, "Tijolos", lambda: mostrar_frame(frames["tijolos"]), "imagens/tijolos.jpg")
criar_botao(frame_navegacao, "Tinta", lambda: mostrar_frame(frames["tinta"]), "imagens/tinta.jpg")
criar_botao(frame_navegacao, "Piso", lambda: mostrar_frame(frames["piso"]), "imagens/piso.jpg")
criar_botao(frame_navegacao, "Elétrica", lambda: mostrar_frame(frames["eletrica"]), "imagens/eletrica.jpg")
criar_botao(frame_navegacao, "Encanamento", lambda: mostrar_frame(frames["encanamento"]), "imagens/encanamento.jpg")

# Mostrar o frame inicial
mostrar_frame(frames["inicio"])

root.mainloop()