import textwrap

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

    @staticmethod
    def criar_usuario(usuarios):
        cpf = input("Informe o CPF (somente número): ")
        if any(u.cpf == cpf for u in usuarios):
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        usuario = Usuario(nome, data_nascimento, cpf, endereco)
        usuarios.append(usuario)
        print("=== Usuário criado com sucesso! ===")

    @staticmethod
    def buscar_por_cpf(cpf, usuarios):
        for usuario in usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None


class Conta:
    def __init__(self, agencia, numero, usuario):
        self.agencia = agencia
        self.numero = numero
        self.usuario = usuario
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0
        self.limite_saques = 3

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def sacar(self, valor):
        if valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > self.limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif self.numero_saques >= self.limite_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")


class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.agencia_padrao = "0001"

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = Usuario.buscar_por_cpf(cpf, self.usuarios)

        if not usuario:
            print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
            return

        numero = len(self.contas) + 1
        conta = Conta(self.agencia_padrao, numero, usuario)
        self.contas.append(conta)
        print("\n=== Conta criada com sucesso! ===")

    def listar_contas(self):
        for conta in self.contas:
            linha = f"""\n
            Agência:\t{conta.agencia}
            C/C:\t\t{conta.numero}
            Titular:\t{conta.usuario.nome}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))


def menu():
    menu_texto = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_texto))


def main():
    banco = Banco()
    conta_ativa = None

    while True:
        opcao = menu()

        if opcao == "d":
            if not conta_ativa:
                print("\n@@@ Nenhuma conta ativa. Crie uma conta primeiro. @@@")
                continue
            valor = float(input("Informe o valor do depósito: "))
            conta_ativa.depositar(valor)

        elif opcao == "s":
            if not conta_ativa:
                print("\n@@@ Nenhuma conta ativa. Crie uma conta primeiro. @@@")
                continue
            valor = float(input("Informe o valor do saque: "))
            conta_ativa.sacar(valor)

        elif opcao == "e":
            if not conta_ativa:
                print("\n@@@ Nenhuma conta ativa. Crie uma conta primeiro. @@@")
                continue
            conta_ativa.exibir_extrato()

        elif opcao == "nu":
            Usuario.criar_usuario(banco.usuarios)

        elif opcao == "nc":
            banco.criar_conta()
            conta_ativa = banco.contas[-1]  # define a última criada como ativa

        elif opcao == "lc":
            banco.listar_contas()

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
