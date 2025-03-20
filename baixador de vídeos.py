import tkinter as tk
from tkinter import StringVar, messagebox
import re 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui as pa
import time

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Baixador de Vídeos")
        self.root.geometry("650x350")
        self.root.resizable(False, False)
        
        self.links = {"instagram": [], "youtube": [], "tiktok": []}
        
        tk.Label(root, text="baixador de vídeos", font=("Arial", 14)).pack(pady=10)
        
        self.create_input("Instagram", "instagram", 0)
        self.create_input("YouTube", "youtube", 1)
        self.create_input("TikTok", "tiktok", 2)
        
        self.run_button = tk.Button(root, text="Rodar", command=self.run_downloads)
        self.run_button.pack(pady=10)
    
    def create_input(self, label_text, platform, position):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        
        tk.Label(frame, text=label_text, font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=2)
        
        entry_var = StringVar()
        entry = tk.Entry(frame, textvariable=entry_var, width=40)
        entry.grid(row=1, column=0)
        
        label_count = tk.Label(frame, text=f"links adicionados: 0")
        label_count.grid(row=1, column=1, padx=10)
        
        entry.bind("<Return>", lambda event, p=platform, var=entry_var, lbl=label_count: self.add_link(p, var, lbl))
    
    def validate_link(self, platform, link):
        patterns = {
            "instagram": r"",
            "youtube": r"https://www\.youtube\.com/shorts/[A-Za-z0-9_-]+",
            "tiktok": r"https://www\.tiktok\.com/@[A-Za-z0-9_.-]+/video/[0-9]+"
        }
        return re.match(patterns.get(platform, ""), link)
    
    def add_link(self, platform, entry_var, label_count):
        link = entry_var.get().strip()
        if link:
            if self.validate_link(platform, link):
                self.links[platform].append(link)
                entry_var.set("")  # Limpa o input
                label_count.config(text=f"links adicionados: {len(self.links[platform])}")
            else:
                messagebox.showerror("Erro", "Erro: link não suportado, tente novamente com outro link")
    def process_next_video(self):
        for platform, links in self.links.items():

            if links:
                link = links.pop(0)  
                print(f"Baixando vídeo: {link} da plataforma {platform}")

                options = webdriver.ChromeOptions()
                options.add_experimental_option("detach", True) 
                driver = webdriver.Chrome(options=options)


                if platform == 'instagram':
                    driver.get('https://saveclip.app/pt')

                    # Insere o link na caixa de entrada
                    linkInput = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/form/div/input")
                    linkInput.send_keys(link)

                    # Clica no botão de gerar link de download
                    downloadButton = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div/form/div/div/button')
                    downloadButton.click()

                    wait = WebDriverWait(driver, 15)

                    elemento = None

                    # 1) Tentar localizar por XPATH com o texto "Baixar video"
                    try:
                        elemento = wait.until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//a[contains(., 'Baixar video')]")
                            )
                        )
                    except:
                        pass

                    # 2) Se não encontrou, tentar por LINK_TEXT exato "Baixar video"
                    if not elemento:
                        try:
                            elemento = wait.until(
                                EC.presence_of_element_located(
                                    (By.LINK_TEXT, "Baixar video")
                                )
                            )
                        except:
                            pass

                    # 3) Se ainda não encontrou, tentar por PARTIAL_LINK_TEXT: "Baixar"
                    if not elemento:
                        try:
                            elemento = wait.until(
                                EC.presence_of_element_located(
                                    (By.PARTIAL_LINK_TEXT, "Baixar")
                                )
                            )
                        except:
                            pass

                    # 4) Tentar por CSS_SELECTOR (classe + atributo title)
                    if not elemento:
                        try:
                            elemento = wait.until(
                                EC.presence_of_element_located(
                                    (
                                        By.CSS_SELECTOR,
                                        "a.abutton.is-success.is-fullwidth.btn-premium.mt-3[title='Download Video 1']"
                                    )
                                )
                            )
                        except:
                            pass

                    # 5) Tentar por XPATH usando classe e atributo title
                    if not elemento:
                        try:
                            elemento = wait.until(
                                EC.presence_of_element_located(
                                    (
                                        By.XPATH,
                                        "//a[@class='abutton is-success is-fullwidth btn-premium mt-3' and @title='Download Video 1']"
                                    )
                                )
                            )
                        except:
                            pass

                    # Se todas as tentativas falharem, gerar exceção
                    if not elemento:
                        raise Exception("Não foi possível encontrar o elemento de download.")

                    # Rolamos a página até o elemento
                    driver.execute_script("arguments[0].scrollIntoView(true);", elemento)

                    # Extrai o link do atributo href
                    downloadLink = elemento.get_attribute("href")
                    driver.quit()


                    # Abre o link no navegador padrão
                    baixador = webdriver.Chrome(options=options)
                    baixador.get(downloadLink)
                    time.sleep(1)
                    pa.press('enter')
                    baixador.quit()

                elif platform == 'tiktok':
                    driver.get('https://ssstik.io/pt')

                    inputLink = driver.find_element(By.XPATH, "/html/body/main/section/div/div/form/div[2]/input[1]")
                    inputLink.send_keys(link)

                    downloadButton = driver.find_element(By.XPATH, '/html/body/main/section/div/div/form/div[2]/button[3]')
                    downloadButton.click()

                    wait = WebDriverWait(driver, 15)
                    downloadElement = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/section/div/div/div[3]/div/div/div[2]/a[1]")))
                    time.sleep(2)
                    downloadLink = downloadElement.get_attribute("href")
                    driver.quit()

                    baixador = webdriver.Chrome(options=options)
                    baixador.get(downloadLink)
                    time.sleep(5)
                    baixador.quit()

                elif platform == 'youtube':
                    driver.get('https://en.greenconvert.net/')

                    inputLink = driver.find_element(By.XPATH, "/html/body/main/section[1]/div[1]/div[2]/input")
                    inputLink.send_keys(link)

                    downloadButton = driver.find_element(By.XPATH, "/html/body/main/section[1]/div[1]/div[2]/div/button")
                    downloadButton.click()


                    wait = WebDriverWait(driver, 40)
                    downloadElement = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/section[1]/div[1]/div[7]/div[2]/div/div[2]/div/div[1]/select/optgroup[2]/option[2]")))
                    downloadElement.click()

                    downloadButton2 = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/main/section[1]/div[1]/div[7]/div[2]/div/div[2]/div/div[1]/div/button[2]")))
                    downloadButton2.click()
                    time.sleep(10)

                    downloadNow =  driver.find_element(By.XPATH, "/html/body/main/section[1]/div[1]/div[7]/div[2]/div/div[2]/div/div[2]/a[1]")
                    downloadNow.click()
                    
                    driver.quit
                    time.sleep(3)
                    pa.press('enter')
                return link, platform

        print("Nenhum link restante para processar.")
        return None, None

    
    def run_downloads(self):
        print("Iniciando downloads dos vídeos...")
        while True:
            link, platform = self.process_next_video()
            if link is None:
                break  # Sai do loop quando não houver mais links para processar
            
            # Aqui é onde você pode chamar sua automação para abrir o navegador e baixar o vídeo.
            print(f"Iniciando download de: {link} ({platform})")
        
        print("Todos os downloads foram concluídos!")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()