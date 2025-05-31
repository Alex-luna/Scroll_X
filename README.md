# Smooth Scroll & Screen Recorder

Este script permite:
- Scroll suave com teclas customizadas
- Simulação de atalhos (Alt+3, Cmd+S, Esc)
- Gravação de vídeo da tela por 3 segundos ao pressionar a tecla **G** (com sinal sonoro no início e fim)

## Instalação de dependências

```bash
pip install -r requirements.txt
```

## Dependências
- pynput
- Quartz (macOS)
- mss
- opencv-python
- numpy

## Como usar
- Pressione **G** para gravar 3 segundos da tela. O vídeo será salvo no diretório configurado na variável `VIDEO_OUTPUT_DIR` com o nome `Vid_dd_MM_YY-HH_mm.mp4`.
- Sinais sonoros são emitidos no início e fim da gravação.

Edite o caminho em `VIDEO_OUTPUT_DIR` no código para escolher onde salvar os vídeos.

## Funcionalidades

- **K**: Scroll suave para cima
- **L**: Scroll suave para baixo
- **,**, **'**, ou **;**: Scroll suave para a esquerda
- **.**, **:**, ou **\"**: Scroll suave para a direita
- **P**: Simula Option+3 (Alt+3)
- **O**: Simula Command+S (⌘+S)
- **I**: Simula Esc
- **Q**: Encerra o script

## Requisitos

- Python 3.10+
- macOS
- Permissão de "Acessibilidade" para o Terminal ou app que executa o script

## Instalação

1. Clone o repositório ou copie os arquivos para uma pasta.
2. Instale as dependências:

```bash
pip install pynput
```

> O módulo `Quartz` já está disponível no macOS via `pyobjc` (instalado por padrão em muitas instalações Python do macOS). Se necessário, instale com:
>
> ```bash
> pip install pyobjc-framework-Quartz
> ```

## Uso

Execute o script principal:

```bash
python smooth_scroll_alt3.py
```

No terminal, use as teclas:

- **K**: Scroll suave para cima
- **L**: Scroll suave para baixo
- **,**, **'**, ou **;**: Scroll suave para a esquerda
- **.**, **:**, ou **\"**: Scroll suave para a direita
- **P**: Simula Option+3 (Alt+3)
- **O**: Simula Command+S (⌘+S)
- **I**: Simula Esc
- **Q**: Encerra o script

> **Dica:**
> - Para scroll lateral, tanto as teclas de pontuação (vírgula, ponto), aspas simples, ponto e vírgula e aspas duplas funcionam como atalhos.
> - O script funciona melhor em aplicativos que aceitam eventos sintéticos do macOS.
> - Se não funcionar em algum app, tente em outro (TextEdit, Safari, etc).
> - Certifique-se de dar permissão de "Acessibilidade" ao Terminal em Preferências do Sistema > Segurança e Privacidade > Acessibilidade.

## Observações

- O script foi desenvolvido e testado para macOS. Não é garantido que funcione em Windows ou Linux.
- O scroll suave é feito simulando múltiplos pressionamentos de seta com easing (ease in/out).
- O projeto pode ser expandido para outros atalhos facilmente.

## Alias para rodar de qualquer lugar

Você pode criar um alias no seu `~/.zshrc` ou `~/.bashrc` para rodar o script de qualquer lugar do terminal:

```bash
alias scrollx='cd /caminho/para/sscroll_x && source .venv/bin/activate && python smooth_scroll_alt3.py && deactivate && cd -'
```

```
echo "alias sscroll='source /Users/alexluna/Documents/Luna-Labs-Cursor/sscroll_x/.venv/bin/activate && python /Users/alexluna/Documents/Luna-Labs-Cursor/sscroll_x/smooth_scroll_alt3.py; deactivate'" >> ~/.zshrc
source ~/.zshrc
```

Troque `/caminho/para/sscroll_x` pelo caminho real da sua pasta.

Assim, basta digitar `scrollx` no terminal para rodar o script com o ambiente virtual ativado. Quando o script terminar, a venv será fechada automaticamente e você voltará para o diretório anterior.

Se preferir, pode criar um script shell executável com esse conteúdo e colocá-lo em um diretório do seu PATH.

**Dica:**
- Se quiser rodar sem ativar a venv, basta remover o `source .venv/bin/activate` e o `deactivate` do alias.
- Para garantir que a venv feche ao encerrar o script, mantenha o `deactivate` após o comando python.

---

Feito com ❤️ para automação no macOS. 