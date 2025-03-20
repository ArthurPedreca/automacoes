import tkinter as tk
from tkinter import ttk,  messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

class PriceMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Preços")
        
        # Campo de entrada
        self.label = ttk.Label(root, text="Digite o produto:")
        self.label.pack(pady=10)
        
        self.entry = ttk.Entry(root, width=50)
        self.entry.pack()
        
        # Botão de busca
        self.button = ttk.Button(root, text="Buscar", command=self.start_search)
        self.button.pack(pady=10)
        
        # Tabela de resultados
        self.tree = ttk.Treeview(root, columns=("Site", "Produto", "Preço", "Link"), show="headings")
        self.tree.heading("Site", text="Site")
        self.tree.heading("Produto", text="Produto")
        self.tree.heading("Preço", text="Preço (R$)")
        self.tree.heading("Link", text="Link")
        self.tree.pack(fill="both", expand=True)

        # Botão de exportar para Excel (canto inferior direito)
        self.export_button = ttk.Button(root, text="Exportar Arquivo Excel", command=self.export_to_excel)
        self.export_button.pack(side="right", anchor="se", padx=10, pady=10)

    def start_search(self):
        product = self.entry.get()
        self.search_mercado_livre(product)  
        self.search_amazon(product)  
        self.search_aliexpress(product)  
        self.search_magalu(product)  

    def search_mercado_livre(self, product):
        driver = webdriver.Chrome()
        driver.get(f"https://lista.mercadolivre.com.br/{product.replace(' ', '-')}")
        driver.maximize_window()
        
        time.sleep(3)
        elementoChato  =  driver.find_element(By.XPATH, "/html/body/div[5]/div")
        driver.execute_script("arguments[0].style.display = 'none';", elementoChato)

        elementoChato2 = driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div")
        driver.execute_script("arguments[0].style.display = 'none';", elementoChato2)

        name = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/section/ol/li[1]/div/div/div[2]/h3/a").text
        try:
            price = driver.find_element(By.CSS_SELECTOR, ".andes-money-amount__fraction").text
        except:
            price = driver.find_element(By.CSS_SELECTOR, ".price-tag-fraction").text 
        link = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/section/ol/li[1]/div/div/div[2]/h3/a").get_attribute("href")
        
        self.tree.insert("", "end", values=("Mercado Livre", name, f"R$ {price}", link))
        
        driver.quit()

    def search_amazon(self, product):
        driver = webdriver.Chrome()
        driver.get(f"https://www.amazon.com.br/s?k={product.replace(' ', '+')}")
        driver.maximize_window()
        time.sleep(3)

        name = driver.find_element(By.CSS_SELECTOR, "h2.a-size-base-plus.a-spacing-none.a-color-base.a-text-normal span").text
        price = driver.find_element(By.CSS_SELECTOR, ".a-price-whole").text
        try:
            link = driver.find_element(By.XPATH, 
                "/html/body/div[1]/div[1]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/div/div/span/div/div/div[2]/div[2]/a"
            ).get_attribute("href")  
        except: 
            link = 'Não foi possível pegar o link'

        self.tree.insert("", "end", values=("Amazon", name, f"R$ {price}", link))
        driver.quit()
        
    def search_magalu(self, product):
        driver = webdriver.Chrome()
        driver.get(f"https://www.magazineluiza.com.br/busca/{product.replace(' ', '+')}")
        driver.maximize_window()
        time.sleep(2)

        name = driver.find_element(By.CSS_SELECTOR, "h2[data-testid='product-title']").text
        price = driver.find_element(By.CSS_SELECTOR, "p[data-testid='price-value']").text
        price = price.replace("ou ", "").strip()
            
        link_element = driver.find_element(By.CSS_SELECTOR, "a[data-testid='product-card-container']")
        link = link_element.get_attribute("href")

        self.tree.insert("", "end", values=("Magazine Luiza", name, f"R$ {price}", link))
        driver.quit()
        messagebox.showerror('Mensagem', 'Dados Coletados!')


    def search_aliexpress(self, product):
        driver = webdriver.Chrome()
        driver.get(f"https://pt.aliexpress.com/wholesale?SearchText={product.replace(' ', '+')}")
        driver.maximize_window()
        time.sleep(3)

        name = driver.find_element(By.CSS_SELECTOR, ".multi--titleText--nXeOvyr").text
        link = driver.find_element(By.XPATH, 
            "/html/body/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div/div/a"
        ).get_attribute("href")

        # Captura o segundo elemento <span> do bloco de preço
        price = driver.find_element(By.CSS_SELECTOR, "div.multi--price-sale--U-S0jtj span:nth-of-type(2)").text
        
        self.tree.insert("", "end", values=("AliExpress", name, f"R$ {price}", link))
        driver.quit()

    def export_to_excel(self):
        # Coleta todos os itens da Treeview
        items = self.tree.get_children()
        dados = []
        
        # Percorre cada linha (item) e pega os valores (Site, Produto, Preço, Link)
        for item in items:
            valores = self.tree.item(item, "values")
            dados.append(valores)
        
        # Converte para DataFrame
        df = pd.DataFrame(dados, columns=["Site", "Produto", "Preço", "Link"])
        
        # Define o caminho para a Área de Trabalho (Desktop)
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # Salva em planilha Excel na Área de Trabalho
        filepath = os.path.join(desktop_path, "produtos.xlsx")
        df.to_excel(filepath, index=False)

        print("Arquivo Excel exportado com sucesso na Área de Trabalho!")

# Executar a aplicação
root = tk.Tk()
app = PriceMonitorApp(root)
root.mainloop()
