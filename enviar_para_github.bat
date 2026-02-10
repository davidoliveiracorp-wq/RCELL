@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ============================================
echo   Enviar para GitHub (RCELL) e Vercel
echo ============================================
echo.

REM Remove pasta .git antiga/corrompida para comecar do zero
if exist ".git" (
    echo Removendo pasta .git antiga para evitar erros de config...
    rd /s /q .git
    echo.
)

echo Inicializando Git...
git init
git branch -M main

echo.
echo Adicionando arquivos...
git add .

echo.
echo Arquivos que serao enviados:
git status --short
echo.

set /p conf="Enviar para o GitHub agora? (S/N): "
if /i not "%conf%"=="S" exit /b 0

git commit -m "Dashboard BI: uniao de planilhas + deploy Vercel"

echo.
echo Repositorio: davidoliveiracorp-wq/RCELL
git remote remove origin 2>nul
git remote add origin https://github.com/davidoliveiracorp-wq/RCELL.git

echo.
echo Enviando (push)...
echo Se pedir Username: davidoliveiracorp-wq
echo Se pedir Password: use um Personal Access Token (nao a senha da conta)
echo    Criar token: GitHub - Settings - Developer settings - Personal access tokens
echo.
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERRO no push. Confira:
    echo - Repositorio existe em: https://github.com/davidoliveiracorp-wq/RCELL
    echo - Password = Token com permissao "repo"
    pause
    exit /b 1
)

echo.
echo OK! Projeto no GitHub: https://github.com/davidoliveiracorp-wq/RCELL
echo.
echo Proximo passo - Vercel:
echo 1. Acesse https://vercel.com e faca login com GitHub
echo 2. Add New - Project - escolha RCELL - Deploy
echo 3. Use o link que o Vercel mostrar para acessar o dashboard online
echo.
pause
