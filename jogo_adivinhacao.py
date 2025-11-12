# jogo_adivinhacao.py

import random
from datetime import datetime
import os
import ast #lê os dicionarios no formato .txt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================
# Sistema de Jogo de Adivinhação
# ============================================

jogadores = {} # {usuario: {nome, data_cadastro}}
partidas = [] # Lista de todas as partidas
contador_partidas = 1

# Configurações do jogo
MIN_NUMERO = 1
MAX_NUMERO = 100
MAX_TENTATIVAS = 10
PONTUACAO_BASE = 100
PENALIDADE_TENTATIVA = 10

# Caminho dos arquivos
CAMINHO_JOGADORES = 'dados/jogadores.txt'
CAMINHO_PARTIDAS = 'dados/partidas.txt'

# ============================================
# FUNÇÕES DE JOGADORES
# ============================================

def cadastrar_jogador(nome, usuario):
    """
    Cadastra um novo jogador.
    
    Args:
        nome (str): Nome completo do jogador
        usuario (str): Nome de usuário único
    
    Returns:
        dict: Dados do jogador cadastrado
    """
    # TODO: Verificar se usuário já existe ------ FEITO
    # TODO: Criar dicionário do jogador ------ FEITO
    # TODO: Adicionar data de cadastro ------ FEITO
    # TODO: Adicionar ao dicionário jogadores ------ FEITO

    if (usuario in jogadores):
        print("O jogador já foi cadastrado!")
        return None
    else:
        data_cadastro = datetime.now()

        #adicionando um novo jogador
        novo_jogador = { 
            usuario: {
                'nome': nome, 
                'data_cadastro': data_cadastro
            } 
        }
        jogadores.update(novo_jogador)     

        print(f"Jogador {usuario} cadastrado com sucesso!")       
        return novo_jogador[usuario]  
        

def login_jogador(usuario):
    """
    Verifica se jogador existe e retorna dados.
    
    Args:
        usuario (str): Nome de usuário
    
    Returns:
        dict: Dados do jogador ou None
    """
    # TODO: Verificar se existe no dicionário ------ FEITO
    # TODO: Retornar dados do jogador ------ FEITO
    if (usuario in jogadores):
        return jogadores[usuario]
    else:
        print("Usuário não foi encontrado!")
        return None


# ============================================
# FUNÇÕES DE JOGO
# ============================================


def gerar_numero_secreto():
    """
    Gera um número aleatório no intervalo configurado.
    
    Returns:
        int: Número secreto
    """
    numero_secreto = random.randint(MIN_NUMERO, MAX_NUMERO)
    return numero_secreto


def calcular_pontuacao(total_tentativas):
    """
    Calcula pontuação da partida baseada em tentativas.
    
    Args:
        total_tentativas (int): Número de tentativas usadas
    
    Returns:
        int: Pontuação (0-100)
    """
    # TODO: Calcular: PONTUACAO_BASE - (tentativas * PENALIDADE) ------ FEITO
    # TODO: Garantir que não seja negativo ------ FEITO
    
    tentativas = total_tentativas - 1
    PONTUACAO_FINAL = PONTUACAO_BASE - (tentativas * PENALIDADE_TENTATIVA)
    #PONTUACAO_FINAL = PONTUACAO_BASE - (total_tentativas * PENALIDADE_TENTATIVA)
    return max(0, PONTUACAO_FINAL)


def jogar_partida(usuario):
    """
    Executa uma partida completa do jogo.
    
    Args:
        usuario (str): Usuário do jogador
    
    Returns:
        dict: Dados da partida
    """
    global contador_partidas
    
    # TODO: Gerar número secreto ------- FEITO
    # TODO: Inicializar variáveis (tentativas, lista_tentativas) ------- FEITO
    # TODO: Loop while para tentativas ------- FEITO
    # TODO: Validar entrada do usuário ------- FEITO
    # TODO: Comparar com número secreto -------- FEITO
    # TODO: Dar dicas (maior/menor) -------- FEITO
    # TODO: Registrar tentativa ------- FEITO
    # TODO: Verificar vitória ou derrota ------- FEITO
    # TODO: Calcular pontuação -------- FEITO
    # TODO: Criar dicionário da partida ------- FEITO
    # TODO: Adicionar à lista de partidas ------- FEITO
    # TODO: Incrementar contador ------- FEITO

    numero_secreto = gerar_numero_secreto()

    tentativas = 1

    lista_tentativas = []

    while (tentativas <= MAX_TENTATIVAS):

        entrada_usuario = input("\nEscolha um número entre 0 - 100: ")
        numero_escolhido = validar_numero(entrada_usuario)

        if numero_escolhido is None:
            continue

        lista_tentativas.append(numero_escolhido)

        if numero_escolhido == numero_secreto: #ver se acertou
            break
        else: #ver se errou e exibir dica
            tentativas += 1
            exibir_dica(numero_escolhido, numero_secreto)

    if (numero_escolhido == numero_secreto):
        resultado = "VITÓRIA"
        PONTUACAO_FINAL = calcular_pontuacao(tentativas)
        print(f"Parabéns {usuario}!! Você acertou o número em {tentativas} tentativas.")
    else:
        resultado = "DERROTA"
        PONTUACAO_FINAL = calcular_pontuacao(tentativas)
        print(f"Não foi dessa vez {usuario}, mais sorte na próxima!")

    partida_atual = {
        'id': contador_partidas,
        'jogador': usuario,
        'numero_secreto': numero_secreto,
        'tentativas': lista_tentativas,
        'total_tentativas': tentativas if resultado == "VITÓRIA" else MAX_TENTATIVAS, #garante que derrotas registrem 10
        'pontuacao': PONTUACAO_FINAL,
        'resultado': resultado,
        'data': datetime.now()
    }

    partidas.append(partida_atual)

    contador_partidas += 1

    return partida_atual


# ============================================
# FUNÇÃO DE CONVERSÃO PARA DATAFRAME
# ============================================


def get_partidas_df():
    """
    Converte a lista global 'partidas' em um DataFrame do Pandas
    para análise.
    """
    if not partidas:
        #retorna o dataframe vazio com colunas definidas para evitar erros
        return pd.DataFrame(columns=[
            'id', 'jogador', 'numero_secreto', 'tentativas', 
            'total_tentativas', 'pontuacao', 'resultado', 'data'
        ])
    
    df = pd.DataFrame(partidas)
    
    #limpando os tipos de dados
    df['data'] = pd.to_datetime(df['data'])
    df['pontuacao'] = df['pontuacao'].astype(int)
    df['total_tentativas'] = df['total_tentativas'].astype(int)
    return df


# ============================================
# FUNÇÕES DE ESTATÍSTICAS
# ============================================


def calcular_estatisticas_jogador(usuario):
    """
    Calcula estatísticas completas de um jogador.
    
    Args:
        usuario (str): Usuário do jogador
    
    Returns:
        dict: Estatísticas do jogador
    """
    # TODO: Filtrar partidas do jogador ---- FEITO
    # TODO: Calcular totais (partidas, vitórias, derrotas) ---- FEITO
    # TODO: Calcular taxa de vitória ---- FEITO
    # TODO: Calcular média de tentativas ---- FEITO
    # TODO: Encontrar melhor pontuação ---- FEITO
    # TODO: Calcular pontuação total ---- FEITO
    # TODO: Criar dicionário de estatísticas ---- FEITO
    df_partidas = get_partidas_df()
    
    #filtra partidas do jogador
    df_jogador = df_partidas[df_partidas['jogador'] == usuario]
    
    total_de_partidas = len(df_jogador)

    if total_de_partidas == 0:
        return {
            'total_partidas': 0, 'total_vitorias': 0, 'total_derrotas': 0,
            'taxa_vitoria': 0.0, 'media_tentativas': 0.0,
            'melhor_pontuacao': 0, 'pontuacao_total': 0, 'media_pontuacao': 0.0
        }

    total_vitorias = len(df_jogador[df_jogador['resultado'] == 'VITÓRIA'])
    total_derrotas = total_de_partidas - total_vitorias
    taxa_vitoria = (total_vitorias / total_de_partidas) * 100
    
    media_tentativas_jogador = df_jogador['total_tentativas'].mean()
    melhor_pontuacao = df_jogador['pontuacao'].max()
    pontuacao_total = df_jogador['pontuacao'].sum()
    media_pontuacao = df_jogador['pontuacao'].mean()

    estatisticas = {
        'total_partidas': int(total_de_partidas),
        'total_vitorias': int(total_vitorias),
        'total_derrotas': int(total_derrotas),
        'taxa_vitoria': float(taxa_vitoria),
        'media_tentativas': float(media_tentativas_jogador),
        'melhor_pontuacao': int(melhor_pontuacao),
        'pontuacao_total': int(pontuacao_total),
        'media_pontuacao': float(media_pontuacao)
    }

    return estatisticas
    """
    Calcula média de tentativas por partida de um jogador.
    
    Args:
        usuario (str): Usuário do jogador
    
    Returns:
        float: Média de tentativas
    """
    # TODO: Filtrar partidas do jogador ----- FEITO
    # TODO: Extrair número de tentativas ----- FEITO
    # TODO: Calcular média ----- FEITO
    
    partidas_do_jogador = []
    for partida in partidas:
        if partida['jogador'] == usuario:
            partidas_do_jogador.append(partida)
    
    total_de_partidas = len(partidas_do_jogador)

    if total_de_partidas == 0: #checar se é zero para evitar problemas de divisão
        return 0.0

    total_tentativas = 0
    for partida in partidas_do_jogador:
        total_tentativas += partida['total_tentativas']

    media = total_tentativas / total_de_partidas

    return media


#removi as funções de taxa de vitoria e media de tentativa, pois agora estão todas na calcular_estatisticas_jogador


# ============================================
# FUNÇÕES DE RANKINGS
# ============================================


def ranking_pontuacao_media(limite=10):
    """
    Gera ranking por pontuação média.
    
    Args:
        limite (int): Quantidade de jogadores no ranking
    
    Returns:
        list: Lista de tuplas (usuario, pontuacao_media)
    """
    # TODO: Calcular estatísticas de todos os jogadores ----- FEITO
    # TODO: Calcular pontuação média ----- FEITO
    # TODO: Ordenar por pontuação (decrescente) ----- FEITO
    # TODO: Retornar top N ----- FEITO
    df = get_partidas_df()
    if df.empty:
        return []
    
    media_pontuacao = df.groupby('jogador')['pontuacao'].mean().sort_values(ascending=False)
    
    lista_pontuacao = list(media_pontuacao.to_dict().items())
    return lista_pontuacao[:limite]


def ranking_vitorias(limite=10):
    """
    Gera ranking por número de vitórias.
    
    Args:
        limite (int): Quantidade de jogadores no ranking
    
    Returns:
        list: Lista de tuplas (usuario, vitorias)
    """
    # TODO: Calcular vitorias por jogador ----- FEITO
    # TODO: Ordenar por vitórias (decrescente) ----- FEITO
    # TODO: Retornar top N ----- FEITO
    df = get_partidas_df()
    if df.empty:
        return []
        
    df_vitorias = df[df['resultado'] == 'VITÓRIA']
    if df_vitorias.empty: #verifica se tem vitórias
        return []
        
    contador_vitorias = df_vitorias.groupby('jogador')['id'].count().sort_values(ascending=False)
    
    lista_vitorias = list(contador_vitorias.to_dict().items())
    return lista_vitorias[:limite]


def ranking_melhor_pontuacao(limite=10):
    """
    Gera ranking por melhor pontuação única.
    
    Args:
        limite (int): Quantidade de jogadores no ranking
    
    Returns:
        list: Lista de tuplas (usuario, melhor_pontuacao)
    """
    # TODO: Encontrar melhor pontuação de cada jogador ----- FEITO
    # TODO: Ordenar por pontuação (decrescente) ----- FEITO
    # TODO: Retornar top N ----- FEITO
    df = get_partidas_df()
    if df.empty:
        return []
        
    lista_pontuacao = df.groupby('jogador')['pontuacao'].max().sort_values(ascending=False)
    
    rank_pontuacao = list(lista_pontuacao.to_dict().items())
    return rank_pontuacao[:limite]



# ============================================
# FUNÇÕES DE RELATÓRIOS
# ============================================


def exibir_estatisticas_jogador(usuario):
    """
    Exibe estatísticas formatadas de um jogador.
    
    Args:
        usuario (str): Usuário do jogador
    """
    # TODO: Calcular estatísticas ------ FEITO
    # TODO: Formatar e exibir com f-strings ------ FEITO

    estatisticas = calcular_estatisticas_jogador(usuario)   
    nome_jogador = jogadores[usuario]['nome']
    print(f"\n--- Estatísticas do Jogador: {usuario} ({nome_jogador}) ---")
    print(f"  Total de Partidas: {estatisticas['total_partidas']}")
    print(f"  Vitórias: {estatisticas['total_vitorias']}")
    print(f"  Derrotas: {estatisticas['total_derrotas']}")
    print(f"  Taxa de Vitória: {estatisticas['taxa_vitoria']:.1f}%")
    print(f"  Média de Tentativas: {estatisticas['media_tentativas']:.1f}")
    print(f"  Melhor Pontuação: {estatisticas['melhor_pontuacao']}")
    print(f"  Pontuação Total: {estatisticas['pontuacao_total']}")
    print(f"--------------------------------------------------")


def exibir_ranking():
    """
    Exibe ranking formatado de todos os jogadores.
    """
    # TODO: Gerar rankings ----- FEITO
    # TODO: Formatar e exibir ------ FEITO
    ranking_melhor = ranking_melhor_pontuacao()

    print(f"\n--- Ranking de Melhores Pontuações ---")
    for i, (usuario, melhor_pontuacao) in enumerate(ranking_melhor, 1):
        print(f"{i}. {usuario} - Melhor Pontuação: {melhor_pontuacao}")
    print(f"-----------------------------------------")

    rank_vitorias = ranking_vitorias()
    print(f"\n--- Ranking de Vitórias ---")
    for i, (usuario, total_vitorias) in enumerate(rank_vitorias, 1):
        print(f"{i}. {usuario} - Vitórias: {total_vitorias}")
    print(f"-----------------------------------------")

    ranking_media = ranking_pontuacao_media()
    print(f"\n--- Ranking de Pontuação Média ---")
    for i, (usuario, pontuacao_media) in enumerate(ranking_media, 1):
        print(f"{i}. {usuario} - Pontuação Média: {pontuacao_media:.1f}")
    print(f"-----------------------------------------")


def historico_partidas(usuario, limite=10):
    """
    Retorna histórico recente de partidas de um jogador.
    
    Args:
        usuario (str): Usuário do jogador
        limite (int): Quantidade de partidas a retornar
    
    Returns:
        list: Lista de partidas recentes
    """
    # TODO: Filtrar partidas do jogador ---- FEITO
    # TODO: Ordenar por data (mais recente primeiro) ---- FEITO
    # TODO: Retornar top N ---- FEITO
    partidas_do_jogador = []
    for partida in partidas:
        if partida['jogador'] == usuario:
            partidas_do_jogador.append(partida)

    # Ordenar por data (mais recente primeiro)
    partidas_do_jogador.sort(key=lambda x: x['data'], reverse=True)

    # Retornar top N
    return partidas_do_jogador[:limite]

# ============================================
# FUNÇÕES AUXILIARES
# ============================================


def validar_numero(entrada):
    """
    Valida se entrada é um número válido no intervalo.
    
    Args:
        entrada (str): Entrada do usuário
    
    Returns:
        int: Número validado ou None
    """
    # TODO: Tentar converter para int ----- FEITO
    # TODO: Verificar se está no intervalo
    # TODO: Retornar número ou None
    try:
        numero = int(entrada)

        if (numero >= MIN_NUMERO) and (numero <= MAX_NUMERO):
            return numero
        else:
            print("Por favor, digite um número entre 1 e 100.")
            return None
        
    except ValueError:
        print("Entrada inválida. Digite apenas números.")
        return None


def exibir_dica(numero_escolhido, numero_secreto):
    """
    Exibe dica se número é maior ou menor.
    
    Args:
        numero_escolhido (int): Número escolhido pelo jogador
        numero_secreto (int): Número secreto
    """
    # TODO: Comparar números
    # TODO: Exibir mensagem apropriada
    if numero_escolhido < numero_secreto:
        print("O número escolhido é MENOR que o número secreto!")
    elif numero_escolhido > numero_secreto:
        print("O número escolhido é MAIOR que o número secreto!")


# ============================================
# FUNÇÕES DE VISUALIZAÇÃO
# ============================================

sns.set_theme(style="whitegrid", palette="pastel") #deixar os gráficos mais bonitos

def grafico_historico_individual(usuario, estatisticas):
    """
    Gera e exibe um gráfico de linha com o histórico de
    pontuação do jogador e sua média.
    """
    df = get_partidas_df()
    df_jogador = df[df['jogador'] == usuario].sort_values(by='data')

    if df_jogador.empty:
        print("Você ainda não tem partidas registradas.")
        return
    
    media = estatisticas['media_pontuacao']

    plt.figure(figsize=(12, 6))
    
    #gráfico de linha
    ax = sns.lineplot(data=df_jogador, x='data', y='pontuacao', marker='o', label='Pontuação da Partida', color='C0')
    ax.fill_between(df_jogador['data'], df_jogador['pontuacao'], color='C0', alpha=0.2)

    #faixa da média
    ax.axhline(y=media, color='#E74C3C', linestyle='--', label=f'Sua Média ({media:.1f} pts)')

    ax.set_title(f'Sua Evolução - {usuario}', fontsize=16, weight='bold')
    ax.set_xlabel('Data da Partida', fontsize=12)
    ax.set_ylabel('Pontuação Obtida', fontsize=12)
    ax.set_ylim(0, 110) #limite superior para melhor visualização
    ax.legend()
    
    #remoção de bordas
    sns.despine() 
    plt.tight_layout()
    
    caminho_salvar = f'relatorios/grafico_historico_{usuario}.png'
    plt.savefig(caminho_salvar)
    print(f"Gráfico de histórico salvo em: {caminho_salvar}")
    
    print("\nExibindo gráfico 'Sua Evolução'...")
    plt.show()


def grafico_ranking_vitorias_global(limite=10):
    """
    Gera e exibe um gráfico de barras (Seaborn) com o
    ranking de vitórias, incluindo rótulos de dados.
    """
    df = get_partidas_df()
    if df.empty:
        print("Sem dados de partidas.")
        return

    vitorias = df[df['resultado'] == 'VITÓRIA']
    if vitorias.empty:
        print("Nenhuma vitória registrada.")
        return
        
    rank_vitorias = vitorias['jogador'].value_counts().head(limite)
    ranking_df = rank_vitorias.reset_index()
    ranking_df.columns = ['jogador', 'total_vitorias']

    plt.figure(figsize=(12, 7))
    
    #gráfico de barras horizontais
    ax = sns.barplot(x='total_vitorias', y='jogador', data=ranking_df, palette='viridis_r', hue='jogador', legend=False, dodge=False)   

    ax.set_title(f'Ranking: Jogadores com Mais Vitórias (Top {limite})', fontsize=16, weight='bold')
    ax.set_xlabel('Total de Vitórias', fontsize=12)
    ax.set_ylabel('Jogador', fontsize=12)
    
    #escrevendo o número de vitórias ao lado de cada barra
    for p in ax.patches:
        ax.annotate(f'{int(p.get_width())} vitórias', xy=( (p.get_width() + 0.1) , (p.get_y() + p.get_height() / 2) ), ha='left', va='center', color='black', fontsize=10, weight='bold')
    
    ax.set_xlim(0, ranking_df['total_vitorias'].max() * 1.1) 
    
    sns.despine(left=True)
    plt.tight_layout()
    
    caminho_salvar = 'relatorios/grafico_ranking_vitorias.png'
    plt.savefig(caminho_salvar)
    print(f"Gráfico de ranking salvo em: {caminho_salvar}")
    
    print("\nExibindo gráfico 'Ranking Global de Vitórias'...")
    plt.show()


def grafico_distribuicao_global():
    """
    Gera e exibe:
    1. Histograma de Pontuações (com linha de média).
    2. Gráfico de Barras de Tentativas (substituindo o Boxplot).
    """
    df = get_partidas_df()
    if df.empty:
        print("Sem dados de partidas.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.suptitle('Análise Geral do Jogo (Todas as Partidas)', fontsize=18, weight='bold')
    
    #gráfico das melhores pontuações
    df_vitorias = df[df['resultado'] == 'VITÓRIA']
    if not df_vitorias.empty:
        media_pontos = df_vitorias['pontuacao'].mean()
        
        sns.histplot(data=df_vitorias, x='pontuacao', bins=10, kde=True, ax=axes[0], color='#0056b3', line_kws={'lw': 3, 'color': '#0056b3'})
        
        #linha da média
        axes[0].axvline(media_pontos, color='#E74C3C', linestyle='--', lw=2, label=f'Média ({media_pontos:.1f} pts)')
        
        axes[0].set_title('Como as Pontuações se Distribuem? (em Vitórias)', fontsize=14)
        axes[0].set_xlabel('Pontuação', fontsize=12)
        axes[0].set_ylabel('Número de Partidas', fontsize=12)
        axes[0].legend()
    else:
        axes[0].set_title('Nenhuma vitória registrada para analisar pontuações.')

    #gráfico distribuição de tentativas
    
    todas_tentativas_possiveis = pd.Categorical(df['total_tentativas'], categories=range(1, MAX_TENTATIVAS + 1), ordered=True)

    sns.histplot(data=df, x='total_tentativas', bins=10, kde=True, ax=axes[1], color='#00b306', line_kws={'lw': 3, 'color': "#00b306"})
    
    axes[1].set_title('Quantas Tentativas São Mais Comuns? (Geral)', fontsize=14)
    axes[1].set_xlabel('Número de Tentativas Usadas na Partida', fontsize=12)
    axes[1].set_ylabel('Número de Partidas', fontsize=12)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) #ajeita o título principal
    
    caminho_salvar = 'relatorios/grafico_distribuicao_global.png'
    plt.savefig(caminho_salvar)
    print(f"Gráfico de distribuição salvo em: {caminho_salvar}")
    
    print("\nExibindo gráfico 'Análise Geral do Jogo'...")
    plt.show()


# ============================================
# SALVANDO E CARREGANDO DADOS E RELATÓRIOS
# ============================================


def salvar_dados_txt(jogadores, partidas):
    """
    Salva os dados de jogadores e partidas nos arquivos .txt.
    """
    
    #formata para escrever no jogadores.txt
    jogadores_para_salvar = {}
    for usuario, dados in jogadores.items():
        jogadores_para_salvar[usuario] = {
            'nome': dados['nome'],
            'data_cadastro': dados['data_cadastro'].isoformat() 
        }
    
    #adiciona os jogadores
    try:
        with open(CAMINHO_JOGADORES, 'w', encoding='utf-8') as f:
            f.write(str(jogadores_para_salvar))
    except Exception as e:
        print(f"Erro ao salvar jogadores.txt: {e}")

    #formata as partidas para escrever no partidas.txt
    partidas_para_salvar = []
    for partida in partidas:
        partida_copia = partida.copy()
        partida_copia['data'] = partida['data'].isoformat() #convertendo datetime para string
        partidas_para_salvar.append(partida_copia)

    #salva as partidas
    try:
        with open(CAMINHO_PARTIDAS, 'w', encoding='utf-8') as f:
            f.write(str(partidas_para_salvar))
    except Exception as e:
        print(f"Erro ao salvar partidas.txt: {e}")


def carregar_dados_txt():
    """
    Carrega os dados de jogadores e partidas dos arquivos .txt.
    """
    global jogadores, partidas, contador_partidas

    #carregando jogadores.txt
    if os.path.exists(CAMINHO_JOGADORES):
        try:
            with open(CAMINHO_JOGADORES, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                jogadores_carregados = ast.literal_eval(conteudo) #transformar dados de texto para dicionário
                
                #converte strings de volta para o datetime
                for usuario, dados in jogadores_carregados.items():
                    dados['data_cadastro'] = datetime.fromisoformat(dados['data_cadastro'])
                
                jogadores = jogadores_carregados
        except Exception as e:
            print(f"Erro ao carregar jogadores.txt: {e}")

    #carregando partidas.txt
    if os.path.exists(CAMINHO_PARTIDAS):
        try:
            with open(CAMINHO_PARTIDAS, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                partidas_carregadas = ast.literal_eval(conteudo)
                
                for partida in partidas_carregadas:
                    partida['data'] = datetime.fromisoformat(partida['data'])
                
                partidas = partidas_carregadas
                
                #atualiza contador de partidas
                if partidas:
                    contador_partidas = max(p['id'] for p in partidas) + 1
        except Exception as e:
            print(f"Erro ao carregar partidas.txt: {e}")

    print("\nDados carregados com sucesso")


def salvar_relatorio_individual(usuario):
    """
    Gera as estatísticas de um jogador e salva em um arquivo .txt
    na pasta /relatorios.
    """
    try:
        estatisticas = calcular_estatisticas_jogador(usuario)
        nome_jogador = jogadores[usuario]['nome']
    except Exception as e:
        print(f"Erro ao calcular estatísticas: {e}")

    linhas_relatorio = [
        f"--- Relatório de Desempenho Individual ---\n",
        f"Jogador: {usuario} ({nome_jogador})\n",
        f"Relatório gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        f"--------------------------------------------------\n",
        f"  Total de Partidas: {estatisticas['total_partidas']}\n",
        f"  Vitórias: {estatisticas['total_vitorias']}\n",
        f"  Derrotas: {estatisticas['total_derrotas']}\n",
        f"  Taxa de Vitória: {estatisticas['taxa_vitoria']:.1f}%\n",
        f"  Média de Tentativas: {estatisticas['media_tentativas']:.1f}\n",
        f"  Melhor Pontuação: {estatisticas['melhor_pontuacao']}\n",
        f"  Pontuação Total: {estatisticas['pontuacao_total']}\n",
        f"--------------------------------------------------\n"
    ]

    caminho_arquivo = f"relatorios/estatisticas_{usuario}.txt"
    try:
        with open(caminho_arquivo, "w", encoding='utf-8') as f:
            f.writelines(linhas_relatorio)
    except Exception as e:
        print(f"Erro ao salvar relatório em '{caminho_arquivo}': {e}")


def salvar_relatorio_rankings(limite=10):
    """
    Gera o relatório geral de todos os jogadores (rankings)
    e salva em um arquivo .txt na pasta /relatorios.
    """
    try:
        rank_vitorias = ranking_vitorias(limite)
        rank_melhor = ranking_melhor_pontuacao(limite)
        ranking_media = ranking_pontuacao_media(limite)
    except Exception as e:
        print(f"Erro ao calcular rankings para salvar: {e}")
        return

    linhas_relatorio = [
        f"--- Relatório Geral de Jogadores (Rankings) ---\n",
        f"Relatório gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        f"\n--- Top 10 por Vitórias ---\n"
    ]
    for i, (usr, vitorias) in enumerate(rank_vitorias, 1):
        linhas_relatorio.append(f"  {i}. {usr} - Vitórias: {vitorias}\n")
    
    linhas_relatorio.append("\n--- Top 10 por Melhor Pontuação ---\n")
    for i, (usr, pont) in enumerate(rank_melhor, 1):
        linhas_relatorio.append(f"  {i}. {usr} - Melhor Pontuação: {pont}\n")
        
    linhas_relatorio.append("\n--- Top 10 por Pontuação Média ---\n")
    for i, (usr, media) in enumerate(ranking_media, 1):
        linhas_relatorio.append(f"  {i}. {usr} - Pontuação Média: {media:.1f}\n")

    caminho_arquivo = f"relatorios/rankings_gerais.txt"
    try:
        with open(caminho_arquivo, "w", encoding='utf-8') as f:
            f.writelines(linhas_relatorio)
    except Exception as e:
        print(f"Erro ao salvar relatório em '{caminho_arquivo}': {e}")


def salvar_historico_individual(usuario, historico_dados, limite):
    """
    Gera o histórico de partidas recentes de um jogador
    e salva em um arquivo .txt na pasta /relatorios.
    """
    #pega os dados do histórico de partidas do usuário
    try:
        historico = historico_partidas(usuario, limite)
    except Exception as e:
        print(f"Erro ao buscar histórico para salvar: {e}")
        return

    #formatando a parte de histórico de partidas do jogador logado
    linhas_relatorio = [
        f"--- Histórico de Partidas Recentes ---\n",
        f"Jogador: {usuario}\n",
        f"Mostrando as últimas {len(historico)} partidas.\n",
        f"Relatório gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        f"--------------------------------------------------\n"
    ]
    
    if not historico:
        linhas_relatorio.append("Nenhuma partida encontrada.\n")
    else:
        for p in historico:
            data_formatada = p['data'].strftime('%Y-%m-%d %H:%M')
            linha = f"  ID {p['id']} | {data_formatada} | {p['resultado']} | Tentativas: {p['total_tentativas']} | Pontos: {p['pontuacao']}\n"
            linhas_relatorio.append(linha)

    #salvando o histórico do usuário
    caminho_arquivo = f"relatorios/historico_{usuario}.txt"
    try:
        with open(caminho_arquivo, "w", encoding='utf-8') as f:
            f.writelines(linhas_relatorio)
    except Exception as e:
        print(f"Erro ao salvar relatório em '{caminho_arquivo}': {e}")


# ============================================
# FUNÇÃO PRINCIPAL
# ============================================


def main():
    """
    Função principal do programa.
    """
    usuario_logado = None

    while True:
        
        # menu principal deslogado
        if usuario_logado is None:
            print("\n--- BEM-VINDO AO JOGO DE ADIVINHAÇÃO ---")
            print("1. Cadastrar novo jogador")
            print("2. Fazer login")
            print("3. Sair do Jogo")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                #cadastro
                nome = input("Digite seu nome completo: ")
                usuario = input("Digite seu nome de usuário (único): ")
                cadastrar_jogador(nome, usuario)
            
            elif opcao == '2':
                #login
                usuario = input("Digite seu nome de usuário: ")
                dados_jogador = login_jogador(usuario)
                if dados_jogador:
                    print(f"Login bem-sucedido! Bem-vindo, {dados_jogador['nome']}!")
                    usuario_logado = usuario

            elif opcao == '3':
                #sair do jogo
                print("Salvando dados...")
                salvar_dados_txt(jogadores, partidas)
                print("Obrigado por jogar! Até mais.")
                break
            
            else:
                print("Opção inválida. Tente novamente.")
        
        #menu principal logado
        else:
            print(f"\n--- JOGO (Logado como: {usuario_logado}) ---")
            print("1. Jogar uma nova partida")
            print("2. Ver minhas estatísticas (com gráficos)")
            print("3. Ver meu histórico de partidas")
            print("4. Ver rankings globais (com gráficos)")
            print("5. Fazer logout (Voltar ao menu principal)")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                #jogar partida
                partida_info = jogar_partida(usuario_logado)
                print(f"Partida {partida_info['id']} registrada. Pontuação: {partida_info['pontuacao']}")

            elif opcao == '2':
                #estatísticas do jogador
                print("Calculando estatísticas...")
                exibir_estatisticas_jogador(usuario_logado)
                
                estatisticas = calcular_estatisticas_jogador(usuario_logado)
                if estatisticas['total_partidas'] > 0:
                    salvar_relatorio_individual(usuario_logado)
                    grafico_historico_individual(usuario_logado, estatisticas)
                else:
                    print("Nenhuma partida encontrada.")

            elif opcao == '3':
                #histórico de partidas do jogador
                print("Buscando histórico de partidas...")
                limite_historico = 5
                historico = historico_partidas(usuario_logado, limite_historico)
                print(f"\n--- {limite_historico} Últimas Partidas de {usuario_logado} ---")
                
                if not historico:
                    print("Nenhuma partida encontrada.")
                else:
                    for p in historico:
                        data_formatada = p['data'].strftime('%Y-%m-%d %H:%M')
                        print(f"  ID {p['id']} | {data_formatada} | {p['resultado']} | Tentativas: {p['total_tentativas']} | Pontos: {p['pontuacao']}")
                
                if historico:
                    salvar_historico_individual(usuario_logado, historico, limite_historico)

            elif opcao == '4':
                #rankings globais
                print("\n--- RANKINGS GLOBAIS ---")
                exibir_ranking()
                
                if partidas:
                    salvar_relatorio_rankings()
                    grafico_ranking_vitorias_global()
                    grafico_distribuicao_global()
                else:
                    print("Nenhuma partida encontrada.")

            elif opcao == '5':
                #logout
                print(f"Salvando dados de {usuario_logado}...")
                salvar_dados_txt(jogadores, partidas)
                print(f"Até logo, {usuario_logado}!")
                usuario_logado = None
            
            else:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    carregar_dados_txt()
    main()