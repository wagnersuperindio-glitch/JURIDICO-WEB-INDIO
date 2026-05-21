# DEPLOY — ÍNDIO JURÍDICO PRIME WEB

## Passos para publicar em 10 minutos

### 1. Criar repositório no GitHub

1. Acesse: https://github.com/new
2. Nome do repo: `JURIDICO-WEB-INDIO`
3. Visibilidade: **Private** (IMPORTANTE — conteúdo confidencial)
4. Clique em "Create repository"

### 2. Configurar chave API no secrets.toml

Editar o arquivo `.streamlit/secrets.toml`:
```toml
ANTHROPIC_API_KEY = "sk-ant-SUA_CHAVE_REAL_AQUI"
```

> ⚠️ NUNCA commitar o secrets.toml com a chave real no GitHub!
> O arquivo já está no .gitignore. No Streamlit Cloud, configurar via painel.

### 3. Push para o GitHub

```powershell
cd "C:\Users\Administrador\Desktop\CLAUDE COWORK PROJETOS\JURIDICO WEB INDIO"
git init
git add app.py requirements.txt
git commit -m "Índio Jurídico Prime Web v1.0"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/JURIDICO-WEB-INDIO.git
git push -u origin main
```

> Nota: NÃO inclua `.streamlit/secrets.toml` no commit — contém a chave API.

### 4. Deploy no Streamlit Cloud

1. Acesse: https://share.streamlit.io
2. Clique em **"New app"**
3. Preencha:
   - Repository: `SEU_USUARIO/JURIDICO-WEB-INDIO`
   - Branch: `main`
   - Main file: `app.py`
4. Clique em **"Advanced settings"** → Secrets
5. Cole o conteúdo do `secrets.toml`:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-SUA_CHAVE_REAL_AQUI"
   ```
6. Clique em **"Deploy!"**

### 5. URL pública gerada

Após deploy (2-3 min), você receberá uma URL como:
```
https://juridico-web-indio-XXXXX.streamlit.app
```

Compartilhe essa URL com:
- Carolina Antonelli
- David Antonelli  
- Dra. Roberta (advogada)
- Cristina (contabilidade)
- Nicolás

### Senhas de acesso

| Usuário | Senha |
|---|---|
| wagner | Ind!o@W2026 |
| carolina | Ind!o@C2026 |
| david | Ind!o@D2026 |
| roberta | Ind!o@R2026 |
| cristina | Ind!o@Cris26 |
| nicolas | Ind!o@N2026 |

### Manutenção

Para atualizar o app:
```powershell
git add app.py
git commit -m "Atualização"
git push
```
O Streamlit Cloud atualiza automaticamente após o push.

Para trocar a chave API: acessar https://share.streamlit.io → seu app → Settings → Secrets.
