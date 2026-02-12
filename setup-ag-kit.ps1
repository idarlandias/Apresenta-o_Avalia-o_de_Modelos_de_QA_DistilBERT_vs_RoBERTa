$ProfilePath = $PROFILE 
$ProfileDir = Split-Path $ProfilePath -Parent

# Cria o diretório do perfil se não existir
if (!(Test-Path $ProfileDir)) {
    New-Item -ItemType Directory -Path $ProfileDir -Force | Out-Null
}

# Cria o arquivo de perfil se não existir
if (!(Test-Path $ProfilePath)) {
    New-Item -ItemType File -Path $ProfilePath -Force | Out-Null
}

# A função que será adicionada
$FunctionCode = @"

function iniciar-projeto {
    param([string]`$ProjectName)

    if (-not `$ProjectName) {
        Write-Host "Por favor, forneça um nome para o projeto." -ForegroundColor Red
        return
    }

    Write-Host "Criando pasta '`$ProjectName'..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path `$ProjectName -Force | Out-Null
    Set-Location `$ProjectName

    Write-Host "Inicializando @vudovn/ag-kit..." -ForegroundColor Cyan
    # Executa o npx sem pedir confirmação (-y)
    cmd /c "npx -y @vudovn/ag-kit init"

    Write-Host "Abrindo VS Code..." -ForegroundColor Green
    code .
}
"@

# Adiciona ao perfil se ainda não existir
$CurrentContent = Get-Content $ProfilePath -Raw -ErrorAction SilentlyContinue
if ($CurrentContent -notmatch "function iniciar-projeto") {
    Add-Content -Path $ProfilePath -Value "`n$FunctionCode"
    Write-Host "Comando 'iniciar-projeto' instalado com sucesso!" -ForegroundColor Green
    Write-Host "Para usar agora, execute: . `$PROFILE" -ForegroundColor Yellow
} else {
    Write-Host "O comando 'iniciar-projeto' já existe no seu perfil." -ForegroundColor Yellow
}
