# Mover projeto para GitHub e depois Vercel

Siga **exatamente** esta ordem no seu computador.

> **Se o Vercel mostrou "O repositório não contém arquivos"**  
> O repositório RCELL no GitHub está **vazio**. É obrigatório fazer **antes** a **Parte 1** (enviar os arquivos para o GitHub). Só depois a Parte 2 (Vercel) funciona.

---

## Parte 1: Enviar para o GitHub (obrigatório primeiro)

### 1. Abrir o terminal na pasta do projeto

- No **Explorador de Arquivos**, vá em `c:\DEV\RCELL`
- Na barra de endereço, digite `powershell` e pressione Enter  
  **ou**
- No Cursor/VS Code: Terminal → New Terminal (já na pasta do projeto)

### 2. Rodar os comandos (copie e cole cada bloco)

**Bloco 1 – Limpar e iniciar o Git**
```powershell
cd c:\DEV\RCELL
if (Test-Path .git) { Remove-Item -Recurse -Force .git }
git init
git branch -M main
```

**Bloco 2 – Adicionar arquivos e fazer commit**
```powershell
git add .
git commit -m "Dashboard BI: uniao de planilhas + deploy Vercel"
```

**Bloco 3 – Conectar ao repositório e enviar**
```powershell
git remote add origin https://github.com/davidoliveiracorp-wq/RCELL.git
git push -u origin main
```

(Se aparecer que o remote `origin` já existe, rode antes: `git remote remove origin` e depois repita o `git remote add` e o `git push`.)

### 3. Quando pedir login do GitHub

- **Username:** `davidoliveiracorp-wq`
- **Password:** use um **Personal Access Token** (não a senha da conta)

**Criar token:** GitHub → sua foto → **Settings** → **Developer settings** → **Personal access tokens** → **Generate new token (classic)** → marque **repo** → Generate → copie e use como senha.

### 4. Conferir

Abra no navegador: **https://github.com/davidoliveiracorp-wq/RCELL**  
Você **precisa ver** arquivos como: dashboard.html, vercel.json, README.md, app.py, etc.  
Se a página mostrar só "README" ou "não contém arquivos", o **push não deu certo** — repita o Bloco 3 (git push) e use o Token como senha.

---

## Parte 2: Publicar no Vercel (só depois do GitHub com arquivos)

1. Acesse **https://vercel.com** e faça login com **Continue with GitHub**.
2. Clique em **Add New…** → **Project**.
3. No campo **"Insira o URL de um repositório Git"** cole:  
   **https://github.com/davidoliveiracorp-wq/RCELL**  
   e clique em **Continuar**.
4. Em **Project Name** coloque: **dashboardge** (para ficar dashboardge.vercel.app).
5. Deixe **Framework Preset** = Other e **Root Directory** em branco.
6. Clique em **Deploy**.

Quando terminar, o link será: **https://dashboardge.vercel.app**

---

## Resumo

| Ordem | O quê |
|-------|--------|
| 1 | Rodar os 3 blocos de comandos no PowerShell (GitHub). |
| 2 | Conferir o repositório em github.com/davidoliveiracorp-wq/RCELL. |
| 3 | No Vercel: Add New → Project → RCELL → Project Name: dashboardge → Deploy. |
