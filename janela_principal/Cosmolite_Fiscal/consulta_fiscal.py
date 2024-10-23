import PySimpleGUI as sg
import requests
import webbrowser
import clipboard
import subprocess
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AppConfig:
    """Configuration settings for the application"""
    api_url: str = 'https://api.cosmos.bluesoft.com.br/gtins/'
    api_token: str = 'UJTBhybMZx96n33FzUfp2w'
    history_file: Path = Path('historico.txt')
    window_size: tuple = (800, 600)
    multiline_size: tuple = (80, 8)
    listbox_size: tuple = (80, 10)

class ProductLookupApp:
    def __init__(self, config: AppConfig):
        self.config = config
        self.history: List[Dict] = []
        self.window: Optional[sg.Window] = None
        
        self.api_headers = {
            'X-Cosmos-Token': config.api_token,
            'User-Agent': 'API Request'
        }
        
    def create_layout(self) -> List:
        """Create the application layout"""
        return [
            [
                sg.Text("Escolha o tipo de pesquisa:"),
                sg.Radio("Código de barras", "RADIO1", default=True, key="-EAN-"),
                sg.Radio("Descrição", "RADIO1", key="-DESC-")
            ],
            [
                sg.Text("Insira o código EAN ou descrição do produto:"),
                sg.Input(key="-SEARCH-"),
                sg.Button("Buscar", bind_return_key=True),
            ],
            [
                sg.Multiline("", size=self.config.multiline_size, key="-RETORNO-",
                         font=("Helvetica", 10), auto_size_text=True)
            ],
            [sg.Text("Histórico:")],
            [
                sg.Listbox([], size=self.config.listbox_size, key="-HISTORICO-",
                       font=("Helvetica", 10), enable_events=True,
                       auto_size_text=True)
            ],
            [
                sg.Text("Software Licenciado e Produzido por Rafael Fernandes, Rurópolis-Pará",
                    font=("Helvetica", 10, "underline"),
                    text_color="white", background_color="red")
            ],
            self.create_button_row(),
            [
                sg.Text("Tenha controle total de seu negócio e acessando as informações de qualquer lugar e a qualquer hora.")
            ],
            [
                sg.Button("TERMOS DE USO", font=("Helvetica", 10, "underline"), key="-TERMS-")
            ]
        ]
    
    def create_button_row(self) -> List:
        """Create the row of action buttons"""
        return [
            sg.Button("Instagram", font=("Helvetica", 10, "underline"),
                     button_color=("white", "purple"), key="-INSTAGRAM-"),
            sg.Button("Whatsapp", font=("Helvetica", 10, "underline"),
                     button_color=("white", "green"), key="-WHATSAPP-"),
            sg.Button("Copiar resultado", font=("Helvetica", 10), key="-COPY-"),
            sg.Button("Cadastro de Produto", font=("Helvetica", 10), key="-CADASTRO-")
        ]

    def validate_input(self, search_term: str) -> bool:
        """Validate if the search term is a valid EAN code or description"""
        return bool(search_term) and (search_term.isdigit() or len(search_term) > 2)

    def query_product(self, gtin: str) -> Optional[Dict]:
        """Query product from API"""
        if not self.validate_input(gtin):
            sg.popup_error("Valor de pesquisa inválido. Insira um código EAN ou descrição válida.")
            return None

        try:
            response = requests.get(f'{self.config.api_url}{gtin}.json', 
                                 headers=self.api_headers, 
                                 timeout=10)
            response.raise_for_status()
            result = response.json()
            self.history.append(result)
            self.save_history()
            return result
        except requests.exceptions.RequestException as e:
            sg.popup_error(f'Erro ao consultar o produto: {str(e)}')
            return None

    def save_history(self) -> None:
        """Save product history to file"""
        try:
            with open(self.config.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except IOError as e:
            sg.popup_error(f'Erro ao salvar histórico: {str(e)}')

    def load_history(self) -> None:
        """Load product history from file"""
        try:
            if self.config.history_file.exists():
                with open(self.config.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            sg.popup_error(f'Erro ao carregar histórico: {str(e)}')
            self.history = []

    @staticmethod
    def format_product(product: Dict) -> str:
        """Format product data for display"""
        formatted = []
        fields = [
            ('gtin', 'Código EAN'),
            ('description', 'Descrição'),
            ('ncm', 'NCM'),
            ('price', 'Preço'),
            ('quantity', 'Quantidade'),
            ('avg_price', 'Preço Médio'),
            ('gross_weight', 'Peso Bruto (g)'),
            ('height', 'Altura (cm)'),
            ('length', 'Comprimento (cm)'),
            ('max_price', 'Preço Máximo'),
            ('net_weight', 'Peso Líquido (g)'),
            ('width', 'Largura (cm)')
        ]
        
        for key, label in fields:
            if value := product.get(key):
                formatted.append(f"{label}: {value}")
        
        if brand := product.get('brand', {}).get('name'):
            formatted.append(f"Marca: {brand}")
            
        if gpc := product.get('gpc'):
            formatted.append(f"GPC: {gpc.get('code')} - {gpc.get('description')}")
            
        if thumbnail := product.get('thumbnail'):
            formatted.append(f"Imagem: {thumbnail}")
            
        if url := product.get('url'):
            formatted.append(
                f'<a href="{url}" style="text-decoration: none; color: inherit;">'
                'Clique aqui</a>'
            )
            
        return '\n'.join(formatted)

    def run(self) -> None:
        """Run the application main loop"""
        self.window = sg.Window(
            "Consulta de Produto",
            self.create_layout(),
            size=self.config.window_size,
            resizable=True,
            finalize=True
        )
        
        self.load_history()
        
        while True:
            event, values = self.window.read()
            
            if event == sg.WINDOW_CLOSED:
                break
                
            self.handle_event(event, values)
            
        self.window.close()

    def handle_event(self, event: str, values: Dict) -> None:
        """Handle window events"""
        if event == "Buscar":
            self.handle_search(values)
        elif event == "-HISTORICO-":
            self.load_history()
            self.window["-HISTORICO-"].update(
                [self.format_product(p) for p in self.history]
            )
        elif event == "-INSTAGRAM-":
            webbrowser.open("https://www.instagram.com/RAFAELMOREIRAFERNANDES")
        elif event == "-WHATSAPP-":
            webbrowser.open("https://wa.me/message/556WDBERNK3MM1")
        elif event == "-COPY-":
            clipboard.copy(self.window["-RETORNO-"].get())
        elif event == "-TERMS-":
            self.show_terms()
        elif event == "-CADASTRO-":
            subprocess.Popen(["python", "cadastro_produto.py"])

    def handle_search(self, values: Dict) -> None:
        """Handle product search"""
        search_term = values["-SEARCH-"]
        if not self.validate_input(search_term):
            self.window["-RETORNO-"].update("Insira um valor válido para a pesquisa.")
            return
            
        search_type = "ean" if values["-EAN-"] else "description"
        
        # Search in history first
        product = next(
            (p for p in self.history if (
                p.get("gtin") == search_term if search_type == "ean" 
                else p.get("description") == search_term
            )), 
            None
        )
        
        if not product:
            product = self.query_product(search_term)
            
        if product:
            result = self.format_product(product)
            self.window["-RETORNO-"].update(result)
        else:
            self.window["-RETORNO-"].update(f"Produto {search_term} não encontrado.")
            
        self.save_history()
        self.window["-HISTORICO-"].update(
            [self.format_product(p) for p in self.history]
        )
        self.window["-SEARCH-"].update('')

    @staticmethod
    def show_terms() -> None:
        """Show terms of use"""
        terms = """Termos de Uso:
A RR SISTEMAS não se responsabiliza pela utilização das informações tributárias do programa Cosmos.

Antes da coleta e utilização de qualquer informação e dados pessoais, o USUÁRIO da Cosmos deverá:

a) somente coletar dados pessoais se o motivo estiver fundamentado em uma das bases legais previstas no artigo 7º da Lei nº 13.709/2018, que trata da Lei Geral de Proteção de Dados (LGPD);

b) obter a aprovação de um contador que se responsabilize legalmente pela classificação das informações tributárias inseridas na plataforma.

A inobservância das regras contidas neste termos e condições de uso poderá culminar em demandas judiciais e/ou administrativas em desfavor do USUÁRIO."""
        sg.popup(terms)

def main():
    config = AppConfig()
    app = ProductLookupApp(config)
    app.run()

if __name__ == "__main__":
    main()
