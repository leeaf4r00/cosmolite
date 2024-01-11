import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
imprt threading
import webbrowser
from requests.exceptions import RequestException
import json
from selenium import webdriver
from ort os
imposelenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Produto:
    def __init__(self, name, price, image_url):
        self.name = name
        self.price = price
        self.image_url = image_url


def get_product_data(gtin):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    headers = {'User-Agent': user_agent}
    url = f'https://cosmos.bluesoft.com.br/produtos/{gtin}'

    try:
        page = requests.get(url, headers=headers, timeout=10)
        page.raise_for_status()
    except RequestException as e:
        print(f"Erro ao fazer a solicitação: {e}")
        return None

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        product_name_elem = soup.find('h1', class_='product-name')
        product_price_elem = soup.find('span', class_='price')
        product_image_elem = soup.find('div', class_='product-image')

        if product_name_elem and product_price_elem and product_image_elem:
            product_name = product_name_elem.get_text().strip()
            product_price = product_price_elem.get_text().strip()
            product_image_url = product_image_elem.find('img')['src'].strip()

            return Produto(name=product_name, price=product_price, image_url=product_image_url)

    return None


def search_product_thread():
    gtin = gtin_var.get()
    if not gtin.isdigit():
        messagebox.showerror("Erro", "O GTIN deve conter apenas números.")
        return

    get_info_button.config(state=tk.DISABLED)
    loading_label.config(text="Obtendo informações...")
    product_info_frame.pack_forget()
    progress_bar.start()

    t = threading.Thread(target=get_product_info, args=(gtin,))
    t.start()


def get_product_info(gtin):
    product = get_product_data(gtin)
    if product:
        if gtin_var.get() == gtin:
            root.after(0, update_product_info, product)
        else:
            loading_label.config(text="")
            progress_bar.stop()
    else:
        name_label.config(
            text=f"Não foi possível obter informações para o GTIN {gtin}.")
        price_label.config(text="")
        image_label.config(image="")
        loading_label.config(text="")
        progress_bar.stop()

    get_info_button.config(state=tk.NORMAL)


def update_product_info(product):
    name_label.config(text=f"Nome do produto: {product.name}")
    price_label.config(text=f"Preço do produto: {product.price}")

    image_path = os.path.join(image_dir_var.get(), f"{gtin_var.get()}.png")
    if not os.path.exists(image_path):
        try:
            image_response = requests.get(product.image_url, timeout=10)
            image_response.raise_for_status()
            with open(image_path, 'wb') as f:
                f.write(image_response.content)
        except RequestException as e:
            print(f"Erro ao salvar a imagem: {e}")
            image_path = "default_image.png"

    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Erro ao abrir a imagem: {e}")
        img = Image.open("default_image.png")

    if auto_resize_var.get() == 1:
        img.thumbnail((250, 250))

    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img

    product_info_frame.pack(pady=10)
    loading_label.config(text="")
    progress_bar.stop()


def clear_product_info():
    gtin_var.set("")
    name_label.config(text="")
    price_label.config(text="")
    image_label.config(image="")
    loading_label.config(text="")
    product_info_frame.pack_forget()
    progress_bar.stop()


def open_product_page():
    gtin = gtin_var.get()
    if not gtin.isdigit():
        return

    product_url = f"https://cosmos.bluesoft.com.br/produtos/{gtin}"
    webbrowser.open_new(product_url)


def toggle_auto_resize():
    if auto_resize_var.get() == 1:
        resize_label.config(state=tk.NORMAL)
    else:
        resize_label.config(state=tk.DISABLED)


def save_settings():
    settings = {
        "image_dir": image_dir_var.get(),
        "auto_resize": auto_resize_var.get()
    }
    with open("settings.json", "w") as f:
        json.dump(settings, f)


def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r", encoding="utf-8") as f:
            settings = json.load(f)
            image_dir_var.set(settings.get("image_dir", "product_images"))
            auto_resize_var.set(settings.get("auto_resize", 1))
    else:
        image_dir_var.set("product_images")
        auto_resize_var.set(1)
        

def get_product_data_selenium(gtin):
    driver = webdriver.Chrome()
    url = f'https://cosmos.bluesoft.com.br/produtos/{gtin}'

    try:
        driver.get(url)

        # Esperar até que o elemento "product-name" esteja presente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'product-name'))
        )

        product_name_elem = driver.find_element(By.CLASS_NAME, 'product-name')
        product_price_elem = driver.find_element(By.CLASS_NAME, 'price')
        product_image_elem = driver.find_element(By.CLASS_NAME, 'product-image')
        
        product_name = product_name_elem.text.strip()
        product_price = product_price_elem.text.strip()
        product_image_url = product_image_elem.find_element(By.TAG_NAME, 'img').get_attribute('src').strip()

        driver.quit()
        return Produto(name=product_name, price=product_price, image_url=product_image_url)

    except Exception as e:
        print(f"Erro ao obter informações usando Selenium: {e}")
        driver.quit()
        return None
    
def search_product_thread_selenium():
    gtin = gtin_var.get()
    if not gtin.isdigit():
        messagebox.showerror("Erro", "O GTIN deve conter apenas números.")
        return

    get_info_button.config(state=tk.DISABLED)
    loading_label.config(text="Obtendo informações...")
    product_info_frame.pack_forget()
    progress_bar.start()

    t = threading.Thread(target=get_product_info_selenium, args=(gtin,))
    t.start()


def get_product_info_selenium(gtin):
    product = get_product_data_selenium(gtin)
    if product:
        if gtin_var.get() == gtin:
            root.after(0, update_product_info, product)
        else:
            loading_label.config(text="")
            progress_bar.stop()
    else:
        name_label.config(
            text=f"Não foi possível obter informações para o GTIN {gtin}.")
        price_label.config(text="")
        image_label.config(image="")
        loading_label.config(text="")
        progress_bar.stop()

    get_info_button.config(state=tk.NORMAL)


root = tk.Tk()
root.title("Informações de Produto")
root.geometry("600x400")

main_frame = ttk.Frame(root)
main_frame.pack(pady=20, padx=20)

image_dir_var = tk.StringVar()
auto_resize_var = tk.IntVar()
load_settings()

gtin_var = tk.StringVar()
gtin_frame = ttk.Frame(main_frame)
gtin_frame.pack(pady=10)

gtin_label = ttk.Label(gtin_frame, text="Insira o código de barras (GTIN):")
gtin_label.grid(row=0, column=0, padx=5, pady=5)

gtin_entry = ttk.Entry(gtin_frame, textvariable=gtin_var)
gtin_entry.grid(row=0, column=1, padx=5, pady=5)

get_info_button = ttk.Button(
    gtin_frame, text="Obter Informações", command=search_product_thread_selenium)
get_info_button.grid(row=0, column=2, padx=5, pady=5)

clear_button = ttk.Button(gtin_frame, text="Limpar",
                          command=clear_product_info)
clear_button.grid(row=0, column=3, padx=5, pady=5)

product_info_frame = ttk.Frame(main_frame)

loading_label = ttk.Label(main_frame, text="")
loading_label.pack(pady=5)

name_label = ttk.Label(product_info_frame, text="")
name_label.pack(pady=5)

price_label = ttk.Label(product_info_frame, text="")
price_label.pack(pady=5)

image_label = ttk.Label(product_info_frame, text="")
image_label.pack(pady=10)

progress_bar = ttk.Progressbar(main_frame, mode="indeterminate")
progress_bar.pack(pady=5)

open_page_button = ttk.Button(
    product_info_frame, text="Ver no site", command=open_product_page)
open_page_button.pack(pady=5)

settings_frame = ttk.LabelFrame(main_frame, text="Configurações")
settings_frame.pack(pady=10)

image_dir_label = ttk.Label(
    settings_frame, text="Caminho para salvar imagens:")
image_dir_label.grid(row=0, column=0, padx=5, pady=5)

image_dir_entry = ttk.Entry(settings_frame, textvariable=image_dir_var)
image_dir_entry.grid(row=0, column=1, padx=5, pady=5)

auto_resize_checkbox = ttk.Checkbutton(settings_frame, text="Redimensionar imagem automaticamente",
                                       variable=auto_resize_var, onvalue=1, offvalue=0, command=toggle_auto_resize)
auto_resize_checkbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

resize_label = ttk.Label(settings_frame, text="Redimensionar para:")
resize_label.grid(row=2, column=0, padx=5, pady=5)
resize_label.config(state=tk.DISABLED)

save_settings_button = ttk.Button(
    settings_frame, text="Salvar Configurações", command=save_settings)
save_settings_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

toggle_auto_resize()

root.mainloop()
