@echo off
cd /d "%~dp0"
echo ============================================
echo   Dashboard BI - RCELL
echo ============================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo Criando ambiente virtual...
    py -m venv venv
    if errorlevel 1 (
        echo Tente: python -m venv venv
        pause
        exit /b 1
    )
)

call venv\Scripts\activate.bat

echo Instalando dependencias (se necessario)...
pip install -r requirements.txt -q

echo.
echo Iniciando o servidor do dashboard...
echo NAO FECHE ESTA JANELA enquanto quiser usar o dashboard.
echo.
echo Quando abrir o navegador, use: http://localhost:8501
echo Se der "Connection Refused", espere alguns segundos e atualize a pagina (F5).
echo.
streamlit run app.py --server.headless true

pause
