# Enviar para o GitHub e publicar no Vercel

Siga estes passos para colocar o projeto no repositório **RCELL** no GitHub e publicar no Vercel para acesso online.

---

## Passo 1: Enviar para o GitHub

### Opção A – Usar o script (recomendado)

1. Abra a pasta **`c:\DEV\RCELL`** no Explorador de Arquivos.
2. Dê **dois cliques** em **`enviar_para_github.bat`**.
3. O script vai:
   - Remover a pasta `.git` antiga (se existir), para evitar erros de “config” ou “not a git repository”.
   - Inicializar um novo repositório Git.
   - Adicionar todos os arquivos, fazer commit e configurar o remote **davidoliveiracorp-wq/RCELL**.
4. Quando perguntar **“Enviar para o GitHub agora? (S/N)”**, digite **S** e Enter.
5. Se abrir uma janela de **login do GitHub**:
   - **Username:** `davidoliveiracorp-wq`
   - **Password:** use um **Personal Access Token** (não a senha da sua conta).

**Criar um Token:** no GitHub → sua foto (canto superior direito) → **Settings** → **Developer settings** → **Personal access tokens** → **Generate new token** → marque **repo** → Generate. Copie o token e use como “senha” quando o Git pedir.

### Opção B – Comandos no PowerShell

Abra o **PowerShell** e execute, **um bloco por vez**:

```powershell
cd c:\DEV\RCELL
```

```powershell
if (Test-Path .git) { Remove-Item -Recurse -Force .git }
git init
git branch -M main
git add .
git status
```

```powershell
git commit -m "Dashboard BI: uniao de planilhas + deploy Vercel"
```

```powershell
git remote add origin https://github.com/davidoliveiracorp-wq/RCELL.git
git push -u origin main
```

(Se der erro de “remote origin already exists”, use antes: `git remote remove origin` e depois o `git remote add` de novo.)

Quando pedir **Username** e **Password**, use seu usuário e o **Personal Access Token** como senha.

---

## Passo 2: Publicar no Vercel (acesso online)

1. Acesse **[vercel.com](https://vercel.com)** e faça login (por exemplo com **Continue with GitHub**).
2. Clique em **“Add New…”** → **“Project”**.
3. Na lista, escolha o repositório **RCELL** (conta **davidoliveiracorp-wq**).
4. Deixe **Framework Preset** como **Other** (ou “No framework”).
5. **Root Directory** em branco.
6. Clique em **“Deploy”**.

Quando terminar, o Vercel mostra um link (ex.: **https://rcell-xxx.vercel.app**). Esse é o endereço do dashboard online.

---

## Resumo

| Etapa | O que fazer |
|-------|-------------|
| 1 | Rodar **`enviar_para_github.bat`** (ou os comandos do PowerShell acima). |
| 2 | Confirmar que o repositório **davidoliveiracorp-wq/RCELL** tem os arquivos no GitHub. |
| 3 | No Vercel: **Add New → Project → RCELL → Deploy**. |
| 4 | Usar o link gerado pelo Vercel para acessar o dashboard na web. |

O que fica online no Vercel é o **dashboard em HTML** (`dashboard.html`). O **app Streamlit** (`app.py`) fica só no repositório para uso local.
