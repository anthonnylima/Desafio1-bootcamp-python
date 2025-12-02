
saldo = 0.00
limite = 500.00
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
usuarios = []
lista_cpf = []
contas = []
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

    numero_conta = len(contas) + 1  

    conta = {
        "agencia": AGENCIA,
        "numero": numero_conta,
        "usuario": usuario
    }

    contas.append(conta)

    print(f"Conta criada! Agência: {AGENCIA} Conta: {numero_conta}")
    return conta


def cadastrar(nome, numero, endereco, cpf):
    dados_usuario = {
        "nome": nome,
        "numero": numero,
        "endereco": endereco,
        "cpf": cpf
    }
    lista_cpf.append(cpf)
    usuarios.append(dados_usuario)
    return usuarios, lista_cpf


def depositar(saldo, extrato, /):
    valor = float(input("Informe o valor do depósito: "))
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def sacar(*, saldo, limite, LIMITE_SAQUES, extrato, numero_saques):
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

def tela_cadastro():
    while True:
        cadastro = input(
            """
-- BEM-VINDO AO NOSSO BANCO --
Já possui cadastro?           
[s] Fazer login
[n] Criar cadastro

"""
        )

        if cadastro == "s":
            cpf = input("Digite o CPF:\n").replace(".", "").replace("-", "")
            if cpf in lista_cpf:
                print("Login efetuado!")
                return cpf
            else:
                print("CPF não encontrado. Tente novamente.")

        elif cadastro == "n":
            print("Preencha com seus dados:\n")

            nome = input("Digite seu nome:\n")
            numero = int(input("Digite seu número:\n"))

            logradouro = input("Logradouro: ").strip()
            bairro = input("Bairro: ").strip()
            cidade = input("Cidade: ").strip()
            uf = input("UF: ").strip().upper()
            endereco = f"{logradouro} - {bairro} - {cidade}/{uf}"

            cpf = input("Digite seu CPF:\n").replace(".", "").replace("-", "")

            if cpf not in lista_cpf:
                cadastrar(nome, numero, endereco, cpf)
                print("Agora vamos criar uma conta corrente:")
                criar_conta_corrente(cpf)
                return cpf
            else:
                print("CPF já cadastrado. Faça login.")


def operacoes_bancarias():
    global saldo, extrato, numero_saques

    menu = '''
ESCOLHA UM SERVIÇO: 

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

'''

    while True:
        opcao = input(menu).lower()

        if opcao == 'd':
            saldo, extrato = depositar(saldo, extrato)

        elif opcao == 's':
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                extrato=extrato,
                limite=limite,
                LIMITE_SAQUES=LIMITE_SAQUES,
                numero_saques=numero_saques
            )

        elif opcao == 'e':
            tirar_extrato(extrato, saldo)

        elif opcao == 'q':
            print("Obrigado por ser nosso cliente!")
            break

        else:
            print("Digite uma opção válida...")


def main():
    cpf_usuario = tela_cadastro()
    print(f"Usuário logado com CPF: {cpf_usuario}")
    operacoes_bancarias()


main()







