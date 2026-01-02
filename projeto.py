from datetime import datetime

AGENCIA = "0001"
LIMITE_SAQUES = 3

usuarios = []
lista_cpf = []
contas = []


contador_contas = 0  



def log_transacao(funcao):
    def wrapper(*args, **kwargs):
        hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        resultado = funcao(*args, **kwargs)
        print("-" * 40)
        print(f"Data/Hora: {hora}")
        print(f"Operação: {funcao.__name__.capitalize()}")
        return resultado
    return wrapper



class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.contas):
            conta = self.contas[self.index]
            self.index += 1
            return conta
        raise StopIteration



def gerador_relatorios(transacoes):
    filtro = input(
        "\nDeseja filtrar as transações?\n"
        "[D] Depósitos\n"
        "[S] Saques\n"
        "[0] Todas\n"
        "Escolha: "
    ).upper()

    for t in transacoes:
        if filtro == "D" and t["tipo"] == "Deposito":
            yield t
        elif filtro == "S" and t["tipo"] == "Saque":
            yield t
        elif filtro == "0":
            yield t


def criar_conta_corrente(cpf):
    global contador_contas

    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)

    if not usuario:
        print("Usuário não encontrado.")
        return None

    contador_contas += 1
    numero_conta = contador_contas

    conta = {
        "agencia": AGENCIA,
        "numero": numero_conta,
        "usuario": usuario,
        "saldo": 0.0,
        "extrato": "",
        "numero_saques": 0,
        "transacoes": []
    }

    contas.append(conta)

    print("Conta criada com sucesso!")
    print(f"Agência: {AGENCIA} | Conta: {numero_conta}")
    return conta


@log_transacao
def cadastrar(nome, numero, endereco, cpf):
    usuarios.append({
        "nome": nome,
        "numero": numero,
        "endereco": endereco,
        "cpf": cpf
    })
    lista_cpf.append(cpf)


@log_transacao
def depositar(conta):
    valor = float(input("Valor do depósito: "))

    if valor > 0:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        conta["saldo"] += valor
        conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"

        conta["transacoes"].append({
            "descricao": f"Depósito de R$ {valor:.2f}",
            "tipo": "Deposito",
            "data_hora": data_hora
        })
    else:
        print("Valor inválido.")



@log_transacao
def sacar(conta):
    valor = float(input("Valor do saque: "))

    if valor > conta["saldo"]:
        print("Saldo insuficiente.")
    elif valor > 500:
        print("Limite excedido.")
    elif conta["numero_saques"] >= LIMITE_SAQUES:
        print("Limite de saques atingido.")
    elif valor > 0:
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        conta["numero_saques"] += 1

        conta["transacoes"].append({
            "descricao": f"Saque de R$ {valor:.2f}",
            "tipo": "Saque",
            "data_hora": data_hora
        })
    else:
        print("Valor inválido.")



@log_transacao
def tirar_extrato(conta):
    print("\n=========== EXTRATO ===========")
    print(conta["extrato"] if conta["extrato"] else "Sem movimentações.")
    print(f"Saldo: R$ {conta['saldo']:.2f}")
    print("===============================")



def tela_cadastro():
            nome = input("Nome: ")
            numero = int(input("Número: "))

            logradouro = input("Logradouro: ").strip()
            bairro = input("Bairro: ").strip()
            cidade = input("Cidade: ").strip()
            uf = input("UF: ").strip().upper()

            endereco = f"{logradouro} - {bairro} - {cidade}/{uf}"

            cpf = input("CPF: ").replace(".", "").replace("-", "")

            if cpf not in lista_cpf:
                cadastrar(nome, numero, endereco, cpf)
                criar_conta_corrente(cpf)
                return cpf
            else:
                print("CPF já cadastrado.")


def operacoes_bancarias(conta):
    while True:
        opcao = input(
            "\n[d] Depositar\n"
            "[s] Sacar\n"
            "[e] Extrato\n"
            "[r] Relatório\n"
            "[q] Voltar\n"
            "Escolha: "
        ).lower()

        if opcao == "d":
            depositar(conta)
        elif opcao == "s":
            sacar(conta)
        elif opcao == "e":
            tirar_extrato(conta)
        elif opcao == "r":
            print("\n----- RELATÓRIO DE TRANSAÇÕES -----")
            for t in gerador_relatorios(conta["transacoes"]):
                 print(f"{t['data_hora']} | {t['tipo']} | {t['descricao']}")
        elif opcao == "q":
            break
        else:
            print("Opção inválida.")



def menu_principal():
    while True:
        opcao = input(
            "\n====== MENU PRINCIPAL ======\n"
            "[1] Criar conta\n"
            "[2] Acessar conta\n"
            "[3] Listar contas\n"
            "[0] Sair\n"
            "Escolha: "
        )

        if opcao == "1":
            tela_cadastro()

        elif opcao == "2":
            if not contas:
                print("Nenhuma conta cadastrada.")
                continue

            numero = int(input("Digite o número da conta: "))
            conta = next((c for c in contas if c["numero"] == numero), None)

            if conta:
                operacoes_bancarias(conta)
            else:
                print("Conta não encontrada.")

        elif opcao == "3":
            print("\n--- CONTAS CADASTRADAS ---")
            for c in ContaIterador(contas):
                print(
                    f"Agência: {c['agencia']} | "
                    f"Conta: {c['numero']} | "
                    f"Titular: {c['usuario']['nome']}"
                )

        elif opcao == "0":
            print("Obrigado por usar o sistema bancário!")
            break

        else:
            print("Opção inválida.")


def main():
    menu_principal()

main()







