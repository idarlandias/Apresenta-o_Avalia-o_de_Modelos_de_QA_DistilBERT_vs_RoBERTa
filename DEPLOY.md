# Guia de Implantação (Deployment) 🚀

Este guia explica como testar sua aplicação localmente e como colocá-la na nuvem para compartilhar o link.

## 1. Testar Localmente (Opcional)

Se você tiver o Docker instalado no seu computador:

1. Abra o terminal nesta pasta.
2. Construa a imagem:
   ```bash
   docker build -t analise-modelos .
   ```
3. Rode o container:
   ```bash
   docker run -p 8080:80 analise-modelos
   ```
4. Acesse no navegador: `http://localhost:8080`

## 2. Publicar na Nuvem (Render.com) - Recomendado

O Render é uma opção gratuita e fácil que suporta Docker diretamente.

### Passo 1: Colocar no GitHub
1. Crie um repositório no GitHub (ex: `analise-modelos`).
2. Envie os arquivos `Dockerfile` e `analise_modelos_qa.html` para lá.

### Passo 2: Criar Serviço no Render
1. Crie uma conta em [render.com](https://render.com).
2. Clique em **"New +"** e selecione **"Web Service"**.
3. Conecte sua conta do GitHub e selecione o repositório que você criou.
4. Dê um nome para sua aplicação (ex: `minha-analise-ia`).
5. Em **Runtime**, escolha **Docker**.
6. Clique em **"Create Web Service"**.

O Render vai construir seu Dockerfile e te dar um link (ex: `https://minha-analise-ia.onrender.com`) que você pode enviar para sua professora!

✅ Vantagem: É gratuito e usa Docker como você pediu.

## Alternativa Simples (Sem Docker)

Se você tiver dificuldades com o Docker, você também pode usar o **Vercel** ou **Netlify**:
1. Apenas arraste a pasta com o arquivo HTML para o site do Netlify Drop.
2. Ele vai gerar um link instantâneo.
