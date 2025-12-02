saldo = 0.00
limite = 500.00
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
opcao=""
usuarios=[]
lista_cpf=[]
contas=[]
lista_contas=[]
AGENCIA = "0001"

def criar_conta_corrente(cpf):
    usuario = None
    for u in usuarios:
        if u["cpf"] == cpf:
            usuario = u
            break

    if usuario is None:
        print("Usuário não encontrado! Conta não criada.")
        return None

    numero_conta = len(contas) + 1  # incrementa automaticamente

    conta = {
        "agencia": AGENCIA,
        "numero": numero_conta,
        "usuario": usuario
    }

    contas.append(conta)

    print(f"Conta criada! Agência: {AGENCIA} Conta: {numero_conta}")
    return conta



def cadastrar(nome,numero,endereco,cpf):
    dados_usuario = {
        "nome": nome,
        "numero": numero,
        "endereco": endereco,
        "cpf": cpf
    }
    lista_cpf.append(cpf)
    usuarios.append(dados_usuario)
    return usuarios, lista_cpf

def depositar(saldo, extrato,/):
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(valor)
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato
        

def sacar(*,saldo, limite, LIMITE_SAQUES, extrato, numero_saques):
    valor = float(input("Informe o valor do saque: "))
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES
    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    else:
        print('Operação falhou! O valor informado é inválido')
    return saldo, extrato, numero_saques
     
def tirar_extrato(extrato, saldo):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

while True:
    cadastro=str(input(
"""
--BEM VINDO AOS SERVIÇOS DO NOSSO BANCO--
    Ja possui cadastro?           
    [s]Logar
    [n]Criar conta\n
"""
))
    if cadastro=="s":
        n_conta=int(input("digite o numero da conta:\n"))
        cpf=str(input("digite o cpf:\n"))
        cpf=cpf.replace(".","").replace("-","")
        if cpf in lista_cpf:
            print("login efetuado")
            break
        else:
            print("login não efetuado")
    elif cadastro=="n":
        print("Preencha com seus dados:\n")
        nome=str(input("digite seu nome\n"))
        numero=int(input("digite seu numero:\n"))
        logradouro = input("Digite o seu enderço:\nLogradouro: ").strip()
        bairro = input("Bairro: ").strip()
        cidade = input("Cidade: ").strip()
        uf = input("Sigla do estado (UF): ").strip().upper()
        endereco = f"{logradouro} - {bairro} - {cidade}/{uf}"
        cpf=str(input("digite seu cpf:\n"))
        cpf=cpf.replace(".","").replace("-","")
        if cpf not in lista_cpf:
            cadastrar(nome, numero, endereco,cpf)
            print("agora vamos criar uma conta corrente: ")
            criar_conta_corrente(cpf)
            break
        else:
            print("Ja possui cadastro")
menu='''
ESCOLHO UM SERVIÇO: 

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

'''
while True:
    opcao=str(input(menu).lower())
    if opcao=='d':
        saldo,extrato=depositar(saldo, extrato)
    elif opcao=='s':
        saldo,extrato,numero_saques=sacar(saldo=saldo,extrato=extrato,limite=limite,LIMITE_SAQUES=LIMITE_SAQUES,numero_saques=numero_saques)
    elif opcao=='e':
        tirar_extrato(extrato,saldo)  
    elif opcao=='q':
        break
    else:
        print('Digite um comando válido')
print('Obrigado por ser nosso cliente')








