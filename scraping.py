from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import math
import pandas as pd
import os

def config_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--start-maximized')
    return webdriver.Chrome(options=options)

def salvar_arquivo(dict_produtos):
    df = pd.DataFrame(dict_produtos)
    try:
        # Define o diretório de salvamento padrão de Downloads Windows e Linux
        save_dir = os.path.expanduser('~/Downloads')

        # Cria o caminho completo para o arquivo
        save_path = os.path.join(save_dir, 'preco_gpu.xlsx')

        # Salva o DataFrame no formato .xlsx
        df.to_excel(save_path, index=False)

        print(f"Arquivo salvo com sucesso em: {save_path}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")


def raspagem_de_dados():
    driver = config_webdriver()
    # Carregando a URL
    url = ''
    driver.get(url)

    try:
        # Espera o elemento aparecer
        qtd_itens = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'listingCount'))
        )
        
        # Extrai apenas o número e converte para inteiro
        qtd_itens_text = qtd_itens.text.strip() # remove espaços em branco
        qtd_itens_num = int(re.search(r'\d+', qtd_itens_text).group()) # pega o primeiro número encontrado
        

        
        ultima_pagina = math.ceil(int(qtd_itens_num)/20)

        dict_produtos = {'marca':[], 'preco':[]}

        for i in range(1, ultima_pagina+1):
            produtos = driver.find_elements(By.CLASS_NAME, 'productCard')

            for produto in produtos:
                marca = produto.find_element(By.CLASS_NAME, 'nameCard').text.strip()
                preco = produto.find_element(By.CLASS_NAME, 'priceCard').text.strip()

                dict_produtos['marca'].append(marca)
                dict_produtos['preco'].append(preco)
    
        driver.quit()
        return dict_produtos
    
    except Exception as e:
        print(f"Erro: {e}")
                
    

def main():
    dict_produtos = raspagem_de_dados()
    salvar_arquivo(dict_produtos)
    
main()


        


