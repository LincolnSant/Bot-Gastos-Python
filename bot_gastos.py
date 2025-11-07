import json
import os


ARQUIVO_DE_GASTOS = 'gastos.json'

# --- GAVETA 3: CARREGAR DADOS ---


def carregar_dados():
    # Se o arquivo não existir, retorna uma lista vazia
    if not os.path.exists(ARQUIVO_DE_GASTOS):
        return []

    # Se o arquivo existir, tenta ler
    try:
        with open(ARQUIVO_DE_GASTOS, 'r') as f:
            dados = json.load(f)
            return dados
    except json.JSONDecodeError:

        # Se o arquivo estiver corrompido/vazio, retorna lista vazia
        print('Erro: Arquivo de save corrompido. Começando do zero. ')
        return []


print('============================BOT DE GASTOS=============================')

# --- MEMÓRIA PRINCIPAL (Global) ---
lista_de_gastos = carregar_dados()
print(f'Total de gastos registrados: {len(lista_de_gastos)}')


# --- GAVETA 1: ADICIONAR GASTO ---
def adicionar_gasto():
    print('\n--- Adicionando Novo Gasto ---')
    print('='*70)

    # --- LOPPING DE VERIFICAÇÃO ---
    while True:
        try:
            valor = float(input('\nPor favor, digite o valor do seu gasto: '))
            break
        except ValueError:
            print('='*70)
            print('ERRO: Formato inválido, tente novamente. EX(25.99, 30.00)')
    # --- FIM DO LOOPING --

    print('='*70)

    categoria = input(
        '\nAgora, digite a categoria do seu gasto, ex (Alimentação, Lazer): ').title()
    print('='*70)

    descricao = input(
        '\nPor fim, digite a descrição do seu gasto, ex (Almoço, Cinema): ').title()
    print('='*70)

    # -- Dicionario para organizar as 3 info de gastos que serão salvas
    gasto_atual = {
        'valor': valor,
        'cat': categoria,
        'desc': descricao
    }
    lista_de_gastos.append(gasto_atual)
    # .append() significa "adicionar no fim da lista_de_gastos"

    print('\n>>> Maravilha, gasto anotado com sucesso! <<<')
    print('='*70)
# --- FIM DA GAVETA 1 ---


# --- GAVETA 2: MOSTRAR RELATÓRIO ---
# (Definida ANTES do menu, para que o menu possa "enxergar ela")
def mostrar_relatorio():
    print('\n================================')
    print('       RELATÓRIO FINAL DE GASTOS')
    print('================================')

    if len(lista_de_gastos) == 0:
        print('Você não registrou nenhum gasto hoje.')
    else:
        total_gasto = 0.0
        for gasto in lista_de_gastos:
            print(
                f"CATEGORIA: {gasto['cat']} | DESCRIÇÃO: {gasto['desc']} | VALOR: R$ {gasto['valor']:.2f}")
            total_gasto += gasto['valor']  # Usei o atalho +=

        print('--------------------------------')
        print(f'Total de gastos: R$ {total_gasto:.2f}')
        print(f'\nNúmero de registros: {len(lista_de_gastos)}')
# --- FIM DA GAVETA 2 ---

# --- GAVETA 4 - SALVAR DADOS ---


def salvar_dados():
    try:
        # 'w' significa 'write' (escrever). Ele SOBRESCREVE o arquivo.
        with open(ARQUIVO_DE_GASTOS, 'w') as f:
            # json.dump(O_QUE_SALVAR, ONDE_SALVAR, indent=4_para_ficar_bonito)
            json.dump(lista_de_gastos, f, indent=4)
        print('\n>>> Gastos salvos com sucesso! <<<')
    except Exception as e:
        print(f'ERRO AO SALVAR: {e}')


# --- LOOP PRINCIPAL (MENU) ---
while True:
    print('\n============================')
    print('       MENU PRINCIPAL')
    print('============================')
    print(f'Gastos registrados: {len(lista_de_gastos)}')
    print('[1] Adicionar novo gasto')
    print('[2] Ver relatório')
    print('[3] Sair')

    opcao = input('Escolha uma opção (1, 2 ou 3): ').strip()

    if opcao == '1':
        adicionar_gasto()  # <--- CHAMA A GAVETA 1

    elif opcao == '2':
        mostrar_relatorio()  # <--- CHAMA A GAVETA 2

    elif opcao == '3':
        salvar_dados()

        print('\nObrigado por usar o Bot de Gastos. Até mais!')
        break  # <--- Quebra o loop do menu e encerra

    else:
        print('\nERRO: Opção inválida! Digite 1, 2 ou 3.')

# --- FIM DO PROGRAMA ---
