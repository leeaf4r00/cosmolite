import subprocess

def botao_ponto_de_venda():
    subprocess.call(["python", "pdv.py"])
    subprocess.call(["python", "vendas_detalhadas.py"])
    subprocess.call(["python", "vendas_resumidas.py"])
