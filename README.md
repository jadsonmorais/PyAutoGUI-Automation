# 🤖 PyAutoGUI Screen Automation

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com)

Uma ferramenta completa de automação de tela que combina reconhecimento de imagens, OCR (Optical Character Recognition) e automação de cliques para criar scripts de automação poderosos e flexíveis.

## 📋 Índice

- [Características](#-características)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Uso Rápido](#-uso-rápido)
- [Funcionalidades Detalhadas](#-funcionalidades-detalhadas)
- [Exemplos de Código](#-exemplos-de-código)
- [Configuração Avançada](#-configuração-avançada)
- [Solução de Problemas](#-solução-de-problemas)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

## ✨ Características

- 🔍 **OCR Inteligente**: Localiza e clica em texto na tela usando Tesseract
- 🖼️ **Reconhecimento de Imagens**: Busca e interage com elementos visuais
- 🎯 **Automação de Cliques**: Executa cliques automatizados em posições específicas
- 🛡️ **Fail-Safe Integrado**: Proteção contra loops infinitos
- 🌐 **Multiplataforma**: Compatível com Windows, Linux e macOS
- ⚙️ **Configuração Automática**: Detecta e configura dependências automaticamente

## 🔧 Pré-requisitos

### Python
- Python 3.7 ou superior

### Dependências Python
```bash
pip install pyautogui pillow pytesseract
```

### Tesseract OCR (para Função 1)

#### Windows
1. Baixe o instalador: [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
2. Execute o instalador
3. Durante a instalação, marque o idioma **Portuguese** (ou outros necessários)
4. O script detectará automaticamente o Tesseract nos caminhos padrão

#### Linux
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-por
```

#### macOS
```bash
brew install tesseract tesseract-lang
```

### OpenCV (Opcional - para busca de imagens com confiança)
```bash
pip install opencv-python
```

## 📦 Instalação

### Clone o repositório
```bash
git clone https://github.com/seu-usuario/pyautogui-automation.git
cd pyautogui-automation
```

### Crie um ambiente virtual (recomendado)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### Instale as dependências
```bash
pip install -r requirements.txt
```

## 🚀 Uso Rápido

### Modo Interativo
```bash
python main.py
```

O script apresentará um menu interativo com 3 opções:
1. Buscar texto com OCR e clicar
2. Buscar imagem e clicar
3. Capturar posição e clicar em loop

### Uso Programático
```python
from main import AutomacaoTela

auto = AutomacaoTela()

# Buscar texto e clicar
auto.funcao1_buscar_texto_ocr(None, "Botão Enviar")

# Buscar imagem e clicar
auto.funcao2_buscar_imagem_clicar("botao.png", confianca=0.8)

# Clique automático em loop
auto.funcao3_clique_loop_posicao(intervalo=5, duracao=60)
```

## 📚 Funcionalidades Detalhadas

### Função 1: Buscar Texto com OCR

Localiza texto específico na tela usando reconhecimento óptico de caracteres e executa ações.

**Parâmetros:**
- `caminho_print` (str, opcional): Caminho para imagem de referência
- `texto_buscar` (str): Texto a ser localizado na tela
- `acao` (str): Tipo de ação - `'clique'`, `'duplo_clique'`, `'hover'`

**Exemplo:**
```python
auto.funcao1_buscar_texto_ocr(None, "Login", acao='clique')
```

**Casos de Uso:**
- Automação de formulários web
- Navegação em interfaces desconhecidas
- Testes de UI baseados em texto

---

### Função 2: Buscar Imagem e Clicar

Localiza uma imagem específica na tela e clica nela.

**Parâmetros:**
- `caminho_imagem` (str): Caminho para a imagem a ser buscada
- `confianca` (float): Nível de confiança da busca (0.0 a 1.0) - requer OpenCV
- `timeout` (int): Tempo máximo de busca em segundos

**Exemplo:**
```python
auto.funcao2_buscar_imagem_clicar(
    "assets/botao_login.png", 
    confianca=0.85, 
    timeout=15
)
```

**Dicas:**
- Use capturas de tela de alta qualidade
- Capture apenas o elemento específico, não a tela inteira
- Mantenha a mesma resolução entre captura e execução
- Use confiança 0.7-0.9 para busca flexível (requer OpenCV)

**Casos de Uso:**
- Automação de jogos
- Testes de aplicações desktop
- Robôs de interface gráfica

---

### Função 3: Clique em Loop

Captura uma posição do mouse e executa cliques repetidos nessa posição.

**Parâmetros:**
- `intervalo` (float): Intervalo entre cliques em segundos
- `duracao` (float, opcional): Duração total do loop em segundos (None = infinito)

**Exemplo:**
```python
# Loop de 5 minutos com cliques a cada 3 segundos
auto.funcao3_clique_loop_posicao(intervalo=3, duracao=300)

# Loop infinito até Ctrl+C ou FAILSAFE
auto.funcao3_clique_loop_posicao(intervalo=5)
```

**Casos de Uso:**
- Farming em jogos
- Testes de estresse em aplicações
- Manutenção de sessões ativas

## 💻 Exemplos de Código

### Exemplo 1: Automação de Login
```python
from main import AutomacaoTela
import time

auto = AutomacaoTela()

# Busca e clica no campo de usuário
auto.funcao2_buscar_imagem_clicar("assets/campo_usuario.png")
time.sleep(1)

# Digita o usuário
pyautogui.write("meu_usuario", interval=0.1)

# Busca o botão de login por texto
auto.funcao1_buscar_texto_ocr(None, "Entrar", acao='clique')
```

### Exemplo 2: Monitoramento e Ação
```python
from main import AutomacaoTela
import time

auto = AutomacaoTela()

while True:
    # Verifica se aparece uma notificação
    if auto.funcao2_buscar_imagem_clicar("assets/notificacao.png", timeout=2):
        print("Notificação detectada!")
        # Executa ação
        auto.funcao1_buscar_texto_ocr(None, "Confirmar", acao='clique')
    
    time.sleep(5)  # Verifica a cada 5 segundos
```

### Exemplo 3: Script Complexo com Tratamento de Erros
```python
from main import AutomacaoTela
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

auto = AutomacaoTela()

def executar_tarefa():
    try:
        # Tenta encontrar botão por imagem
        if auto.funcao2_buscar_imagem_clicar("assets/botao.png", timeout=5):
            logger.info("Botão encontrado por imagem")
            return True
        
        # Fallback: tenta encontrar por texto
        if auto.funcao1_buscar_texto_ocr(None, "Confirmar"):
            logger.info("Botão encontrado por OCR")
            return True
            
        logger.warning("Botão não encontrado")
        return False
        
    except Exception as e:
        logger.error(f"Erro na execução: {e}")
        return False

# Executa a tarefa
sucesso = executar_tarefa()
```

## ⚙️ Configuração Avançada

### Ajustar Velocidade do Mouse
```python
auto = AutomacaoTela()
pyautogui.PAUSE = 1.0  # Pausa de 1 segundo entre ações
```

### Desabilitar Fail-Safe (não recomendado)
```python
pyautogui.FAILSAFE = False
```

### Configurar Tesseract Manualmente
```python
import pytesseract

# Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Caminho\Para\tesseract.exe'

# Linux/macOS geralmente não precisa
```

### Salvar Screenshots para Debug
```python
# Salvar captura da tela para análise
screenshot = pyautogui.screenshot()
screenshot.save('debug_screenshot.png')

# Testar OCR em arquivo
texto = pytesseract.image_to_string(Image.open('debug_screenshot.png'), lang='por')
print(texto)
```

## 🐛 Solução de Problemas

### Tesseract não encontrado

**Erro:** `tesseract is not installed or it's not in your PATH`

**Solução:**
1. Verifique se o Tesseract está instalado
2. Adicione o caminho ao PATH do sistema ou configure manualmente no script

### OpenCV não disponível

**Erro:** `The confidence keyword argument is only available if OpenCV is installed`

**Solução:**
- Instale OpenCV: `pip install opencv-python`
- Ou use busca sem confiança (o script se adapta automaticamente)

### Imagem não encontrada

**Problema:** A função 2 não encontra a imagem na tela

**Soluções:**
- Verifique se a resolução da tela é a mesma da captura
- Capture apenas o elemento específico
- Use confiança menor (0.7) se tiver OpenCV instalado
- Teste em modo debug salvando screenshots

### Loop não para

**Problema:** O loop de cliques não para

**Solução:**
- Mova o mouse rapidamente para o canto superior esquerdo (FAILSAFE)
- Ou pressione Ctrl+C no terminal

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Diretrizes
- Mantenha o código limpo e documentado
- Adicione testes quando aplicável
- Atualize a documentação conforme necessário
- Siga as convenções PEP 8

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ para automação de tarefas repetitivas

## 🙏 Agradecimentos

- [PyAutoGUI](https://pyautogui.readthedocs.io/) - Automação de GUI
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - Reconhecimento de texto
- [Pillow](https://python-pillow.org/) - Processamento de imagens
- [OpenCV](https://opencv.org/) - Visão computacional

---

**⚠️ Aviso Legal:** Esta ferramenta deve ser usada de forma ética e responsável. O autor não se responsabiliza pelo uso indevido desta ferramenta. Sempre respeite os termos de serviço das aplicações que você está automatizando.