# 🤖 Jeff Bot - Um Bot Multifuncional para Discord

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![discord.py](https://img.shields.io/badge/discord.py-2.3.2-7289DA.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Jeff Bot** é um bot para Discord desenvolvido em Python com a biblioteca `discord.py`. Ele foi criado para adicionar diversão, interação e um sistema de engajamento baseado em perfis e pontos ao seu servidor.

## ✨ Funcionalidades

O bot vem com um conjunto de funcionalidades prontas para usar:

- **👋 Mensagens de Boas-Vindas:** Recebe novos membros com uma mensagem personalizada.
- **😂 Comandos de Diversão:** `!piada`, `!dominio`, `!hug @membro`.
- **❤️ Respostas a Reações:** O bot reage com mensagens contextuais a emojis específicos (🔥, 😂, ❤️).
- **🏆 Sistema de Perfis e Ranking:** `!criarperfil`, `!perfil`, `!rank`.
- **🛠️ Comandos de Administração:** `!addpontos` e `!rempontos` (apenas para admins).

## 🚀 Começando

Siga estas instruções para configurar e rodar o bot no seu próprio servidor de forma segura.

### Pré-requisitos

- [Python 3.8+](https://www.python.org/downloads/)
- Uma conta no Discord e um servidor onde você tenha permissão de administrador.

### Guia de Instalação

1.  **Clone o repositório:**
    ```sh
    git clone [https://github.com/walkerataide/codebot.git](https://github.com/walkerataide/codebot.git)
    cd codebot
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    Crie um arquivo `requirements.txt` com o seguinte conteúdo:
    ```txt
    discord.py
    python-dotenv
    ```
    Em seguida, instale-o:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Crie e configure seu Bot no Discord:**
    - Acesse o [Portal de Desenvolvedores do Discord](https://discord.com/developers/applications).
    - Crie uma "New Application" e na aba "Bot", clique em "Add Bot".
    - Na seção **Privileged Gateway Intents**, ative `SERVER MEMBERS INTENT` e `MESSAGE CONTENT INTENT`.
    - Na aba "Bot", clique em "Reset Token" para gerar seu token. **Copie-o e guarde-o em um local seguro.**

5.  **Configure as Variáveis de Ambiente (Passo de Segurança):**
    - Crie um arquivo chamado `.env` na raiz do projeto.
    - Dentro dele, adicione seu token da seguinte forma:
      ```
      DISCORD_TOKEN="SEU_TOKEN_AQUI"
      ```

6.  **Crie um arquivo `.gitignore`:**
    Para garantir que seu arquivo `.env` nunca seja enviado para o GitHub, crie um arquivo chamado `.gitignore` na raiz do projeto e adicione o seguinte conteúdo:
    ```
    # Arquivos de ambiente
    .env

    # Diretório do ambiente virtual
    venv/
    /venv/

    # Arquivos de cache do Python
    __pycache__/
    *.pyc
    ```

7.  **Personalize o Bot:**
    - No arquivo `mainjeff.py`, encontre a função `on_member_join` e altere a variável `canal_id` para o ID do seu canal de boas-vindas.

### Rodando o Bot

Com tudo configurado, inicie o bot com o comando:
```sh
python mainjeff.py