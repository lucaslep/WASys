echo Iniciando ambiente virtual ...

call .venv\scripts\activate
if errorlevel 1 (
    echo Falha ao ativar o ambiente virtual
    exit /b 1
)

echo Buildando exe ...

pyinstaller wasys.spec
if errorlevel 1 (
    echo Falha ao executar o pyinstaller
    exit /b 1
)

echo WaSys.exe criado com sucesso!
