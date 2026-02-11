# Dashboard BI - RCELL

Dashboard em formato BI que **une os dados das duas planilhas**

**Enviar para o GitHub (repositório RCELLe) e publicar no Vercel:** veja o guia passo a passo em **[DEPLOY.md](DEPLOY.md)**. ("A vencer até 28-02" e "Pagos até 10-02") e permite **upload de novas planilhas** para atualizar os dados.

---

## Opção 1: Dashboard no navegador (recomendado – sem servidor)

**Não precisa de Python nem de servidor.** Não dá erro de "Connection Refused".

1. Abra a pasta do projeto no Explorador de Arquivos: `c:\DEV\RCELL`
2. Dê **dois cliques** no arquivo **`dashboard.html`**
3. O dashboard abrirá no seu navegador (Chrome, Edge, etc.)
4. Clique em **"Escolher arquivo"** em cada caixa e selecione:
   - **Planilha A vencer** → o arquivo "A vencer até 28-02.xls" (ou outra que quiser)
   - **Planilha Pagos** → o arquivo "Pagos até 10-02.xls" (ou outra que quiser)
5. Clique em **"Unir dados e atualizar dashboard"**
6. Os KPIs, gráficos e tabela serão preenchidos. Use **"Baixar dados unificados (CSV)"** para exportar.

Para **atualizar os dados**, basta enviar novas planilhas e clicar de novo em "Unir dados e atualizar dashboard".

---

## Opção 2: Dashboard Streamlit (com servidor Python)

### O que o dashboard faz

- **União dos dados**: junta as duas planilhas em uma única base, com coluna **Origem** (A vencer / Pagos).
- **Upload para atualização**: na barra lateral você pode enviar novas planilhas para substituir os dados.
- **Resumo (KPIs)**, **gráficos**, **filtros**, **tabela** e **exportar em Excel**.

### 1. Ambiente Python

Certifique-se de ter Python 3.9+ instalado. No terminal:

```bash
cd c:\DEV\RCELL
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

(Se no seu sistema o comando for `python` em vez de `py`, use `python -m venv venv` e `python -m pip install -r requirements.txt`.)

### 2. Subir o dashboard

```bash
streamlit run app.py
```

O navegador abrirá em `http://localhost:8501`.

**Atalho no Windows:** dê dois cliques em `run_dashboard.bat` — ele cria o ambiente, instala dependências e inicia o servidor. **Mantenha a janela do terminal aberta** enquanto usar o dashboard.

### 3. Dados iniciais

- Se os arquivos **"A vencer até 28-02.xls"** e **"Pagos até 10-02.xls"** estiverem na pasta do projeto, eles serão carregados automaticamente.
- Para atualizar sem mexer nos arquivos originais: use os **uploads** na barra lateral. Os arquivos enviados são salvos em `data/` e passam a ser usados nas próximas cargas.

## Estrutura do projeto

```
RCELL/
├── dashboard.html         # Dashboard no navegador (sem servidor) – use este se der Connection Refused
├── app.py                 # Aplicação Streamlit (dashboard com servidor)
├── requirements.txt       # Dependências Python
├── run_dashboard.bat      # Atalho para iniciar o Streamlit no Windows
├── README.md
├── A vencer até 28-02.xls # Planilha 1 (opcional)
├── Pagos até 10-02.xls    # Planilha 2 (opcional)
├── data/                  # Planilhas enviadas por upload no Streamlit (opcional)
└── .streamlit/
    └── config.toml        # Tema do Streamlit
```

## Erro "Connection Refused" (Conexão recusada)

Esse erro aparece quando o **servidor do Streamlit não está rodando** ou a janela do terminal foi fechada.

1. **Inicie o servidor:** no terminal (ou com `run_dashboard.bat`), execute `streamlit run app.py` e **deixe essa janela aberta**.
2. **Abra no navegador:** use o endereço que aparecer no terminal, em geral `http://localhost:8501`.
3. **Não use um link antigo:** se você fechou o terminal antes, o link que você salvou deixa de funcionar; inicie de novo com `streamlit run app.py` e abra o novo link.
4. **Se ainda falhar:** espere uns 5 segundos após subir o servidor e atualize a página (F5), ou abra manualmente `http://localhost:8501`.

## Observações

- O app detecta automaticamente uma coluna que parece **valor monetário** e colunas de **data** para métricas e gráficos.
- Formatos suportados: **.xls** e **.xlsx**.
- Os nomes das colunas das duas planilhas não precisam ser idênticos; o merge é feito por concatenação, com a coluna **Origem** indicando de qual planilha veio cada linha.
