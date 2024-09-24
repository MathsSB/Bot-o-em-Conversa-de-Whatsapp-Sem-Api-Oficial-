import customtkinter as ctk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def enviar_mensagem(numero, mensagem, driver):
    url = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem}"
    driver.get(url)
    print(f"Abrindo conversa com {numero}...")

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
        )
        print(f"Campo de mensagem encontrado para {numero}.")
        time.sleep(5)  # Aguarde um momento para garantir que o campo esteja visível

        # Usar JavaScript para simular o envio de mensagem
        driver.execute_script("document.querySelector('span[data-icon=\"send\"]').click();")
        print(f"Mensagem enviada para {numero}.")
        time.sleep(5)  # Aguarde um momento após o envio
    except Exception as e:
        print(f"Erro ao enviar mensagem para {numero}: {e}")

def enviar_mensagens():
    driver_path = r'C:\Users\Maths\Desktop\chromedriver-win64\chromedriver.exe'
    service = Service(driver_path)
    global driver
    driver = webdriver.Chrome(service=service)
    driver.get('https://web.whatsapp.com')
    status_label.config(text="WhatsApp Web aberto. Escaneie o QR Code e clique em 'Estou Logado' quando estiver pronto...")
    root.update()
    root.wait_variable(login_done_var)

    mensagem = mensagem_entry.get("1.0", ctk.END).strip()  # Obter a mensagem diretamente do CTkTextbox
    leads = [lead.strip() for lead in leads_text.get("1.0", ctk.END).strip().split('\n')]
    for lead in leads:
        enviar_mensagem(lead, mensagem, driver)
    
    status_label.config(text="Todas as mensagens foram enviadas.")
    # Manter a página do WhatsApp aberta
    # driver.quit()

def open_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        with open(filepath, 'r') as file:
            leads_text.delete('1.0', ctk.END)
            leads_text.insert(ctk.END, file.read())

def mark_as_logged_in():
    login_done_var.set(True)

# Configuração da janela principal
root = ctk.CTk()
root.title("Envio de Mensagens WhatsApp")
root.geometry("800x600")  # Aumentando o tamanho da janela
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

login_done_var = ctk.BooleanVar()

# Layout da interface
ctk.CTkLabel(root, text="Cole ou insira números de telefone, um por linha:", font=("Arial", 12)).pack(pady=10)
leads_text = ctk.CTkTextbox(root, height=15, width=90)  # Aumentando a altura e largura
leads_text.pack(pady=5)

ctk.CTkLabel(root, text="Escolha a mensagem a ser enviada:", font=("Arial", 12)).pack(pady=10)
mensagem_entry = ctk.CTkTextbox(root, height=10, width=90)  # Aumentando a altura da caixa de texto
mensagem_entry.pack(pady=5)
mensagem_entry.insert(ctk.END, "Olá, esta é uma mensagem de teste.")  # Definir texto padrão

ctk.CTkButton(root, text="Carregar de Arquivo", command=open_file, width=200).pack(pady=10)
ctk.CTkButton(root, text="Enviar Mensagens", command=enviar_mensagens, width=200).pack(pady=10)

ctk.CTkLabel(root, text="Depois de escanear o QR Code, clique no botão abaixo para continuar:", font=("Arial", 12)).pack(pady=10)
ctk.CTkButton(root, text="Estou Logado", command=mark_as_logged_in, width=200).pack(pady=10)

status_label = ctk.CTkLabel(root, text="", font=("Arial", 12))
status_label.pack(pady=10)

root.mainloop()
