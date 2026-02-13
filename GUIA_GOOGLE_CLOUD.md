# Como Colocar no Google Cloud (Cloud Run) ☁️

Você escolheu a **Opção A** (Deploy contínuo via GitHub), que é a forma mais profissional e automatizada. O Google Cloud Run vai monitorar seu GitHub e atualizar o site sempre que você mudar o código.

**Pré-requisitos:**
- Ter o código já no GitHub (você já fez isso!).
- Ter uma conta no Google Cloud com faturamento ativado (cartão de crédito, mesmo que tenha nível grátis).

---

## Passo a Passo

1. **Acesse o Google Cloud Console:**
   - Entre em: [console.cloud.google.com/run](https://console.cloud.google.com/run)
   - Se for seu primeiro acesso, crie um "Novo Projeto" (dê o nome de `analise-ia`).

2. **Crie o Serviço:**
   - Clique no botão azul **"CRIAR SERVIÇO"** (Create Service) no topo.

3. **Configure a Origem (GitHub):**
   - Na primeira opção ("Deploy one revision from an existing container image"), **NÃO** selecione isso.
   - Marque a opção debaixo: **"Continuously deploy new revisions from a source repository"**.
   - Clique em **"SET UP WITH CLOUD BUILD"**.
   - Vai abrir uma janela lateral:
     - **Repository Provider:** Escolha **GitHub**.
     - **Repository:** Selecione o seu repositório (`seu-usuario/analise-modelos`).
     - **Branch:** Deixe `^master$` ou `^main$`.
     - **Build Type:** Escolha **Dockerfile** (o Google vai achar seu arquivo `Dockerfile` automaticamente).
     - Clique em **SAVE**.

4. **Configurações do Serviço:**
   - **Service name:** Pode deixar `analise-modelos` (padrão).
   - **Region:** Escolha `us-central1` (Iowa) ou `southamerica-east1` (São Paulo - pode ser um pouco mais caro, mas é mais rápido). Recomendação: `us-central1` (mais barato/grátis).
   - **Authentication:** ⚠️ **MUITO IMPORTANTE!** ⚠️
     - Marque a opção: **"Allow unauthenticated invocations"**.
     - Isso torna seu site **PÚBLICO** para sua professora acessar. Se não marcar isso, só você consegue ver.

5. **Finalizar:**
   - Clique na setinha "Container, Networking, Security" para abrir opções avançadas (opcional), mas geralmente o padrão serve.
   - A porta do container deve ser **80** (nosso Dockerfile usa 80). Verifique se está 80 (em "Container port").
   - Clique no botão **"CREATE"** no final da página.

## O que acontece agora?

1.  Você verá uma tela com etapas de "Build" e "Deploy".
2.  O Google vai baixar seu código do GitHub.
3.  Vai ler o `Dockerfile` e criar o container.
4.  Vai iniciar o serviço na nuvem do Google.

⏳ **Tempo de espera:** Cerca de 2 a 4 minutos.

Quando ficar tudo **verde**, aparecerá um link no topo da página:
👉 **`https://analise-modelos-xxxx-uc.a.run.app`**

Esse é o link oficial do Google para o seu trabalho!
