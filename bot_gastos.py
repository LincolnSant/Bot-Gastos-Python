import json
import os

ARQUIVO_DE_GASTOS = 'gastos.json'

# --- CLASSE GASTO (A Planta do Robô) ---
class Gasto:
    def __init__(self, valor, categoria, descricao):
        self.valor = valor
        self.categoria = categoria
        self.descricao = descricao

    def para_dicionario(self):
        return {
            'valor': self.valor,
            'cat': self.categoria,
            'desc': self.descricao
        }
# ---------------------------------------

# --- GAVETA 3: CARREGAR DADOS ---
def carregar_dados():
    if not os.path.exists(ARQUIVO_DE_GASTOS):
        return []

    try:
        with open(ARQUIVO_DE_GASTOS, 'r') as f:
            dados_brutos = json.load(f)
            
            # RECONSTRUÇÃO: Transforma os dicionários do JSON de volta em Objetos Gasto
            lista_de_objetos = []
            for gasto_dict in dados_brutos:
                gasto_obj = Gasto(
                    gasto_dict['valor'], 
                    gasto_dict['cat'], 
                    gasto_dict['desc']
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

    # CRIANDO O OBJETO (ROBÔ)
    novo_gasto = Gasto(valor, categoria, descricao)
    lista_de_gastos.append(novo_gasto)

    print('\n>>> Maravilha, gasto anotado com sucesso! <<<')
    print('='*70)
# --- FIM DA GAVETA 1 ---


# --- GAVETA 2: MOSTRAR RELATÓRIO ---
def mostrar_relatorio():
    print('\n================================')
    print('       RELATÓRIO FINAL DE GASTOS')
    print('================================')

    if len(lista_de_gastos) == 0:
        print('Você não registrou nenhum gasto ainda.')
    else:
        total_gasto = 0.0
        for gasto in lista_de_gastos:
            # Acessando os dados do OBJETO com ponto (.)
            print(f"CATEGORIA: {gasto.categoria} | DESCRIÇÃO: {gasto.descricao} | VALOR: R$ {gasto.valor:.2f}")
            total_gasto += gasto.valor # Soma o valor do objeto

        print('--------------------------------')
        print(f'Total de gastos: R$ {total_gasto:.2f}')
        print(f'Número de registros: {len(lista_de_gastos)}')
# --- FIM DA GAVETA 2 ---


# --- GAVETA 4: SALVAR DADOS ---
def salvar_dados():
    try:
        with open(ARQUIVO_DE_GASTOS, 'w') as f:
            # TRADUÇÃO: Converte os objetos em dicionários antes de salvar
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
    print('[3] Sair e Salvar')

    opcao = input('Escolha uma opção: ').strip()

    if opcao == '1':
        adicionar_gasto()
    elif opcao == '2':
        mostrar_relatorio()
    elif opcao == '3':
        salvar_dados()
        print('\nObrigado por usar o Bot de Gastos. Até mais!')
        break
    else:
        print('\nERRO: Opção inválida!')
# --- FIM DO PROGRAMA ---