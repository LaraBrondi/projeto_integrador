import numpy as np
import mysql.connector


def letra_para_numero(c):
    return ord(c.lower()) - ord('a') + 1

def numero_para_letra(n):
    return chr(((n - 1) % 26) + ord('a'))

def cifra_hill(texto, K):
    texto = texto.lower().replace(" ", "")
    if len(texto) % 2 != 0:
        texto += 'x'
    numeros = [letra_para_numero(c) for c in texto]
    cifrado = []
    for i in range(0, len(numeros), 2):
        bloco = np.array([[numeros[i]], [numeros[i+1]]])
        codificado = np.dot(K, bloco) % 26
        codificado[codificado == 0] = 26
        cifrado.extend(codificado.flatten().tolist())
    return ''.join(numero_para_letra(n) for n in cifrado)

def decifra_hill(cifrado, K_inv):
    numeros = [letra_para_numero(c) for c in cifrado]
    decifrado = []
    for i in range(0, len(numeros), 2):
        bloco = np.array([[numeros[i]], [numeros[i+1]]])
        decodificado = np.dot(K_inv, bloco) % 26
        decodificado[decodificado == 0] = 26
        decifrado.extend(decodificado.flatten().tolist())
    return ''.join(numero_para_letra(n) for n in decifrado)

def calcular_classificacao(consumo_agua, consumo_energia, residuos_nao_reciclaveis, residuos_reciclados):
    total_residuos = residuos_nao_reciclaveis + residuos_reciclados
    percentual_reciclados = (residuos_reciclados / total_residuos) * 100 if total_residuos != 0 else 0

    if consumo_agua < 150 and consumo_energia < 100 and percentual_reciclados > 50:
        return "Excelente"
    elif consumo_agua < 200 and consumo_energia < 150 and percentual_reciclados > 30:
        return "Bom"
    else:
        return "Precisa Melhorar"

def solicitar_novos_dados(registro_antigo):
    def entrada_ou_valor_atual(prompt, valor_atual):
        entrada = input(f"{prompt} ({valor_atual}): ")
        return entrada if entrada else valor_atual

    nome_usuario = entrada_ou_valor_atual("Nome", registro_antigo[1])
    consumo_agua = float(entrada_ou_valor_atual("Consumo de água", registro_antigo[2]))
    consumo_energia = float(entrada_ou_valor_atual("Consumo de energia", registro_antigo[3]))
    residuos_nao_reciclaveis = float(entrada_ou_valor_atual("Resíduos não recicláveis", registro_antigo[4]))
    residuos_reciclados = float(entrada_ou_valor_atual("Resíduos reciclados", registro_antigo[5]))
    transporte_usado = entrada_ou_valor_atual("Transporte usado", registro_antigo[6])
    data = entrada_ou_valor_atual("Data", registro_antigo[7])

    return (
        nome_usuario, consumo_agua, consumo_energia,
        residuos_nao_reciclaveis, residuos_reciclados,
        transporte_usado, data
    )

def alterar_monitoramento(cursor, conexao, K):
    print("\n--- Alterar Monitoramento ---")
    try:
        id_alterar = int(input("Digite o ID do monitoramento que deseja alterar: "))
        cursor.execute("SELECT * FROM Monitoramento_Sustentabilidade WHERE id = %s", (id_alterar,))
        registro = cursor.fetchone()

        if not registro:
            print("Monitoramento não encontrado.")
            return

        novos_dados = solicitar_novos_dados(registro)
        classificacao = calcular_classificacao(
            novos_dados[1], novos_dados[2], novos_dados[3], novos_dados[4]
        )
        classificacao_criptografada = cifra_hill(classificacao, K)

        sql = """
            UPDATE Monitoramento_Sustentabilidade
            SET nome_usuario = %s, consumo_agua = %s, consumo_energia = %s,
                residuos_nao_reciclaveis = %s, residuos_reciclados = %s,
                transporte_usado = %s, data = %s, classificacao = %s
            WHERE id = %s
        """
        cursor.execute(sql, (*novos_dados, classificacao_criptografada, id_alterar))
        conexao.commit()
        print("Monitoramento alterado com sucesso!")
    except Exception as e:
        print(f"Erro ao alterar: {e}")

def cadastrar_monitoramento(cursor, conexao, K):
    print("\n--- Cadastrar Monitoramento ---")
    try:
        nome_usuario = input("Nome do usuário: ")
        consumo_agua = float(input("Consumo de água (litros): "))
        consumo_energia = float(input("Consumo de energia (kWh): "))
        residuos_nao_reciclaveis = float(input("Resíduos não recicláveis (kg): "))
        residuos_reciclados = float(input("Resíduos reciclados (kg): "))
        transporte_usado = input("Transporte usado: ")
        data = input("Data (AAAA-MM-DD): ")

        classificacao = calcular_classificacao(consumo_agua, consumo_energia, residuos_nao_reciclaveis, residuos_reciclados)
        classificacao_criptografada = cifra_hill(classificacao, K)

        sql = """
            INSERT INTO Monitoramento_Sustentabilidade
            (nome_usuario, consumo_agua, consumo_energia, residuos_nao_reciclaveis, residuos_reciclados, transporte_usado, data, classificacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nome_usuario, consumo_agua, consumo_energia, residuos_nao_reciclaveis, residuos_reciclados, transporte_usado, data, classificacao_criptografada))
        conexao.commit()
        print("Monitoramento cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar: {e}")

def listar_monitoramentos(cursor, K_inv):
    print("\n--- Lista de Monitoramentos ---")
    try:
        cursor.execute("SELECT * FROM Monitoramento_Sustentabilidade")
        registros = cursor.fetchall()
        for registro in registros:
            classificacao = decifra_hill(registro[8], K_inv)
            print(f"ID: {registro[0]}, Nome: {registro[1]}, Água: {registro[2]}, Energia: {registro[3]}, Não recicláveis: {registro[4]}, Reciclados: {registro[5]}, Transporte: {registro[6]}, Data: {registro[7]}, Classificação: {classificacao}")
    except Exception as e:
        print(f"Erro ao listar: {e}")

def excluir_monitoramento(cursor, conexao):
    print("\n--- Excluir Monitoramento ---")
    try:
        id_excluir = int(input("Digite o ID do monitoramento que deseja excluir: "))
        cursor.execute("DELETE FROM Monitoramento_Sustentabilidade WHERE id = %s", (id_excluir,))
        conexao.commit()
        print("Monitoramento excluído com sucesso!")
    except Exception as e:
        print(f"Erro ao excluir: {e}")

K = np.array([[4, 3], [1, 2]])
K_inv = np.array([[16, 15], [5, 6]])

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='fraccaroli3',
    database='projeto_integrador'
)

if conexao.is_connected():
    print('Conectado ao banco de dados!')

cursor = conexao.cursor()

while True:
    print("\n=== Sistema de Monitoramento de Sustentabilidade Pessoal ===")
    print("1 - Ver dados e calcular médias")
    print("2 - Cadastrar monitoramento diário")
    print("3 - Listar monitoramentos")
    print("4 - Alterar monitoramento")
    print("5 - Excluir monitoramento")
    print("6 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        listar_monitoramentos(cursor, K_inv)
    elif opcao == "2":
        cadastrar_monitoramento(cursor, conexao, K)
    elif opcao == "3":
        listar_monitoramentos(cursor, K_inv)
    elif opcao == "4":
        alterar_monitoramento(cursor, conexao, K)
    elif opcao == "5":
        excluir_monitoramento(cursor, conexao)
    elif opcao == "6":
        print("Saindo do sistema :(")
        break
    else:
        print("Opção inválida. Tente novamente.")

cursor.close()
conexao.close()