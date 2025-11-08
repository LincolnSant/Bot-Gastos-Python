import json
import os
import datetime

# Nome do arquivo onde os gastos serão salvos.
ARQUIVO_DE_GASTOS = 'gastos.json'

# --- CLASSE GASTO (A Planta do Robô) ---
# Define como cada gasto deve ser estruturado (quais informações ele tem).
class Gasto:
    # O __init__ roda automaticamente quando criamos um novo gasto.
    # ATUALIZADO: Agora recebe 'data' também.
    def __init__(self, valor, categoria, descricao, data):
        self.valor = valor           # Guarda o valor
        self.categoria = categoria   # Guarda a categoria
        self.descricao = descricao   # Guarda a descrição
        self.data = data             # Guarda a data

    # Ensina o robô a se transformar num dicionário para poder ser salvo no JSON.
    def para_dicionario(self):
        return {
            'valor': self.valor,
            'cat': self.categoria,
            'desc': self.descricao,
            'data': self.data # Salva a data no JSON
        }
# ---------------------------------------

# --- GAVETA 3: CARREGAR DADOS ---
# Lê o arquivo JSON e recria os objetos Gasto na memória.
def carregar_dados():
    if not os.path.exists(ARQUIVO_DE_GASTOS):
        return []

    try:
        with open(ARQUIVO_DE_GASTOS, 'r') as f:
            dados_brutos = json.load(f)
            
            lista_de_objetos = []
            for gasto_dict in dados_brutos:
                # RECONSTRUÇÃO: Agora incluindo a DATA!
                gasto_obj = Gasto(
                    gasto_dict['valor'], 
                    gasto_dict['cat'], 
                    gasto_dict['desc'],
                    # Usa .get() para não quebrar com arquivos antigos sem data
                    gasto_dict.get('data', 'N/A')
                )
                lista_de_objetos.append(gasto_obj)
            
            return lista_de_objetos

    except json.JSONDecodeError:
        print('AVISO: Arquivo de save vazio ou corrompido. Começando do zero.')
        return []
# --- FIM DA GAVETA 3 ---


print('============================BOT DE GASTOS=============================')

# --- MEMÓRIA PRINCIPAL ---
lista_de_gastos = carregar_dados()
print(f'Total de gastos registrados: {len(lista_de_gastos)}')


# --- GAVETA 1: ADICIONAR GASTO ---
# Pergunta os dados ao usuário e cria um novo Gasto.
def adicionar_gasto():
    print('\n--- Adicionando Novo Gasto ---')
    print('='*70)

    while True:
        try:
            valor = float(input('\nPor favor, digite o valor do seu gasto: '))
            break
        except ValueError:
            print('='*70)
            print('ERRO: Formato inválido, tente novamente. EX(25.99, 30.00)')
    
    print('='*70)
    categoria = input('\nAgora, digite a categoria (ex: Alimentação): ').title()
    print('='*70)
    descricao = input('\nPor fim, digite a descrição (ex: Almoço): ').title()
    print('='*70)

    # --- LOOP DE VALIDAÇÃO DE DATA (NOVO!) ---
    while True:
        data_str = input('\nDigite a data do gasto (DD/MM/AAAA) ou deixe vazio para HOJE: ').strip()
        
        if not data_str:
            # Se deixou vazio, pega a data de hoje automaticamente.
            data_final = datetime.date.today().strftime('%d/%m/%Y')
            break
        else:
            try:
                # Tenta validar se o que foi digitado é uma data real.
                datetime.datetime.strptime(data_str, '%d/%m/%Y')
                data_final = data_str
                break
            except ValueError:
                 print('ERRO: Data inválida. Use o formato DD/MM/AAAA (ex: 31/12/2023)')
    # -----------------------------------------

    # Cria o novo objeto Gasto com todas as informações (incluindo data).
    novo_gasto = Gasto(valor, categoria, descricao, data_final)
    lista_de_gastos.append(novo_gasto)

    print('\n>>> Maravilha, gasto anotado com sucesso! <<<')
    print('='*70)
# --- FIM DA GAVETA 1 ---


# --- GAVETA 2: MOSTRAR RELATÓRIO ---
# Mostra todos os gastos da lista na tela.
def mostrar_relatorio():
    print('\n================================')
    print('       RELATÓRIO FINAL DE GASTOS')
    print('================================')

    if len(lista_de_gastos) == 0:
        print('Você não registrou nenhum gasto ainda.')
    else:
        total_gasto = 0.0
        for gasto in lista_de_gastos:
            # Agora mostrando a DATA no relatório também!
            print(f"DATA: {gasto.data} | CATEGORIA: {gasto.categoria} | DESCRIÇÃO: {gasto.descricao} | R$ {gasto.valor:.2f}")
            total_gasto += gasto.valor

        print('--------------------------------')
        print(f'Total de gastos: R$ {total_gasto:.2f}')
        print(f'Número de registros: {len(lista_de_gastos)}')
# --- FIM DA GAVETA 2 ---


# --- GAVETA 5: REMOVER GASTO (NOVO!) ---
# Permite ao usuário apagar um gasto da lista.
def remover_gasto():
    print('\n--- Remover Gasto ---')
    print('='*70)

    if len(lista_de_gastos) == 0:
        print('Não há gastos para remover.')
        return

    # Mostra a lista numerada (começando do 1)
    print('LISTA DE GASTOS:')
    for i, gasto in enumerate(lista_de_gastos, start=1):
        print(f"[{i}] DATA: {gasto.data} | R$ {gasto.valor:.2f} | {gasto.descricao}")
    print('='*70)

    while True:
        try:
            opcao = int(input('Digite o NÚMERO do gasto para remover (0 para cancelar): '))
            
            if opcao == 0:
                print('\nOperação cancelada.')
                break
            
            # Valida se o número escolhido existe na lista
            if 1 <= opcao <= len(lista_de_gastos):
                # Usa 'opcao - 1' porque a lista interna começa do 0
                indice_real = opcao - 1
                gasto_removido = lista_de_gastos.pop(indice_real)
                print(f'\n>>> Gasto "{gasto_removido.descricao}" (R$ {gasto_removido.valor:.2f}) removido! <<<')
                break
            else:
                print(f'ERRO: Número inválido. Digite entre 1 e {len(lista_de_gastos)}.')

        except ValueError:
            print('ERRO: Digite apenas números inteiros.')
# --- FIM DA GAVETA 5 ---


# --- GAVETA 4: SALVAR DADOS ---
# Transforma os objetos em dicionários e salva no arquivo JSON.
def salvar_dados():
    try:
        with open(ARQUIVO_DE_GASTOS, 'w') as f:
            lista_para_salvar = [g.para_dicionario() for g in lista_de_gastos]
            json.dump(lista_para_salvar, f, indent=4)
        print('\n>>> Gastos salvos com sucesso! <<<')
    except Exception as e:
        print(f'ERRO AO SALVAR: {e}')
# --- FIM DA GAVETA 4 ---


# --- LOOP PRINCIPAL (MENU) ---
while True:
    print('\n============================')
    print('       MENU PRINCIPAL')
    print('============================')
    print(f'Gastos registrados: {len(lista_de_gastos)}')
    print('[1] Adicionar novo gasto')
    print('[2] Ver relatório')
    print('[3] Remover gasto')    # NOVA OPÇÃO
    print('[4] Sair e Salvar')    # NOVA OPÇÃO

    opcao = input('Escolha uma opção: ').strip()

    if opcao == '1':
        adicionar_gasto()
    elif opcao == '2':
        mostrar_relatorio()
    elif opcao == '3':        # NOVA CHAMADA
        remover_gasto()
    elif opcao == '4':        # ATUALIZADO PARA 4
        salvar_dados()
        print('\nObrigado por usar o Bot de Gastos. Até mais!')
        break
    else:
        print('\nERRO: Opção inválida!')
# --- FIM DO PROGRAMA ---