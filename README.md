# Smooth Scroll & Hotkey Simulator (macOS)

Este projeto é um script Python para macOS que permite:
- Simular scroll suave usando atalhos personalizados
- Simular combinações de teclas comuns (Command+S, Esc, Option+3)
- Encerrar o script facilmente por atalho

## Funcionalidades

- **K**: Scroll suave para cima
- **L**: Scroll suave para baixo
- **,** ou **'**: Scroll suave para a esquerda
- **.** ou **:**: Scroll suave para a direita
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
- **,** ou **'**: Scroll suave para a esquerda
- **.** ou **:**: Scroll suave para a direita
- **P**: Simula Option+3 (Alt+3)
- **O**: Simula Command+S (⌘+S)
- **I**: Simula Esc
- **Q**: Encerra o script

> **Dica:**
> - Para scroll lateral, tanto as teclas de pontuação (vírgula, ponto) quanto as teclas de aspas simples e dois pontos funcionam como atalhos.
> - O script funciona melhor em aplicativos que aceitam eventos sintéticos do macOS.
> - Se não funcionar em algum app, tente em outro (TextEdit, Safari, etc).
> - Certifique-se de dar permissão de "Acessibilidade" ao Terminal em Preferências do Sistema > Segurança e Privacidade > Acessibilidade.

## Observações

- O script foi desenvolvido e testado para macOS. Não é garantido que funcione em Windows ou Linux.
- O scroll suave é feito simulando múltiplos pressionamentos de seta com easing (ease in/out).
- O projeto pode ser expandido para outros atalhos facilmente.

---

Feito com ❤️ para automação no macOS. 