@echo off
echo [INFO] Verificando Docker...
docker --version
if %errorlevel% neq 0 (
    echo [ERRO] Docker nao encontrado ou nao esta rodando. Por favor, inicie o Docker Desktop.
    pause
    exit /b
)

echo [INFO] Construindo a imagem Docker...
docker build -t analise-modelos .

echo [INFO] Iniciando o container na porta 8080...
echo [INFO] Acesse http://localhost:8080 no seu navegador.
docker run -p 8080:80 analise-modelos
pause
