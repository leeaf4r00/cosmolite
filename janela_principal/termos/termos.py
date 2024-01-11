import PySimpleGUI as sg

sg.theme("DefaultNoMoreNagging")


def exibir_termos():
    sg.popup_scrolled("""Termos de Uso:

A RR SISTEMAS não se responsabiliza pela utilização das informações tributárias do programa Cosmos.

Antes da coleta e utilização de qualquer informação e dados pessoais, o USUÁRIO da Cosmos deverá:  

a) Somente coletar dados pessoais se o motivo estiver fundamentado em uma das bases legais previstas no artigo 7º da Lei nº 13.709/2018, que trata da Lei Geral de Proteção de Dados (LGPD).

b) Obter a aprovação de um contador que se responsabilize legalmente pela classificação das informações tributárias inseridas na plataforma.

c) Garantir que as informações coletadas sejam armazenadas e protegidas de acordo com as melhores práticas de segurança da informação e em conformidade com as leis de proteção de dados aplicáveis.

d) Limitar a coleta e utilização de dados pessoais apenas ao necessário para cumprir a finalidade declarada e informada aos titulares dos dados.

e) Assegurar que os titulares dos dados tenham o direito de acessar, retificar, atualizar ou excluir suas informações pessoais, conforme permitido pela legislação de proteção de dados aplicável.

f) Não transferir ou compartilhar informações pessoais com terceiros sem o consentimento explícito dos titulares dos dados, a menos que exigido por lei ou autoridade competente.

g) Adotar medidas técnicas e organizacionais adequadas para proteger as informações pessoais contra acesso não autorizado, uso indevido, divulgação, alteração ou destruição não autorizada.

h) Manter registros claros e precisos sobre as atividades de coleta, uso e processamento de dados pessoais, incluindo o consentimento obtido, quando aplicável.

i) Cumprir todas as leis e regulamentos aplicáveis relacionados à proteção de dados pessoais e privacidade.

É responsabilidade do USUÁRIO da Cosmos garantir o cumprimento dessas diretrizes e dos requisitos legais de proteção de dados ao utilizar a plataforma e coletar informações pessoais dos usuários. O não cumprimento dessas obrigações pode resultar em sanções legais e danos à reputação da empresa.
A inobservância das regras contidas nestes termos e condições de uso poderá culminar em demandas judiciais e/ou administrativas em desfavor do USUÁRIO.""", title="Termos de Uso", size=(60, 20))


# Botão de exibição dos termos de uso
layout = [
    [sg.Button("Exibir Termos de Uso", key="-TERMS-")]
]

# Criar a janela principal
window = sg.Window("Consulta de Produto", layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "-TERMS-":
        exibir_termos()

window.close()
