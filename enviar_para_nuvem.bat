@echo off
echo [INFO] Configurando identidade Git (se necessario)...
git config user.email "aluno@projeto.com"
git config user.name "Aluno Projeto"

echo [INFO] Configurando Git para envio a nuvem...
set /p REPO_URL="Cole a URL do seu repositorio GitHub aqui (ex: https://github.com/usuario/repo.git): "

if "%REPO_URL%"=="" (
    echo [ERRO] Voce precisa colar a URL!
    pause
    exit /b
)

echo [INFO] Adicionando arquivos...
git add .
git commit -m "Commit inicial para deploy"

echo [INFO] Conectando ao GitHub...
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo [INFO] Enviando arquivos...
git push -u origin master

echo.
echo [SUCESSO] Se nao houve erros vermelhos acima, seus arquivos estao no GitHub!
echo Agora va ao Render.com e conecte seu repositorio.
pause
