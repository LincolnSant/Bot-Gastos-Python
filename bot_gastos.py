import sqlite3
import os
import datetime

# Nome do arquivo do banco de dados
ARQUIVO_BD = 'gastos.db'

# --- GAVETA 0: INICIALIZAR O BANCO DE DADOS ---
# Garante que o arquivo e a tabela existam antes de começarmos.
def inicializar_bd():
    conexao = sqlite3.connect(ARQUIVO_BD)
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL NOT NULL,
            categoria TEXT NOT NULL,
            descricao TEXT NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

# --- FUNÇÃO EXTRA: CONTAR GASTOS ---
# Usada apenas para mostrar o total no menu principal.
def obter_quantidade_gastos():
    conexao = sqlite3.connect(ARQUIVO_BD)
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM gastos")
    quantidade = cursor.fetchone()[0]
    conexao.close()
    return quantidade

# --- GAVETA 1: ADICIONAR GASTO (SQL) ---
def adicionar_gasto():
    print('\n--- Adicionando Novo Gasto ---')
    print('='*70)

    # Validação do VALOR
    while True:
        try:
            valor = float(input('\nPor favor, digite o valor do seu gasto: '))
            break
        except ValueError:
            print('='*70)
            print('ERRO: Formato inválido. Use ponto (ex: 25.99)')

    print('='*70)
    categoria = input('\nAgora, digite a categoria (ex: Alimentação): ').title()
    print('='*70)
    descricao = input('\nPor fim, digite a descrição (ex: Almoço): ').title()
    print('='*70)

    # Validação da DATA
    while True:
        data_str = input('\nDigite a data (DD/MM/AAAA) ou deixe vazio para HOJE: ').strip()
        if not data_str:
            data_final = datetime.date.today().strftime('%d/%m/%Y')
            break
        else:
            try:
                datetime.datetime.strptime(data_str, '%d/%m/%Y')
                data_final = data_str
                break
            except ValueError:
                 print('ERRO: Data inválida. Use DD/MM/AAAA')

    # --- COMANDO SQL PARA INSERIR ---
    conexao = sqlite3.connect(ARQUIVO_BD)
    cursor = conexao.cursor()
    # Usamos '?' para evitar problemas de segurança (SQL Injection)
    cursor.execute("INSERT INTO gastos (valor, categoria, descricao, data) VALUES (?, ?, ?, ?)",
                   (valor, categoria, descricao, data_final))
    conexao.commit()
    conexao.close()
    
    print('\n>>> Gasto salvo no Banco de Dados com sucesso! <<<')
    print('='*70)

# --- GAVETA 2: MOSTRAR RELATÓRIO (SQL) ---
def mostrar_relatorio():
    print('\n================================')
    print('       RELATÓRIO FINAL DE GASTOS')
    print('================================')

    conexao = sqlite3.connect(ARQUIVO_BD)
    cursor = conexao.cursor()
    
    # Pega TUDO da tabela gastos
    cursor.execute("SELECT * FROM gastos")
    todos_gastos = cursor.fetchall() # Retorna uma lista de tuplas
    conexao.close()

    if len(todos_gastos) == 0:
        print('Você não registrou nenhum gasto ainda.')
    else:
        total_gasto = 0.0
        for g in todos_gastos:
            # Como é uma tupla, acessamos pelo índice numérico:
            # g[0] é o ID, g[1] é o valor, g[2] é categoria, etc.
            print(f"[ID: {g[0]}] DATA: {g[4]} | CAT: {g[2]} | DESC: {g[3]} | R$ {g[1]:.2f}")
            total_gasto += g[1]

        print('--------------------------------')
        print(f'Total de gastos: R$ {total_gasto:.2f}')
        print(f'Número de registros: {len(todos_gastos)}')

# --- GAVETA 3: REMOVER GASTO (SQL) ---
def remover_gasto():
    print('\n--- Remover Gasto ---')
    # Mostra o relatório para o usuário ver os IDs disponíveis
    mostrar_relatorio()
    print('='*70)

    try:
        id_para_remover = int(input('Digite o ID do gasto para remover (0 para cancelar): '))
        if id_para_remover == 0:
            return

        conexao = sqlite3.connect(ARQUIVO_BD)
        cursor = conexao.cursor()
        
        # Primeiro, verifica se esse ID realmente existe
        cursor.execute("SELECT count(*) FROM gastos WHERE id = ?", (id_para_remover,))
        if cursor.fetchone()[0] == 0:
            print(f'\nERRO: Gasto com ID {id_para_remover} não encontrado.')
        else:
            # Se existe, deleta!
            cursor.execute("DELETE FROM gastos WHERE id = ?", (id_para_remover,))
            conexao.commit()
            print(f'\n>>> Gasto ID {id_para_remover} removido com sucesso! <<<')
        
        conexao.close()

    except ValueError:
        print('\nERRO: Digite um número de ID válido.')

# ==============================================================================
# --- INÍCIO DO PROGRAMA ---
print('============================BOT DE GASTOS=============================')
inicializar_bd() # Cria o arquivo .db se ele não existir
print('Banco de dados conectado com sucesso!')

# --- LOOP PRINCIPAL (MENU) ---
while True:
    # Pega a quantidade atualizada direto do banco
    qtd = obter_quantidade_gastos()
    
    print('\n============================')
    print('       MENU PRINCIPAL')
    print('============================')
    print(f'Gastos registrados no Banco: {qtd}')
    print('[1] Adicionar novo gasto')
    print('[2] Ver relatório')
    print('[3] Remover gasto')
    print('[4] Sair')

    opcao = input('Escolha uma opção: ').strip()

    if opcao == '1':
        adicionar_gasto()
    elif opcao == '2':
        mostrar_relatorio()
    elif opcao == '3':
        remover_gasto()
    elif opcao == '4':
        print('\nObrigado por usar o Bot de Gastos. Até mais!')
        break
    else:
        print('\nERRO: Opção inválida!')