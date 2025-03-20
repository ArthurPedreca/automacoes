from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import pyautogui as pa
import time
import pyperclip
import tkinter as tk
from tkinter import messagebox




def responder():
    # Configurações do Chrome (mantém o navegador aberto)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    # Abre o formulário
    driver.get('https://docs.google.com/forms/d/e/1FAIpQLSdGJ1z1Asb2TYjrkSPHjFWtVKeypzfK9kPuoOye7RsdiMwzYg/viewform')

    # Aguarda até que pelo menos um elemento com a classe "M7eMe" seja carregado
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "M7eMe")))

    # Encontra todos os containers que possuam um elemento <span> com a classe "M7eMe"
    question_containers = driver.find_elements(By.XPATH, "//div[.//span[contains(@class, 'M7eMe')]]")

    def detect_question_type(container):
        """
        Identifica o tipo da pergunta:
        - Se houver <input type="text"> ou <textarea>, retorna "escrever".
        - Se houver <input type="radio">, <input type="checkbox"> ou labels com alternativas, retorna "assinalar".
        """
        if container.find_elements(By.XPATH, ".//input[@type='text']") or container.find_elements(By.TAG_NAME, "textarea"):
            return "escrever"
        if container.find_elements(By.XPATH, ".//input[@type='radio']") or container.find_elements(By.XPATH, ".//input[@type='checkbox']"):
            return "assinalar"
        alt_labels = container.find_elements(By.XPATH, ".//label[contains(@class, 'docssharedWizToggleLabeledContainer')]")
        if alt_labels:
            return "assinalar"
        return "indefinido"

    def extract_alternatives(container):
        """
        Extrai as alternativas da pergunta do tipo "assinalar".
        Procura por todos os labels com a classe característica e extrai o texto do span com o atributo dir="auto".
        """
        alternativas = []
        alt_labels = container.find_elements(By.XPATH, ".//label[contains(@class, 'docssharedWizToggleLabeledContainer')]")
        for label in alt_labels:
            try:
                alt_text = label.find_element(By.XPATH, ".//span[@dir='auto']").text.strip()
                if alt_text and alt_text not in alternativas:
                    alternativas.append(alt_text)
            except Exception:
                continue
        return alternativas

    # Usaremos um dicionário para evitar duplicatas (chave: texto da pergunta)
    unique_questions = {}

    for container in question_containers:
        try:
            # Extrai o texto da pergunta (geralmente dentro de um <span> com a classe "M7eMe")
            question_text = container.find_element(By.XPATH, ".//span[contains(@class, 'M7eMe')]").text.strip()
        except Exception:
            continue  # Pula se não conseguir extrair o texto

        q_type = detect_question_type(container)
        entry = {"pergunta": question_text, "tipo": q_type}
        
        if q_type == "assinalar":
            alternativas = extract_alternatives(container)
            if alternativas:
                entry["alternativas"] = alternativas
        
        # Se a pergunta já estiver no dicionário, verifica se a nova entrada é mais completa
        if question_text in unique_questions:
            existing = unique_questions[question_text]
            # Se a versão existente for "indefinido" e a nova for "assinalar" com alternativas, substitui
            if existing["tipo"] == "indefinido" and q_type == "assinalar" and "alternativas" in entry:
                unique_questions[question_text] = entry
        else:
            unique_questions[question_text] = entry

    # Converte para lista
    data = list(unique_questions.values())

    # Salva os dados em um arquivo JSON
    with open("perguntas.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    main_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "o3Dpx")))
    question_count = len(main_div.find_elements(By.XPATH, "./div"))
    print(f"Número de perguntas no formulário: {question_count}")

    for i in range(question_count):
        print(f"Respondendo a pergunta {i + 1} de {question_count}")
        # print("Dados salvos em perguntas.json")
        # print(data)

        #abre o chrome
        pa.press('win')
        pa.write('Chrome')
        time.sleep(2)
        pa.press('enter')
        #pesquisa pelo chatgpt
        time.sleep(2)
        pa.write('chatgpt.com')
        pa.press('enter')
        time.sleep(2)
        #fecha um popup chato
        pa.press('tab')
        pa.press('tab')
        pa.press('enter')
        pa.click(689, 111)
        time.sleep(2)
        #pega o dado da PRIMEIRA pergunta do forms
        pergunta = data[i]['pergunta']
        tipo = data[i]['tipo']
        alternativas = ", ".join(data[i].get("alternativas", []))
        print(alternativas)
        if tipo == 'escrever':
            pergunta_completa = f"Eu vou te fazer uma pergunta, escreva uma resposta simples e curta: {pergunta}. Você deve escrever somente o texto com a resposta da pergunta e nada mais"
        elif tipo == 'assinalar':
            pergunta_completa = f"Eu vou te fazer uma pergunta com alternativas, e você deve escrever somente a alternativa certa: {pergunta}, Alternativas: {alternativas}"
        #escreve a pergunta para  chat responder
        pa.write(pergunta_completa)
        pa.press('enter')
        time.sleep(6)
        #pressiona o botao de copiar que aparece embaixo da resposta
        pa.click(689, 111)
        pa.press('tab')
        pa.press('tab')
        pa.press('tab')
        pa.press('tab')
        pa.press('tab')
        pa.press('enter')
        pa.hotkey('alt', 'f4')

        if tipo == 'escrever': 
            try:
                input = driver.find_element(By.XPATH, f"/html/body/div/div[2]/form/div[2]/div/div[2]/div[{i+1}]/div/div/div[2]/div/div[1]/div[2]/textarea")
                clipboard_content = pyperclip.paste()
                input.send_keys(clipboard_content)
            except:
                input = driver.find_element(By.XPATH, f"/html/body/div/div[2]/form/div[2]/div/div[2]/div[{i+1}]/div/div/div[2]/div/div[1]/div/div[1]/input")
                clipboard_content = pyperclip.paste()
                input.send_keys(clipboard_content)
            
        elif tipo == 'assinalar':
            elements = driver.find_elements(By.CSS_SELECTOR, ".nWQGrd")

            for element in elements:
                try:
                    span = element.find_element(By.TAG_NAME, "span")
                    clipboard_content = pyperclip.paste()
                    print(clipboard_content)
                    if span.text.strip().lower() == clipboard_content.strip().lower():
                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", element)
                        time.sleep(1)
                        element.click()
                        print(f"Cliquei no elemento contendo {clipboard_content}")
                        break
                except:
                    print('nao consegui clicar, sou um lixo')
                    continue

    botaoEnviar = driver.find_element(By.XPATH, "/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span")
    botaoEnviar.click()


# Cria a janela principal
root = tk.Tk()
root.title("Interface para Google Forms")
root.geometry("500x150")

# Rótulo para instrução
label = tk.Label(root, text="Digite o link do Google Forms:")
label.pack(pady=10)

# Campo de entrada para o link
entry_link = tk.Entry(root, width=60)
entry_link.pack(pady=5)

# Botão que, ao ser clicado, chama a função 'responder'
button_responder = tk.Button(root, text="Responder", command=responder)
button_responder.pack(pady=20)

# Inicia o loop da interface
root.mainloop()