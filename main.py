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
    
    def funcao1_buscar_texto_ocr(self, caminho_print, texto_buscar, acao='clique'):
        """
        Função 1: Busca texto em uma imagem usando OCR e executa ação
        
        Args:
            caminho_print: Caminho para a imagem de referência
            texto_buscar: Texto a ser encontrado via OCR
            acao: Tipo de ação ('clique', 'duplo_clique', 'hover')
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
            
            print(f"Procurando por '{texto_buscar}' na tela...")
            
            # Captura a tela atual
            screenshot = pyautogui.screenshot()
            
            # Realiza OCR na tela
            texto_tela = pytesseract.image_to_string(screenshot, lang='por')
            
            if texto_buscar.lower() in texto_tela.lower():
                print(f"Texto '{texto_buscar}' encontrado!")
                
                # Obtém dados detalhados do OCR com posições
                dados_ocr = pytesseract.image_to_data(screenshot, lang='por', output_type=pytesseract.Output.DICT)
                
                # Procura a posição do texto
                for i, palavra in enumerate(dados_ocr['text']):
                    if texto_buscar.lower() in palavra.lower():
                        x = dados_ocr['left'][i] + dados_ocr['width'][i] // 2
                        y = dados_ocr['top'][i] + dados_ocr['height'][i] // 2
                        
                        print(f"Posição encontrada: X={x}, Y={y}")
                        
                        # Executa a ação
                        if acao == 'clique':
                            pyautogui.click(x, y)
                        elif acao == 'duplo_clique':
                            pyautogui.doubleClick(x, y)
                        elif acao == 'hover':
                            pyautogui.moveTo(x, y)
                        
                        return True
                
            else:
                print(f"Texto '{texto_buscar}' não encontrado na tela.")
                return False
                
        except Exception as e:
            print(f"Erro na função 1: {e}")
            return False
    
    def funcao2_buscar_imagem_clicar(self, caminho_imagem, confianca=0.8, timeout=10):
        """
        Função 2: Busca uma imagem na tela e clica nela
        
        Args:
            caminho_imagem: Caminho para a imagem a ser buscada
            confianca: Nível de confiança da busca (0 a 1) - requer OpenCV
            timeout: Tempo máximo de busca em segundos
        """
        try:
            if not os.path.exists(caminho_imagem):
                print(f"Erro: Arquivo '{caminho_imagem}' não encontrado!")
                return False
            
            print(f"Procurando imagem: {caminho_imagem}")
            print(f"Aguardando até {timeout} segundos...")
            
            # Verifica se OpenCV está disponível para usar confidence
            usar_confidence = False
            try:
                import cv2
                usar_confidence = True
            except ImportError:
                if confianca != 0.8:
                    print("AVISO: OpenCV não instalado. Buscando por correspondência exata.")
                    print("Para usar confiança, instale: pip install opencv-python")
            
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
                        x, y = pyautogui.center(posicao)
                        print(f"Imagem encontrada na posição: X={x}, Y={y}")
                        
                        # Move o mouse e clica
                        pyautogui.moveTo(x, y, duration=0.5)
                        pyautogui.click()
                        print("Clique executado com sucesso!")
                        return True
                        
                except pyautogui.ImageNotFoundException:
                    time.sleep(0.5)
                    continue
            
            print(f"Imagem não encontrada após {timeout} segundos.")
            return False
            
        except Exception as e:
            print(f"Erro na função 2: {e}")
            return False
    
    def funcao3_clique_loop_posicao(self, intervalo=5, duracao=None):
        """
        Função 3: Captura posição do mouse e executa cliques em loop
        
        Args:
            intervalo: Intervalo entre cliques em segundos
            duracao: Duração total do loop em segundos (None = infinito)
        """
        try:
            print("\n=== CAPTURA DE POSIÇÃO DO MOUSE ===")
            print("Posicione o mouse no local desejado e pressione ENTER...")
            input()
            
            # Captura a posição atual do mouse
            x, y = pyautogui.position()
            print(f"Posição capturada: X={x}, Y={y}")
            
            print(f"\nIniciando cliques a cada {intervalo} segundos...")
            print("Para parar, mova o mouse para o canto superior esquerdo da tela (FAILSAFE)")
            
            tempo_inicial = time.time()
            contador = 0
            
            while True:
                # Verifica se deve parar por tempo
                if duracao and (time.time() - tempo_inicial) >= duracao:
                    print(f"\nLoop finalizado após {duracao} segundos.")
                    break
                
                # Executa o clique
                pyautogui.click(x, y)
                contador += 1
                print(f"Clique {contador} executado em X={x}, Y={y}")
                
                # Aguarda o intervalo
                time.sleep(intervalo)
                
        except KeyboardInterrupt:
            print("\n\nLoop interrompido pelo usuário (Ctrl+C)")
        except pyautogui.FailSafeException:
            print("\n\nLoop interrompido (FAILSAFE ativado)")
        except Exception as e:
            print(f"Erro na função 3: {e}")


# Exemplo de uso
if __name__ == "__main__":
    auto = AutomacaoTela()
    
    print("=== SCRIPT DE AUTOMAÇÃO COM PYAUTOGUI ===\n")
    print("Escolha uma função:")
    print("1 - Buscar texto com OCR e clicar")
    print("2 - Buscar imagem e clicar")
    print("3 - Capturar posição e clicar em loop")
    
    escolha = input("\nDigite o número da função (1/2/3): ")
    
    if escolha == "1":
        # Função 1: OCR
        caminho = input("Caminho da imagem de referência (opcional, ENTER para pular): ")
        texto = input("Digite o texto a buscar na tela: ")
        auto.funcao1_buscar_texto_ocr(caminho if caminho else None, texto)
        
    elif escolha == "2":
        # Função 2: Buscar imagem
        caminho = input("Caminho da imagem a buscar: ")
        confianca = input("Confiança (0-1, padrão 0.8): ")
        confianca = float(confianca) if confianca else 0.8
        auto.funcao2_buscar_imagem_clicar(caminho, confianca)
        
    elif escolha == "3":
        # Função 3: Loop de cliques
        intervalo = input("Intervalo entre cliques em segundos (padrão 5): ")
        intervalo = float(intervalo) if intervalo else 5
        duracao = input("Duração total em segundos (ENTER para infinito): ")
        duracao = float(duracao) if duracao else None
        auto.funcao3_clique_loop_posicao(intervalo, duracao)
        
    else:
        print("Opção inválida!")