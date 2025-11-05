# jogo_adivinhacao.py

import random
from datetime import datetime
import os
import ast #lê os dicionarios no formato .txt

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

        entrada_usuario = input("Escolha um número entre 0 - 100: ")
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
    partidas_do_jogador = []
    for partida in partidas:
        if partida['jogador'] == usuario:
            partidas_do_jogador.append(partida)
    
    total_de_partidas = len(partidas_do_jogador)

    if total_de_partidas == 0: #checar se é zero para evitar problemas de divisão
        estatisticas_vazias = {
            'total_partidas': 0,
            'total_vitorias': 0,
            'total_derrotas': 0,
            'taxa_vitoria': 0.0,
            'media_tentativas': 0.0,
            'melhor_pontuacao': 0,
            'pontuacao_total': 0
        }
        return estatisticas_vazias

    total_vitorias = 0
    for resul in partidas_do_jogador:
        if resul['resultado'] == "VITÓRIA":
            total_vitorias += 1

    total_derrotas = total_de_partidas - total_vitorias

    taxa_vitoria = calcular_taxa_vitoria(usuario)

    media_tentativas_jogador = media_tentativas(usuario)

    melhor_pontuacao = 0
    for partida in partidas_do_jogador:
        if partida['pontuacao'] > melhor_pontuacao:
            melhor_pontuacao = partida['pontuacao']

    pontuacao_total = 0
    for partida in partidas_do_jogador:
        pontuacao_total += partida['pontuacao']

    estatisticas = {
        'total_partidas': total_de_partidas,
        'total_vitorias': total_vitorias,
        'total_derrotas': total_derrotas,
        'taxa_vitoria': taxa_vitoria,
        'media_tentativas': media_tentativas_jogador,
        'melhor_pontuacao': melhor_pontuacao,
        'pontuacao_total': pontuacao_total
    }

    return estatisticas


def calcular_taxa_vitoria(usuario):
    """
    Calcula taxa de vitórias de um jogador.
    
    Args:
        usuario (str): Usuário do jogador
    
    Returns:
        float: Taxa de vitória (0-100)
    """
    # TODO: Filtrar partidas do jogador ----- FEITO
    # TODO: Contar vitórias e total ----- FEITO
    # TODO: Calcular percentual ----- FEITO

    #taxa de vitoria = (vitorias / tentativas) * 100

    #partidas_do_jogador = [partida for partida in partidas if partida['jogador'] == usuario]  ------ exemplo de listcomprehension, mas eu não entendo muito bem como funciona

    partidas_do_jogador = []
    for partida in partidas:
        if partida['jogador'] == usuario:
            partidas_do_jogador.append(partida)
    
    total_de_partidas = len(partidas_do_jogador)

    if total_de_partidas == 0: #checar se é zero para evitar problemas de divisão
        return 0.0

    total_vitorias = 0
    for resul in partidas_do_jogador:
        if resul['resultado'] == "VITÓRIA":
            total_vitorias += 1

    taxa_vitoria = (total_vitorias / total_de_partidas) * 100

    return taxa_vitoria


def media_tentativas(usuario):
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
    jogadores_estatisticas = {}
    for usuario in jogadores.keys():
        estatisticas = calcular_estatisticas_jogador(usuario)
        jogadores_estatisticas[usuario] = estatisticas

    pontuacao_media_jogadores = []
    for usuario, estatisticas in jogadores_estatisticas.items():
        if estatisticas['total_partidas'] > 0:
            pontuacao_media = estatisticas['pontuacao_total'] / estatisticas['total_partidas']
        else:
            pontuacao_media = 0.0
        pontuacao_media_jogadores.append((usuario, pontuacao_media))

    pontuacao_media_jogadores.sort(key=lambda x: x[1], reverse=True)
    return pontuacao_media_jogadores[:limite]


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
    jogadores_estatisticas = {}
    for usuario in jogadores.keys():    
        estatisticas = calcular_estatisticas_jogador(usuario)
        jogadores_estatisticas[usuario] = estatisticas

    vitorias_jogadores = []
    for usuario, estatisticas in jogadores_estatisticas.items():
        vitorias_jogadores.append((usuario, estatisticas['total_vitorias']))

    vitorias_jogadores.sort(key=lambda x: x[1], reverse=True)
    return vitorias_jogadores[:limite]


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

    jogadores_estatisticas = {}
    for usuario in jogadores.keys():
        estatisticas = calcular_estatisticas_jogador(usuario)
        jogadores_estatisticas[usuario] = estatisticas

    melhor_pontuacao_jogadores = []
    for usuario, estatisticas in jogadores_estatisticas.items():
        melhor_pontuacao_jogadores.append((usuario, estatisticas['melhor_pontuacao']))

    melhor_pontuacao_jogadores.sort(key=lambda x: x[1], reverse=True)
    return melhor_pontuacao_jogadores[:limite]



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
# SALVANDO E CARREGANDO DADOS E RELATÓRIOS
# ============================================


def salvar_dados_txt(jogadores, partidas):
    """
    Salva os dados de jogadores e partidas nos arquivos .txt.
    """
    
    # 1. Preparar Jogadores (Converter datetime para string)
    jogadores_para_salvar = {}
    for usuario, dados in jogadores.items():
        jogadores_para_salvar[usuario] = {
            'nome': dados['nome'],
            'data_cadastro': dados['data_cadastro'].isoformat()
        }
    
    # Escreve a string do dicionário no arquivo
    try:
        with open(CAMINHO_JOGADORES, 'w', encoding='utf-8') as f:
            f.write(str(jogadores_para_salvar))
    except Exception as e:
        print(f"Erro ao salvar jogadores.txt: {e}")

    # 2. Preparar Partidas (Converter datetime para string)
    partidas_para_salvar = []
    for partida in partidas:
        partida_copia = partida.copy()
        partida_copia['data'] = partida['data'].isoformat()
        partidas_para_salvar.append(partida_copia)

    # Escreve a string da lista no arquivo
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

    # Carregar Jogadores
    if os.path.exists(CAMINHO_JOGADORES):
        try:
            with open(CAMINHO_JOGADORES, 'r', encoding='utf-8') as f:
                conteudo = f.read()
                jogadores_carregados = ast.literal_eval(conteudo)
                
                #converte strings de volta para o datetime
                for usuario, dados in jogadores_carregados.items():
                    dados['data_cadastro'] = datetime.fromisoformat(dados['data_cadastro'])
                
                jogadores = jogadores_carregados
        except Exception as e:
            print(f"Erro ao carregar jogadores.txt: {e}")

    # Carregar Partidas
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

    print("\nDados carregados com sucesso dos arquivos .txt!")


def salvar_relatorio_individual(usuario):
    """
    Gera as estatísticas de um jogador e salva em um arquivo .txt
    na pasta /relatorios.
    """
    try:
        estatisticas = calcular_estatisticas_jogador(usuario)
        nome_jogador = jogadores[usuario]['nome']
    except Exception as e:
        print(f"Erro ao calcular estatísticas para salvar: {e}")
        return

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
    # 1. Pegar os dados
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
    try:
        linhas_relatorio = [
            f"--- Histórico de Partidas Recentes ---\n",
            f"Jogador: {usuario}\n",
            f"Mostrando as últimas {len(historico_dados)} partidas (limite de {limite}).\n",
            f"Relatório gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
            f"--------------------------------------------------\n"
        ]
        
        if not historico_dados:
            linhas_relatorio.append("Nenhuma partida encontrada.\n")
        else:
            for p in historico_dados:
                data_formatada = p['data'].strftime('%Y-%m-%d %H:%M')
                linha = f"  ID {p['id']} | {data_formatada} | {p['resultado']} | Tentativas: {p['total_tentativas']} | Pontos: {p['pontuacao']}\n"
                linhas_relatorio.append(linha)

        caminho_arquivo = f"relatorios/historico_{usuario}.txt"
        with open(caminho_arquivo, "w", encoding='utf-8') as f:
            f.writelines(linhas_relatorio)
        print(f"\nRelatório de histórico salvo com sucesso em: {caminho_arquivo}")
    
    except Exception as e:
        print(f"Erro ao salvar relatório de histórico: {e}")
    """
    Gera o histórico de partidas recentes de um jogador
    e salva em um arquivo .txt na pasta /relatorios.
    """
    # 1. Pegar os dados
    try:
        historico = historico_partidas(usuario, limite)
    except Exception as e:
        print(f"Erro ao buscar histórico para salvar: {e}")
        return

    # 2. Definir o conteúdo
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

    # 3. Salvar no arquivo
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
    # TODO: Menu interativo ----- FEITO
    # TODO: Opções: cadastrar, login, jogar, estatísticas, ranking, sair ----- FEITO
    
    usuario_logado = None

    while True:
        
        # --- MENU 1: ESTADO "DESLOGADO" ---
        if usuario_logado is None:
            print("\n--- BEM-VINDO AO JOGO DE ADIVINHAÇÃO ---")
            print("1. Cadastrar novo jogador")
            print("2. Fazer login")
            print("3. Sair do Jogo")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                # --- CADASTRAR ---
                nome = input("Digite seu nome completo: ")
                usuario = input("Digite seu nome de usuário (único): ")
                #a função cadastrar_jogador já imprime se deu certo ou errado
                cadastrar_jogador(nome, usuario)
            
            elif opcao == '2':
                # --- LOGIN ---
                usuario = input("Digite seu nome de usuário: ")
                dados_jogador = login_jogador(usuario) 
                
                if dados_jogador:
                    print(f"Login bem-sucedido! Bem-vindo, {dados_jogador['nome']}!")
                    usuario_logado = usuario
                #a função login_jogador já imprime o erro se falhar)

            elif opcao == '3':
                # --- SAIR ---
                salvar_dados_txt(jogadores, partidas)

                print("Obrigado por jogar! Até mais.")
                break
            
            else:
                print("Opção inválida. Tente novamente.")
        
        # --- MENU 2: ESTADO "LOGADO" ---
        else:
            print(f"\n--- JOGO (Logado como: {usuario_logado}) ---")
            print("1. Jogar uma nova partida")
            print("2. Ver minhas estatísticas")
            print("3. Ver meu histórico de partidas")
            print("4. Ver rankings globais")
            print("5. Fazer logout (Voltar ao menu principal)")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                # --- JOGAR ---
                partida_info = jogar_partida(usuario_logado)
                print(f"Partida {partida_info['id']} registrada. Pontuação: {partida_info['pontuacao']}")

            elif opcao == '2':
                # --- ESTATÍSTICAS ---
                exibir_estatisticas_jogador(usuario_logado)

                #checa se o jogador tem partidas antes de tentar salvar o relatório
                estatisticas = calcular_estatisticas_jogador(usuario_logado)
                if estatisticas['total_partidas'] > 0:
                    salvar_relatorio_individual(usuario_logado)
                else:
                    print("Nenhuma partida enocntrada.")

            elif opcao == '3':
                # --- HISTÓRICO ---
                limite_historico = 5
                historico = historico_partidas(usuario_logado, limite_historico)
                print(f"\n--- {limite_historico} Últimas Partidas de {usuario_logado} ---")
                
                if not historico:
                    print("Nenhuma partida encontrada.")
                else:
                    for p in historico:
                        #formata a data pra ficar legal de ler
                        data_formatada = p['data'].strftime('%Y-%m-%d %H:%M')
                        print(f"  ID {p['id']} | {data_formatada} | {p['resultado']} | Tentativas: {p['total_tentativas']} | Pontos: {p['pontuacao']}")
                salvar_historico_individual(usuario_logado, historico, limite_historico)

            elif opcao == '4':
                # --- RANKING ---
                print("\n--- RANKINGS GLOBAIS ---")
                exibir_ranking()
                if partidas:
                    salvar_relatorio_rankings()
                else:
                    print("Nenhuma partida encontrada.")

            elif opcao == '5':
                # --- LOGOUT ---
                salvar_dados_txt(jogadores, partidas)
                print(f"Até logo, {usuario_logado}!")
                usuario_logado = None
            
            else:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    carregar_dados_txt()
    main()