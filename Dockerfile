# Use uma imagem leve do Nginx para servir arquivos estáticos
FROM nginx:alpine

# Copia o arquivo HTML para o diretório padrão do Nginx
COPY analise_modelos_qa.html /usr/share/nginx/html/index.html

# Expõe a porta 80 para acesso web
EXPOSE 80
