import pyautogui
import pytesseract
from PIL import Image
import time
import os

# Configuração automática do Tesseract para Windows
import platform
if platform.system() == 'Windows':
    # Tenta localizar o Tesseract automaticamente
    caminhos_possiveis = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        r'C:\Tesseract-OCR\tesseract.exe',
    ]
    for caminho in caminhos_possiveis:
        if os.path.exists(caminho):
            pytesseract.pytesseract.tesseract_cmd = caminho
            break

class AutomacaoTela:
    def __init__(self):
        # Configura fail-safe (mover mouse para canto superior esquerdo para parar)
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
    
    def funcao1_buscar_texto_ocr(self, texto_buscar, acao='clique', offset_x=0, offset_y=0, digitar=None):
        """
        Função 1: Busca texto usando OCR e executa ação com offset opcional
        
        Args:
            texto_buscar: Texto a ser localizado na tela
            acao: Tipo de ação - 'clique', 'duplo_clique', 'hover', 'nenhuma'
            offset_x: Deslocamento horizontal em pixels a partir do texto encontrado
            offset_y: Deslocamento vertical em pixels a partir do texto encontrado
            digitar: Texto a digitar após o clique (None = não digita)
        
        Returns:
            dict: {'sucesso': bool, 'posicao': (x, y)} ou False
        """
        try:
            # Verifica se o Tesseract está instalado
            try:
                pytesseract.get_tesseract_version()
            except pytesseract.TesseractNotFoundError:
                print("\n❌ ERRO: Tesseract OCR não está instalado!")
                print("\n📥 Para instalar o Tesseract:")
                print("1. Baixe: https://github.com/UB-Mannheim/tesseract/wiki")
                print("2. Instale e marque o idioma Português")
                print("3. Reinicie o terminal e tente novamente")
                return False
            
            print(f"🔍 Procurando por '{texto_buscar}' na tela...")
            if offset_x != 0 or offset_y != 0:
                print(f"   Offset: X={offset_x:+d}, Y={offset_y:+d}")
            
            # Captura a tela atual
            screenshot = pyautogui.screenshot()
            
            # Obtém dados detalhados do OCR com posições
            dados_ocr = pytesseract.image_to_data(screenshot, lang='por', output_type=pytesseract.Output.DICT)
            
            # Procura a posição do texto
            for i, palavra in enumerate(dados_ocr['text']):
                if texto_buscar.lower() in palavra.lower():
                    # Calcula posição central do texto
                    x_texto = dados_ocr['left'][i] + dados_ocr['width'][i] // 2
                    y_texto = dados_ocr['top'][i] + dados_ocr['height'][i] // 2
                    
                    # Aplica offset
                    x_final = x_texto + offset_x
                    y_final = y_texto + offset_y
                    
                    print(f"✅ Texto encontrado em: X={x_texto}, Y={y_texto}")
                    print(f"🎯 Posição final (com offset): X={x_final}, Y={y_final}")
                    
                    # Executa a ação
                    if acao == 'clique':
                        pyautogui.click(x_final, y_final)
                    elif acao == 'duplo_clique':
                        pyautogui.doubleClick(x_final, y_final)
                    elif acao == 'hover':
                        pyautogui.moveTo(x_final, y_final)
                    elif acao == 'nenhuma':
                        pyautogui.moveTo(x_final, y_final, duration=0.3)
                    
                    # Digita texto se fornecido
                    if digitar is not None:
                        time.sleep(0.3)
                        pyautogui.write(digitar, interval=0.05)
                        print(f"⌨️  Digitado: '{digitar}'")
                    
                    return {'sucesso': True, 'posicao': (x_final, y_final)}
            
            print(f"❌ Texto '{texto_buscar}' não encontrado na tela.")
            return False
                
        except Exception as e:
            print(f"❌ Erro na função 1: {e}")
            return False
    
    def funcao2_buscar_imagem_clicar(self, caminho_imagem, confianca=0.8, timeout=10, 
                                      offset_x=0, offset_y=0, acao='clique', digitar=None):
        """
        Função 2: Busca imagem e executa ação com offset opcional
        
        Args:
            caminho_imagem: Caminho para a imagem a ser buscada
            confianca: Nível de confiança da busca (0 a 1) - requer OpenCV
            timeout: Tempo máximo de busca em segundos
            offset_x: Deslocamento horizontal em pixels a partir da imagem
            offset_y: Deslocamento vertical em pixels a partir da imagem
            acao: Tipo de ação - 'clique', 'duplo_clique', 'hover', 'nenhuma'
            digitar: Texto a digitar após o clique (None = não digita)
        
        Returns:
            dict: {'sucesso': bool, 'posicao': (x, y)} ou False
        """
        try:
            if not os.path.exists(caminho_imagem):
                print(f"❌ Erro: Arquivo '{caminho_imagem}' não encontrado!")
                return False
            
            print(f"🔍 Procurando imagem: {os.path.basename(caminho_imagem)}")
            if offset_x != 0 or offset_y != 0:
                print(f"   Offset: X={offset_x:+d}, Y={offset_y:+d}")
            print(f"⏱️  Aguardando até {timeout} segundos...")
            
            # Verifica se OpenCV está disponível para usar confidence
            usar_confidence = False
            try:
                import cv2
                usar_confidence = True
            except ImportError:
                if confianca != 0.8:
                    print("⚠️  OpenCV não instalado. Buscando por correspondência exata.")
            
            tempo_inicial = time.time()
            
            while time.time() - tempo_inicial < timeout:
                try:
                    # Localiza a imagem na tela
                    if usar_confidence:
                        posicao = pyautogui.locateOnScreen(caminho_imagem, confidence=confianca)
                    else:
                        posicao = pyautogui.locateOnScreen(caminho_imagem)
                    
                    if posicao:
                        # Obtém o centro da imagem encontrada
                        x_imagem, y_imagem = pyautogui.center(posicao)
                        
                        # Aplica offset
                        x_final = x_imagem + offset_x
                        y_final = y_imagem + offset_y
                        
                        print(f"✅ Imagem encontrada em: X={x_imagem}, Y={y_imagem}")
                        print(f"🎯 Posição final (com offset): X={x_final}, Y={y_final}")
                        
                        # Move o mouse para a posição
                        pyautogui.moveTo(x_final, y_final, duration=0.3)
                        
                        # Executa a ação
                        if acao == 'clique':
                            pyautogui.click()
                        elif acao == 'duplo_clique':
                            pyautogui.doubleClick()
                        elif acao == 'clique_direito':
                            pyautogui.rightClick()
                        elif acao == 'hover':
                            pass  # Já moveu o mouse
                        elif acao == 'nenhuma':
                            pass
                        
                        # Digita texto se fornecido
                        if digitar is not None:
                            time.sleep(0.3)
                            pyautogui.write(digitar, interval=0.05)
                            print(f"⌨️  Digitado: '{digitar}'")
                        
                        return {'sucesso': True, 'posicao': (x_final, y_final)}
                        
                except pyautogui.ImageNotFoundException:
                    time.sleep(0.5)
                    continue
            
            print(f"❌ Imagem não encontrada após {timeout} segundos.")
            return False
            
        except Exception as e:
            print(f"❌ Erro na função 2: {e}")
            return False
    
    def funcao3_clique_loop_posicao(self, intervalo=5, duracao=None):
        """
        Função 3: Captura posição do mouse e executa cliques em loop
        
        Args:
            intervalo: Intervalo entre cliques em segundos
            duracao: Duração total do loop em segundos (None = infinito)
        """
        try:
            print("\n" + "="*50)
            print("🎯 CAPTURA DE POSIÇÃO DO MOUSE")
            print("="*50)
            print("📍 Posicione o mouse no local desejado e pressione ENTER...")
            input()
            
            # Captura a posição atual do mouse
            x, y = pyautogui.position()
            print(f"✅ Posição capturada: X={x}, Y={y}")
            
            print(f"\n🔄 Iniciando cliques a cada {intervalo} segundos...")
            print("⛔ Para parar: mova o mouse para o canto superior esquerdo (FAILSAFE)")
            print("   ou pressione Ctrl+C\n")
            
            tempo_inicial = time.time()
            contador = 0
            
            while True:
                # Verifica se deve parar por tempo
                if duracao and (time.time() - tempo_inicial) >= duracao:
                    print(f"\n✅ Loop finalizado após {duracao} segundos.")
                    break
                
                # Executa o clique
                pyautogui.click(x, y)
                contador += 1
                tempo_decorrido = int(time.time() - tempo_inicial)
                print(f"🖱️  Clique #{contador} executado | Tempo: {tempo_decorrido}s")
                
                # Aguarda o intervalo
                time.sleep(intervalo)
                
        except KeyboardInterrupt:
            print("\n\n⛔ Loop interrompido pelo usuário (Ctrl+C)")
        except pyautogui.FailSafeException:
            print("\n\n⛔ Loop interrompido (FAILSAFE ativado)")
        except Exception as e:
            print(f"❌ Erro na função 3: {e}")
    
    def enviar_teclas(self, teclas, intervalo=0.1):
        """
        Envia comandos de teclado (atalhos, teclas especiais, etc)
        
        Args:
            teclas: String ou lista de teclas a pressionar
                   - String simples: 'a', 'enter', 'esc'
                   - Atalhos: 'ctrl+a', 'ctrl+c', 'alt+f4'
                   - Lista: ['ctrl', 'a'] para pressionar simultaneamente
                   - Sequência: [['ctrl', 'a'], 'delete'] para múltiplas ações
            intervalo: Tempo de espera entre teclas (segundos)
        
        Exemplos:
            enviar_teclas('enter')                    # Pressiona Enter
            enviar_teclas('ctrl+a')                   # Ctrl+A (selecionar tudo)
            enviar_teclas(['ctrl', 'shift', 's'])     # Ctrl+Shift+S
            enviar_teclas([['ctrl', 'a'], 'delete'])  # Seleciona tudo e deleta
        """
        try:
            # Se for uma string com '+', divide em atalho
            if isinstance(teclas, str) and '+' in teclas:
                partes = teclas.split('+')
                print(f"⌨️  Enviando atalho: {teclas.upper()}")
                pyautogui.hotkey(*partes)
                time.sleep(intervalo)
                
            # Se for uma string simples
            elif isinstance(teclas, str):
                print(f"⌨️  Pressionando: {teclas.upper()}")
                pyautogui.press(teclas)
                time.sleep(intervalo)
                
            # Se for uma lista de teclas para pressionar juntas
            elif isinstance(teclas, list) and all(isinstance(t, str) for t in teclas):
                print(f"⌨️  Pressionando simultaneamente: {'+'.join(teclas).upper()}")
                pyautogui.hotkey(*teclas)
                time.sleep(intervalo)
                
            # Se for uma sequência de ações
            elif isinstance(teclas, list):
                print(f"⌨️  Executando sequência de {len(teclas)} ações...")
                for acao in teclas:
                    if isinstance(acao, list):
                        print(f"   → {'+'.join(acao).upper()}")
                        pyautogui.hotkey(*acao)
                    else:
                        print(f"   → {acao.upper()}")
                        pyautogui.press(acao)
                    time.sleep(intervalo)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar teclas: {e}")
            return False
    
    def funcao4_preencher_formulario(self, campos):
        """
        Função 4: Preenche múltiplos campos de formulário usando referências
        
        Args:
            campos: Lista de dicionários com configuração de cada campo
                   Cada dict pode ter:
                   - tipo: 'texto' ou 'imagem'
                   - referencia: texto OCR ou caminho da imagem
                   - offset_x, offset_y: deslocamento da referência
                   - valor: texto a digitar
                   - acao: tipo de clique (padrão: 'clique')
                   - aguardar: tempo de espera após preencher (padrão: 0.5s)
                   - limpar_antes: se True, limpa o campo antes (Ctrl+A + Delete)
                   - teclas_antes: teclas a pressionar antes de digitar
                   - teclas_depois: teclas a pressionar depois de digitar
        
        Exemplo:
            campos = [
                {
                    'tipo': 'texto',
                    'referencia': 'Nome:',
                    'offset_x': 100,
                    'offset_y': 0,
                    'valor': 'João Silva'
                },
                {
                    'tipo': 'imagem',
                    'referencia': 'campo_email.png',
                    'offset_x': 0,
                    'offset_y': 30,
                    'valor': 'joao@email.com'
                }
            ]
        """
        print("\n" + "="*50)
        print("📝 PREENCHIMENTO DE FORMULÁRIO")
        print("="*50)
        
        resultados = []
        
        for i, campo in enumerate(campos, 1):
            print(f"\n📌 Campo {i}/{len(campos)}: {campo.get('referencia', 'N/A')}")
            
            tipo = campo.get('tipo', 'texto')
            referencia = campo.get('referencia')
            offset_x = campo.get('offset_x', 0)
            offset_y = campo.get('offset_y', 0)
            valor = campo.get('valor', '')
            acao = campo.get('acao', 'clique')
            aguardar = campo.get('aguardar', 0.5)
            limpar_antes = campo.get('limpar_antes', False)
            teclas_antes = campo.get('teclas_antes', None)
            teclas_depois = campo.get('teclas_depois', None)
            
            resultado = False
            
            if tipo == 'texto':
                resultado = self.funcao1_buscar_texto_ocr(
                    referencia, 
                    acao=acao,
                    offset_x=offset_x, 
                    offset_y=offset_y,
                    digitar=None  # Vai digitar depois
                )
            elif tipo == 'imagem':
                resultado = self.funcao2_buscar_imagem_clicar(
                    referencia,
                    offset_x=offset_x,
                    offset_y=offset_y,
                    acao=acao,
                    digitar=None  # Vai digitar depois
                )
            
            # Se encontrou o campo, processa teclas e digitação
            if resultado:
                time.sleep(0.3)
                
                # Limpa o campo se solicitado
                if limpar_antes:
                    self.enviar_teclas('ctrl+a')
                    self.enviar_teclas('delete')
                
                # Pressiona teclas antes se houver
                if teclas_antes:
                    self.enviar_teclas(teclas_antes)
                
                # Digita o valor
                if valor:
                    pyautogui.write(valor, interval=0.05)
                    print(f"⌨️  Digitado: '{valor}'")
                
                # Pressiona teclas depois se houver
                if teclas_depois:
                    self.enviar_teclas(teclas_depois)
                
                time.sleep(aguardar)
            else:
                print(f"⚠️  Falha ao processar campo {i}")
            
            resultados.append({
                'campo': i,
                'referencia': referencia,
                'sucesso': bool(resultado)
            })
        
        # Resumo
        print("\n" + "="*50)
        print("📊 RESUMO DO PREENCHIMENTO")
        print("="*50)
        sucesso_total = sum(1 for r in resultados if r['sucesso'])
        print(f"✅ Campos preenchidos: {sucesso_total}/{len(campos)}")
        
        for r in resultados:
            status = "✅" if r['sucesso'] else "❌"
            print(f"{status} Campo {r['campo']}: {r['referencia']}")
        
        return resultados


# Exemplo de uso
if __name__ == "__main__":
    auto = AutomacaoTela()
    
    print("="*50)
    print("🤖 SCRIPT DE AUTOMAÇÃO AVANÇADO")
    print("="*50)
    print("\nEscolha uma função:")
    print("1 - Buscar texto com OCR (com offset)")
    print("2 - Buscar imagem (com offset)")
    print("3 - Capturar posição e clicar em loop")
    print("4 - Preencher formulário automaticamente")
    print("5 - Exemplo avançado de formulário")
    print("6 - Testar comandos de teclado")
    
    escolha = input("\n▶️  Digite o número da função (1-6): ")
    
    if escolha == "1":
        # Função 1: OCR com offset
        texto = input("Digite o texto a buscar: ")
        offset_x = input("Offset X em pixels (padrão 0): ")
        offset_y = input("Offset Y em pixels (padrão 0): ")
        digitar = input("Texto a digitar (ENTER para pular): ")
        
        offset_x = int(offset_x) if offset_x else 0
        offset_y = int(offset_y) if offset_y else 0
        digitar = digitar if digitar else None
        
        auto.funcao1_buscar_texto_ocr(
            texto, 
            acao='clique',
            offset_x=offset_x, 
            offset_y=offset_y,
            digitar=digitar
        )
        
    elif escolha == "2":
        # Função 2: Buscar imagem com offset
        caminho = input("Caminho da imagem: ")
        offset_x = input("Offset X em pixels (padrão 0): ")
        offset_y = input("Offset Y em pixels (padrão 0): ")
        digitar = input("Texto a digitar (ENTER para pular): ")
        
        offset_x = int(offset_x) if offset_x else 0
        offset_y = int(offset_y) if offset_y else 0
        digitar = digitar if digitar else None
        
        auto.funcao2_buscar_imagem_clicar(
            caminho,
            offset_x=offset_x,
            offset_y=offset_y,
            digitar=digitar
        )
        
    elif escolha == "3":
        # Função 3: Loop de cliques
        intervalo = input("Intervalo entre cliques (padrão 5s): ")
        duracao = input("Duração total em segundos (ENTER para infinito): ")
        
        intervalo = float(intervalo) if intervalo else 5
        duracao = float(duracao) if duracao else None
        
        auto.funcao3_clique_loop_posicao(intervalo, duracao)
        
    elif escolha == "4":
        # Função 4: Formulário personalizado
        print("\n📝 Configure os campos do formulário")
        print("   (Digite 'fim' no campo referência para concluir)\n")
        
        campos = []
        while True:
            print(f"\n--- Campo {len(campos) + 1} ---")
            tipo = input("Tipo (texto/imagem): ").lower()
            if tipo == 'fim':
                break
                
            referencia = input("Referência (texto OCR ou caminho imagem): ")
            if referencia == 'fim':
                break
                
            offset_x = input("Offset X (padrão 0): ")
            offset_y = input("Offset Y (padrão 0): ")
            valor = input("Valor a digitar: ")
            
            campos.append({
                'tipo': tipo,
                'referencia': referencia,
                'offset_x': int(offset_x) if offset_x else 0,
                'offset_y': int(offset_y) if offset_y else 0,
                'valor': valor
            })
        
        if campos:
            auto.funcao4_preencher_formulario(campos)
        else:
            print("⚠️  Nenhum campo configurado!")
            
    elif escolha == "5":
        # Exemplo 5: Formulário pré-configurado
        print("\n📋 Executando exemplo de formulário...")
        print("   Este é um exemplo. Ajuste conforme sua necessidade.\n")
        
        campos_exemplo = [
            {
                'tipo': 'texto',
                'referencia': 'Nome',
                'offset_x': 150,
                'offset_y': 0,
                'valor': 'João Silva',
                'aguardar': 0.5
            },
            {
                'tipo': 'texto',
                'referencia': 'Email',
                'offset_x': 150,
                'offset_y': 0,
                'valor': 'joao@email.com',
                'aguardar': 0.5
            },
            {
                'tipo': 'texto',
                'referencia': 'Telefone',
                'offset_x': 150,
                'offset_y': 0,
                'valor': '11999999999',
                'aguardar': 0.5
            }
        ]
        
        auto.funcao4_preencher_formulario(campos_exemplo)
        
    elif escolha == "6":
        # Teste de comandos de teclado
        print("\n⌨️  TESTE DE COMANDOS DE TECLADO")
        print("="*50)
        print("\nExemplos de uso:")
        print("1. Atalhos simples: ctrl+a, ctrl+c, alt+f4")
        print("2. Teclas especiais: enter, esc, tab, backspace")
        print("3. Múltiplas teclas: ctrl+shift+s")
        print("4. Sequências: pressiona várias teclas em ordem")
        print("\nDigite 'sair' para voltar\n")
        
        while True:
            comando = input("Digite o comando (ou exemplos 1-5): ").strip().lower()
            
            if comando == 'sair':
                break
            elif comando == '1':
                print("\n📋 Exemplo 1: Selecionar tudo e copiar")
                auto.enviar_teclas('ctrl+a')
                time.sleep(0.5)
                auto.enviar_teclas('ctrl+c')
            elif comando == '2':
                print("\n🗑️  Exemplo 2: Selecionar tudo e deletar")
                auto.enviar_teclas('ctrl+a')
                time.sleep(0.3)
                auto.enviar_teclas('delete')
            elif comando == '3':
                print("\n💾 Exemplo 3: Salvar (Ctrl+S)")
                auto.enviar_teclas('ctrl+s')
            elif comando == '4':
                print("\n↹ Exemplo 4: Navegar com Tab")
                auto.enviar_teclas([['tab'], ['tab'], ['enter']])
            elif comando == '5':
                print("\n🔙 Exemplo 5: Desfazer várias vezes")
                auto.enviar_teclas([['ctrl', 'z'], ['ctrl', 'z'], ['ctrl', 'z']])
            else:
                auto.enviar_teclas(comando)
        
    else:
        print("❌ Opção inválida!")