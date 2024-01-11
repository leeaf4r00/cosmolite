# Classe para representar as contas da empresa
class Conta:
  def __init__(self, nome, saldo_inicial):
    self.nome = nome
    self.saldo = saldo_inicial

  def depositar(self, valor):
    self.saldo += valor
  
  def sacar(self, valor):
    self.saldo -= valor

# Classe para representar entradas e saídas  
class Lancamento:
  def __init__(self, data, conta, valor, descricao):
    self.data = data
    self.conta = conta
    self.valor = valor
    self.descricao = descricao

# Classe para controlar o fluxo de caixa
class ControleFinanceiro:
  def __init__(self):
    self.contas = []
    self.lancamentos = []

  def adicionar_conta(self, conta):
    self.contas.append(conta)
  
  def registrar_lancamento(self, lancamento):
    self.lancamentos.append(lancamento)
    if lancamento.valor > 0:
      lancamento.conta.depositar(lancamento.valor)
    else:
      lancamento.conta.sacar(-lancamento.valor)
  
  def fluxo_de_caixa(self, inicio, fim):
    fluxo = 0
    for l in self.lancamentos:
      if inicio <= l.data <= fim:
        fluxo += l.valor
    return fluxo

# Exemplo de uso
caixa = Conta("Caixa", 1000)
banco = Conta("Banco", 5000)

controle = ControleFinanceiro()
controle.adicionar_conta(caixa)
controle.adicionar_conta(banco)

controle.registrar_lancamento(Lancamento("10/05/2022", caixa, 500, "Venda")) 
controle.registrar_lancamento(Lancamento("13/05/2022", banco, -350, "Pagamento Func."))

print(controle.fluxo_de_caixa("01/05/2022", "31/05/2022")) # Exibe 150