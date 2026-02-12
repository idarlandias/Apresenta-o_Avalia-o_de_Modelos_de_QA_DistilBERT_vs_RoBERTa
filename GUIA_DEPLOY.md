# Como Colocar Seu Site no Ar (Nuvem) ☁️

Este guia passo a passo vai te ajudar a pegar o seu site (que agora está "dockerizado") e colocá-lo na internet para sua professora ver.

## Opção Recomendada: Render (Grátis e Fácil)

O Render conecta com seu GitHub e faz o deploy automático do Dockerfile que criamos.

### Passo 1: Preparar o GitHub
1. Crie uma conta no [GitHub.com](https://github.com) (se não tiver).
2. Crie um novo repositório (chamado `analise-modelos` por exemplo).
3. Faça o upload destes arquivos para lá:
   - `Dockerfile`
   - `analise_modelos_qa.html`
   - `.dockerignore`

### Passo 2: Configurar no Render
1. Acesse [render.com](https://render.com) e crie uma conta.
2. Clique no botão **"New +"** e escolha **"Web Service"**.
3. Conecte sua conta do GitHub e selecione o repositório que você criou.
4. Na tela de configuração:
   - **Name:** Dê um nome (ex: `analise-ia-seu-nome`).
   - **Runtime:** Escolha **Docker**.
   - **Region:** Pode deixar o padrão (Ohio ou Frankfurt).
   - **Instance Type:** Selecione **Free** ($0/month).
5. Clique em **"Create Web Service"**.

🚀 **Pronto!** O Render vai construir seu Docker e te dar uma URL (ex: `https://analise-ia-seu-nome.onrender.com`).
Esse é o link que você vai mandar para sua professora!

---

## Testar no Seu Computador (Localmente)

Antes de enviar, você pode garantir que está tudo funcionando:

1. Dê dois cliques no arquivo `testar_localmente.bat` que eu criei.
2. Ele vai abrir uma janela preta, construir o container e te avisar quando estiver pronto.
3. Abra seu navegador em `http://localhost:8080`.

Se aparecer o site, o Docker está funcionando perfeitamente!
