# 🎮 Jogo de Adivinhação 🐍  

Este é um jogo de adivinhação de números em linha de comando, desenvolvido em **Python**.  
O objetivo é adivinhar um número secreto gerado aleatoriamente, acumular pontos e competir nos rankings.  

---

## 🎯 Regras do Jogo  

O funcionamento do jogo é simples, mas desafiador:  

- **Objetivo:** Adivinhar um número secreto gerado pelo computador.  
- **Intervalo:** O número secreto estará sempre entre **1 e 100**.  
- **Tentativas:** Você tem um máximo de **10 tentativas** por partida.  
- **Dicas:** A cada palpite errado, o jogo informará se o número secreto é **MAIOR** ou **MENOR** que o seu palpite.  

### 🧮 Pontuação  

- Você começa com **100 pontos de pontuação base**.  
- Cada tentativa utilizada (além da primeira) remove **10 pontos**.  

#### Exemplo:  
- Acertar na **1ª tentativa** = 100 pontos  
- Acertar na **2ª tentativa** = 90 pontos  
- Acertar na **10ª tentativa** = 10 pontos  

> 💀 Se você não acertar em 10 tentativas (derrota), sua pontuação para aquela partida será **0**.  

---

## 🚀 Instruções de Uso  

Siga estes passos para executar o jogo.  

### 1. Pré-requisitos  

- **Python 3.x instalado**.  
- O jogo utiliza apenas **bibliotecas padrão do Python** (`random`, `datetime`, `os`, `ast`), portanto, **nenhuma instalação de pacote adicional (via pip)** é necessária.  

### 2. Como Executar  

1. Abra seu **terminal ou prompt de comando**.  
2. Navegue até o diretório onde você salvou o arquivo `jogo_adivinhacao.py`.  
3. Execute o arquivo Python:  

```bash
python jogo_adivinhacao.py
```  

---

## 🎮 Como Jogar  

O jogo é controlado por **menus de texto**.  

### 🏠 Menu Principal (Deslogado)  

Ao iniciar o jogo, você verá estas opções:  

- **Cadastrar novo jogador:**  
  Você precisará fornecer um nome completo e um nome de usuário (único).  

- **Fazer login:**  
  Informe seu nome de usuário para acessar o menu do jogador.  

- **Sair do Jogo:**  
  Encerra o programa e salva todos os dados.  

---

### 👤 Menu do Jogador (Logado)  

Após fazer login, você terá acesso às seguintes opções:  

- **Jogar uma nova partida:**  
  Inicia uma nova rodada do jogo.  

- **Ver minhas estatísticas:**  
  Exibe seu relatório de desempenho completo.  

- **Ver meu histórico de partidas:**  
  Mostra suas últimas 5 partidas jogadas.  

- **Ver rankings globais:**  
  Exibe os 10 melhores jogadores em diferentes categorias.  

- **Fazer logout:**  
  Salva seus dados e retorna ao menu principal.  
