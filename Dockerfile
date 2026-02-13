# Use uma imagem leve do Nginx
FROM nginx:alpine

# Copia a configuração customizada do Nginx (para usar a porta 8080)
COPY default.conf /etc/nginx/conf.d/default.conf

# Copia o arquivo HTML
COPY analise_modelos_qa.html /usr/share/nginx/html/index.html

# O Cloud Run espera a porta 8080 por padrão
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
