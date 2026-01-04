from main import AutomacaoTela, pyautogui
import time

if __name__ == "__main__":
    auto = AutomacaoTela()
    # ch_nfce = "23251202333096000135650010000000011023330961"

    chaves = [
        # '23251227794852000154650030000000141277948523',
        # '23251227794852000154650050000000241277948522',
        '23260127794852000154650020000000091277948522',
        '23260127794852000154650020000000101277948523',
        '23260127794852000154650020000000111277948520',
        '23260127794852000154650020000000121277948528',
        '23260127794852000154650020000000131277948525',
        '23260127794852000154650020000000141277948522',
        '23260127794852000154650020000000151277948520',
        '23260127794852000154650030000000251277948522',
        '23260127794852000154650030000000261277948520',
        '23260127794852000154650030000000271277948527',
        '23260127794852000154650030000000281277948524',
        '23260127794852000154650030000000291277948521',
        '23260127794852000154650030000000301277948522',
        '23260127794852000154650030000000311277948520',
        '23260127794852000154650040000000091277948525',
        '23260127794852000154650050000000061277948520',
        '23260127794852000154650050000000071277948527',
        '23260127794852000154650050000000081277948524',
        '23260127794852000154650050000000091277948521',
        '23260127794852000154650050000000101277948522',
        '23260127794852000154650050000000111277948520',
        '23260127794852000154650050000000121277948527',
        '23260127794852000154650050000000131277948524',
        '23260127794852000154650050000000141277948521',
        '23260127794852000154650050000000151277948529',
        '23260127794852000154650050000000161277948526',
        '23260127794852000154650050000000171277948523',
        '23260127794852000154650050000000181277948520',
        '23260127794852000154650050000000191277948528',
    ]

    def auto1(chave):

        ## PT 1

        # Buscar e clicar no botão de buscar da tela de lançamento de nfce no CMFlex já logado
        auto.funcao2_buscar_imagem_clicar(r"C:\Users\jadso\Documents\images\botao_buscar_cmflex_1.png")
        time.sleep(1)
        
        auto.funcao4_preencher_formulario([{'tipo': 'texto', 'referencia': 'Chave', 'offset_x': 400}])

        time.sleep(1)

        auto.enviar_teclas('ctrl+a')
        auto.enviar_teclas('backspace')
        pyautogui.typewrite(chave)
        
        

        # Buscar e clicar no botão de buscar da tela de lançamento de nfce no CMFlex já logado
        auto.funcao2_buscar_imagem_clicar(r"C:\Users\jadso\Documents\images\botao_buscar_cmflex_2.png")
        time.sleep(1.2)

        pyautogui.click(1237, 309)
        time.sleep(1)


        ## PT 2

        # verifica o status
        res = auto.funcao2_buscar_imagem_clicar(caminho_imagem=r"C:\Users\jadso\Documents\images\sit_documentocancelado.png",\
                                             timeout=1,\
                                               acao="nenhuma")
        if res:
            pass
        else:
            # verifica se o tipo de documento ta preenchido
            res1 = auto.funcao2_buscar_imagem_clicar(caminho_imagem=r"C:\Users\jadso\Documents\images\tipodocumentofiscal_nulo.png",\
                                                timeout=1,\
                                                acao="clique",\
                                                digitar="NFCE Pr")
            if res1 != False: 
                auto.enviar_teclas('tab')
                time.sleep(1)

            # Preenche um formulário completo
            campos = [
            # Ou usando imagens dos campos
                {'tipo': 'imagem', \
                'referencia': r'C:\Users\jadso\Documents\images\botao_statusnfce_cmflex.png', \
                'offset_y': 20 \
                }
            ]
            # Buscar e clicar no botão de buscar da tela de lançamento de nfce no CMFlex já logado
            auto.funcao4_preencher_formulario(campos)
                # alterar status pra cancelado

            pyautogui.leftClick(1324, 561)
            time.sleep(1)
            pyautogui.leftClick(1324, 561)
            time.sleep(1)

            pyautogui.scroll(-5000)
            time.sleep(1)

            campos = [

                # Ou usando imagens dos campos
                {'tipo': 'imagem', \
                'referencia': r'C:\Users\jadso\Documents\images\botao_salvar_1.png', \
                'offset_y': 5 \
                }
            ]
            # Buscar e clicar no botão de buscar da tela de lançamento de nfce no CMFlex já logado
            auto.funcao4_preencher_formulario(campos)

            pyautogui.scroll(5000)
            time.sleep(1)

    inc = 0
    for chave in chaves:
        print(f"{inc} / {len(chaves)}")
        auto1(chave)
        inc += 1


