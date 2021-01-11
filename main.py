from tkinter import filedialog as dlg #Caixa de diálogo para escolher o arquivo
from tkinter import * #Tudo do tkinter
from PIL import Image, ImageTk #Para as imagens
import camelot #Para pegar os dados da tabela do arquivo
import numpy #Para manipular os dados que foram pegos com o camelot


#===========Configurações da Janela
#Criar janelas do Tk
window = Tk()

#Título da janela
window.title("Qual é o meu CR?")

#dimensoes da janela
largura = 700
altura = 400

#resolução do sistema
largura_screen = window.winfo_screenwidth()
altura_screen = window.winfo_screenheight()

#posicao da janela
posx = largura_screen / 2 - largura / 2
posy = altura_screen / 2 - altura / 2

#definir geometry
window.geometry("%dx%d+%d+%d" % (largura,altura,posx,posy))

#Não vai poder ser redimensionado
window.resizable(0,0)

#Configuraçõesdo grid
window.rowconfigure(0,weight = 1)
window.columnconfigure(0,weight = 1)

#Cor de fundo da janela
window.configure(bg="#06335a")

#Logo da janela
window.iconphoto(True, PhotoImage(file="img/logo-3.png"))

#====================Janelas modais de erro e aviso

#============Janela Modal de Erro
def popUpError(msg):
    
    top = Toplevel() #Janela modal

    larguraTop = 320
    alturaTop = 120

    largura_screen_top = window.winfo_screenwidth()
    altura_screen_top = window.winfo_screenheight()

    posx_top = largura_screen_top / 2 - larguraTop / 2
    posy_top = altura_screen_top / 2 - alturaTop / 2

    top.geometry("%dx%d+%d+%d" % (larguraTop,alturaTop,posx_top,posy_top))

    top.title("Error")

    top.resizable(0,0)

    #Para exibir o ícone de erro
    load = Image.open("img/erro_icon.png")
    render = ImageTk.PhotoImage(load)
    labelPhoto = Label(top,image = render)
    labelPhoto.image = render
    labelPhoto.grid(row = 0,column = 0,sticky = W,pady = 10,padx = 10)
    
    #conteúdo da janela
    labelTop = Label(top, text = f"\n{msg}\n", font = "Arial 11 bold")
    labelTop.grid(row = 0, column = 1,sticky = N,pady = 10,padx = 5)
    
    btnLabelTop = Button(top, text="OK",command = lambda: top.destroy())
    btnLabelTop.grid(row = 1, column = 1,sticky = S)

    #Para exibir sobre todas as janelas
    top.attributes('-topmost', True)
    
    #Atualizr janela
    top.update()

    #Fechar o programa com atalho de teclado
    top.bind("<Control_L><w>", lambda x: top.destroy())
   
 
#============Janela Modal de Atenção 
def popUpWarning(msg):
    
    top = Toplevel()
    
    larguraTop = 320
    alturaTop = 120

   
    largura_screen_top = window.winfo_screenwidth()
    altura_screen_top = window.winfo_screenheight()

   
    posx_top = largura_screen_top / 2 - larguraTop / 2
    posy_top = altura_screen_top / 2 - alturaTop / 2

    top.geometry("%dx%d+%d+%d" % (larguraTop,alturaTop,posx_top,posy_top))

    top.title("Warning")
    top.resizable(0,0)

    #Para exibir o ícone de atenção
    load = Image.open("img/warning_icon.png")
    render = ImageTk.PhotoImage(load)
    labelPhoto = Label(top,image = render)
    labelPhoto.image = render
    labelPhoto.grid(row = 0,column = 0,sticky = W,pady = 10,padx = 10)
    #conteúdo da janela
    labelTop = Label(top, text = f"\n{msg}\n", font = "Arial 11 bold")
    labelTop.grid(row = 0, column = 1,sticky = N,pady = 10,padx = 5)
    
    btnLabelTop = Button(top, text="OK",command = lambda: top.destroy())
    btnLabelTop.grid(row = 1, column = 1,sticky = S)

    #Para exibir sobre todas as janelas
    top.attributes('-topmost', True)
    #atualizr janela
    top.update()

    top.bind("<Control_L><w>", lambda x: top.destroy())
   
#================Funcionamento da Janela Principal

def show_frame(frame):#Exibir frame
    frame.tkraise()

def clearFrame(frame):#Limpar os widgets do Frame 
    for widget in frame.winfo_children():
        widget.destroy()


def openWindowFileDialog():#Abrir janela para escolher o arquivo
    
    global path
    
    #Deixar janela princiál invisível
    window.withdraw()

    try:
        #Abrir janela file dialog e com isso consigo pegar o caminho do arquivo             
        path = dlg.askopenfilename(title = "Selecione o arquivo do seu histórico", initialdir = "/", filetypes = (("pdf files","*.pdf"),("all files","*.*")))
       
        #Se a operação de pegar o caminhodo arquivo foi um sucesso, vá para a próxima janela
        if(path): 
            frameMenu1_1()
       
        #Deixa a janela principal visível
        window.deiconify()

        #Colocar janela principal em nível superior
        window.lift()
        
        #Colocar o foco na janela principal
        window.focus_force()
    except:
        popUpError("Erro ao executar a opção escolhida")
       
        
#==================Lógica do coeficiente de rendimento

#Encontrar a tabela e o local das notas no histórico
def setTable():
    global tables
    global indices

    #Lê o PDF e encontra tabelas
    tables = camelot.read_pdf(path, pages="1-end") 
    
    #Encontrar a tabela correta (que contém as notas) entre todas as tabelas de tables    
    indices = findRightTable(tables)

    #Se indice está vazio, esse arquivo PDF não é um histórico válido 
    if(len(indices) == 0):
        return False
    
    return True
        
#Encontrar a tabela correta
def findRightTable(tables):
  
  #Quantas tabelas o camelot encontrou
  tam = len(tables)

  k = 0

  #Variável para armazenar os índices da tabela que tem a string que eu quero
  indices = []

  #Loop para saber o índice da tabela que tem a string que eu quero
  while(k < tam):
    #Transforma a tabela em um array
    listaTables = (numpy.array(tables[k].df))

    #Loop para encontrar string no conteúdo da tabela
    for j in range(0,len(listaTables)):
      if listaTables[j][0] == "Ano/Período\nLetivo":
        indices.append(k)#Adiciona índice na variável indices

    k = k + 1
  
  return indices

#Calcular o CR que a pessoa tem atualmente
def currentCR(tables, indices):
 
  soma = 0.0
  numberSoma = 0

  #loop que funciona até o número de tabelas encontradas com a string requisitada no loop anterior
  for b in range(0,len(indices)):
    #Cria um vetor dos dados da tabela
    l = numpy.array(tables[b].df)
   
    #Até o tamanho do array que contém o conteúdo da tabela
    for a in range(1,len(l)):

      #Símbolo de quando não tem nota no campo média  
      if(l[a][8] != "--"):
        #É necessário fazer o replace da vírgula para o ponto, para fazer o cast
        soma = soma + float(l[a][8].replace(",","."))
        numberSoma = numberSoma + 1 #Encontrar o número total de médias que estão nas tabelas

  #Calcular CR
  CR = soma / numberSoma
  return CR

#Calcular o CR até um período determinado, se o período não existir é retornado o CR atual
def crPeriodoLimite(tables, indices, periodoLimite):
  soma = 0.0
  numberSoma = 0
  end = 0

  #loop que funciona até o número de tabelas encontradas com a string requisitada no loop anterior
  for b in range(0,len(indices)):
    l = numpy.array(tables[b].df)
    for a in range(1,len(l)):#Até o tamanho do array que contém o conteúdo da tabela
      if(l[a-1][0] == periodoLimite and l[a][0] != periodoLimite):
        end = 1
        break

      if(l[a][8] != "--"):#Símbolo de quando não tem nota no campo média
        soma = soma + float(l[a][8].replace(",","."))#É necessário fazer o replace da vírgula para o ponto, para fazer o cast
        numberSoma = numberSoma + 1 #Encontrar o número total de médias encontradas nas tabelas
    
    if(end == 1):
      break
  
  #Calcular CR
  CR = soma / numberSoma
  return CR

#Para encontrar qual seria o CR da pessoa se ela conseguisse uma nota X na matéria Y   
def crSimular(tables, indices, valorNumNotas, numNotas):
  soma = 0.0
  numberSoma = 0

  #loop que funciona até o número de tabelas encontradas com a string requisitada no loop anterior
  for b in range(0,len(indices)):
    l = numpy.array(tables[b].df)

    for a in range(1,len(l)):#Até o tamanho do array que contém o conteúdo da tabela
      if(l[a][8] != "--"):#Símbolo de quando não tem nota no campo média
        soma = soma + float(l[a][8].replace(",","."))#É necessário fazer o replace da vírgula para o ponto, para fazer o cast
        numberSoma = numberSoma + 1 #Encontrar o número total de médias encontradas nas tabelas

  #Adiciona em soma as notas digitadas pelo usuário
  for i in range(0,numNotas):
    soma = soma + valorNumNotas[i]
  
  #Adiciona em numberSoma a quantidade de notas digitadas pelo usuário
  numberSoma = numberSoma + numNotas
  
  #Calcular CR
  CR = soma / numberSoma
  return CR


#Validar entrada do usuário (Período digitado) 
def validateInputPeriodo(val):
    
    #Separa a string quando encontrar um ponto
    splitVal = val.split(".")
   
    #Se o tamanho da lista for 2
    if(len(splitVal) == 2):
        #O que está na primeira e segunda posição é um digito e tem tamanhos respectivamente 4 e 1
        if(splitVal[0].isdigit() and splitVal[1].isdigit()):
            if(len(splitVal[0]) == 4 and len(splitVal[1]) == 1):
                return True
            else:
                return False
        else:
            return False
        
    else:      
        return False

       
#Recebe o período digitado
def getPeriodo(inputPeriodo, getPeriodo_text):   
    try:
        #Pega o período e tudo que for vírgula será substituído por ponto 
        val = inputPeriodo.get().replace(",",".")

        #Se for um período válido       
        if(validateInputPeriodo(val)):
                #É o arquivo correto
                if(setTable()):
                    #Recebe ocoeficiente de rendimento
                    cr = crPeriodoLimite(tables, indices, val)
                    #Salva em getPeriodo_text para exibir ao usuário
                    getPeriodo_text.set(f"\nCR = {cr:.3f} \n\n")
                else:
                    popUpWarning("Arquivo não permitido") #Modal de Atenção
        else:
            popUpWarning("Período digitado incorreto")

    except:
        popUpError("Erro ao executar a opção escolhida") #Modal de erro
        
#Validar entrada de notas
def validateNotas(valNotas,numMaterias):
    
    validateNotas = []
    
    for i in range(0,numMaterias):
        #Adiciona valores na lista separando a entrada do usuário por ponto
        validateNotas.append(valNotas[i].split(".")) 
        
        #Pega um valor da lista
        number = validateNotas.pop()       
        
        #Se o tamanho do valor for maior que 2, só pode aceitar números entre 0 e 10
        if(len(number) > 2):
            return False
            
        
        for j in range(0,len(number)):
            #Se não for um número
            if(not number[j].isdigit()):               
                return False
            else:              
                if(len(number[0]) > 2):                   
                    return False
                
    return True        

#Converter uma lista de string para float
def floatList(valNotas):
    for i in range(0,len(valNotas)):
        val = float(valNotas[i])
        if(val > 10):
            return False
        else:        
            valNotas[i] = val

#Recebe as notas do usuário
def getSimulacaoCR(numMaterias,inputNotas,getSimulacaoCR_text,frameMenuSimulacao1):
    try:
        #Tudo que for vírgula será substituido por ponto
        valNotas = inputNotas.get().replace(",",".")

        #Separa quando encontrar um traço           
        valNotas = valNotas.split("-")

        #Se a quantidade de notas for igual a quantidade de máterias
        if(len(valNotas) == numMaterias):
            #Verifica se são números
            continua = validateNotas(valNotas,numMaterias)

            if(continua):
                if(floatList(valNotas) == False):#Encontrou uma nota maior que 10
                    popUpWarning("Notas digitadas incorretas")
                    
                else:

                    if(setTable()):
                        cr = crSimular(tables, indices, valNotas, numMaterias)
                        getSimulacaoCR_text.set(f"CR = {cr:.3f}")
                    else:
                        popUpWarning("Arquivo não permitido")
            else:
                popUpWarning("Notas digitadas incorretas")
                
        else:
            popUpWarning("Notas digitadas incorretas")
    except:
        popUpError("Erro ao executar a opção escolhida")
        
 


#==================Trocar Frames
frame1 = Frame(window,bg = "#06335a")
frameCRAtual1 = Frame(window, bg = "#06335a")
frameMenu1 = Frame(window,bg = "#06335a")
frameMenuPeriodo1 = Frame(window,bg="#06335a")
frameMenuSimulacao1 = Frame(window,bg = "#06335a")
frameGetNotas1 = Frame(window,bg = "#06335a")
frameSobre = Frame(window,bg = "#06335a")

#Loop de frames
for frame in (frame1, frameSobre, frameCRAtual1, frameMenu1, frameMenuPeriodo1, frameMenuSimulacao1, frameGetNotas1):
    frame.grid(row = 0, column = 0, sticky = 'nsew')#sticky = coordenadas


#=================Configurando frames

#==========Frame CR Atual code
def frameCRAtual1_1():
    
    #Limpar o frame anterior e montar os componentes novamente
    clearFrame(frameCRAtual1)
    try:
        #Se for um histórico válido
        if(setTable()):
            #Recebe o valor do coeficiente de rendimento
            crText = currentCR(tables,indices)

            #conteúdo
            frameCRAtual1_title = Label(frameCRAtual1,text = f"\n\n\nCR = {crText:.3f}\n\n", bg= "#06335a",fg = "#ffffff",
                                    font = "Arial 15 bold")
            frameCRAtual1_title.pack(fill="x")

            frameCRAtual1_btn = Button(frameCRAtual1, text="Voltar",
                                command = lambda:show_frame(frameMenu1),
                                bg = "#fff",
                                font="Arial 12",
                                bd = 2,relief="raised")

        
            frameCRAtual1_btn.pack()

            #Para exibir o frame
            show_frame(frameCRAtual1)
        else:
            popUpWarning("Arquivo não permitido")
                   

    except:
        popUpError("Erro ao executar a opção escolhida")
        
 
#=============Frame para pegar as notas e mostrar o resultado da simulação code
def frameGetNotas1_1(inputNumMaterias):
    clearFrame(frameGetNotas1)
    
    try:        
        numMaterias = int(inputNumMaterias.get())
        
        #conteúdo
        frameGetNotas1_1_Title = Label(frameGetNotas1,
                                        text = f"Simular CR para {numMaterias} matérias",
                                        bg = "#06335a",fg = "#fff",
                                        font="Arial 13",pady = 20, justify = CENTER,width= 22)
        
        frameGetNotas1_1_Title.grid(row = 1, column = 1, padx = (largura / 3) + frameGetNotas1_1_Title['width'])

        getSimulacaoCR_text = StringVar()

        frameGetNotas1_1_Title = Label(frameGetNotas1,
                                        text = "Digite suas notas. Exemplo: Para 3 matérias colocar 7.5-8-5.8",
                                        bg = "#06335a",fg = "#fff",
                                        font="Arial 12",pady = 10, justify = CENTER)
        frameGetNotas1_1_Title.grid(row = 2, column = 1,padx = posx / 3)

        inputNotas = Entry(frameGetNotas1, bd = 1, relief = "flat",
                                font="Arial 12")
                 
        inputNotas.grid(row = 3, column = 1)

        frameGetNotas1_1_btn = Button(frameGetNotas1, text = "Calcular CR", 
                                command = lambda:getSimulacaoCR(numMaterias,inputNotas,getSimulacaoCR_text,frameMenuSimulacao1),
                                bg = "#fff",
                                font="Arial 12",
                                bd = 2,relief="raised")
        frameGetNotas1_1_btn.grid(row = 4, column = 1,pady = 10)

        
        frameGetNotas1_1_Title = Label(frameGetNotas1,
                                        textvariable = getSimulacaoCR_text,
                                        bg = "#06335a",fg = "#fff",
                                        font="Arial 15 bold",pady = 10, justify = CENTER)
        frameGetNotas1_1_Title.grid(row = 5, column = 1,padx = posx / 3)

        frameGetNotas1_1_btn = Button(frameGetNotas1, text = "Voltar", 
                                bg = "#fff",
                                font="Arial 12",
                                bd = 2,relief="raised", command = frameMenuSimulacao1_1)
        frameGetNotas1_1_btn.grid(row = 6, column = 1,pady = 10)
        
        
        show_frame(frameGetNotas1)
    except:
        popUpError("Erro ao executar a opção escolhida")
        
        



#==========Frame Menu Simulação code
def frameMenuSimulacao1_1():
    clearFrame(frameMenuSimulacao1)
    
    try:
        #conteúdo
        frameMenuSimulacao1_1_Title = Label(frameMenuSimulacao1,
                                        text = " Digite o número de matérias que você quer simular suas notas:",
                                        bg = "#06335a",fg = "#fff",
                                        font="Arial 12",pady = 20, justify = CENTER)
        frameMenuSimulacao1_1_Title.grid(row = 0, column = 1,padx = posx / 3)

        inputNumMaterias = Entry(frameMenuSimulacao1, bd = 1, relief = "flat",
                                font="Arial 12")
                 
        inputNumMaterias.grid(row = 1, column = 1)

        frameMenuSimulacao1_1_btn = Button(frameMenuSimulacao1, text = "Salvar", 
                                command = lambda: frameGetNotas1_1(inputNumMaterias),                                
                                bg = "#fff",
                                font="Arial 12",
                                bd = 2,relief="raised")
        frameMenuSimulacao1_1_btn.grid(row = 2, column = 1,pady = 10)

        frameGetNotas1_1_btn = Button(frameMenuSimulacao1, text = "Voltar", 
                                bg = "#fff",
                                font="Arial 12",
                                bd = 2,relief="raised", command = frameMenu1_1)
        frameGetNotas1_1_btn.grid(row = 3, column = 1,pady = 10)
        
       
        show_frame(frameMenuSimulacao1)
    except:
        popUpError("Erro ao executar a opção escolhida")
        
        

#==========Frame Menu Período code
def frameMenuPeriodo1_1():
    clearFrame(frameMenuPeriodo1)
    
    try:
        #conteúdo
        frameMenuPeriodo1_1_title = Label(frameMenuPeriodo1,text = "\nDigite na caixa de entrada abaixo o período desejado. Exemplo: 2018.1\n",
                            bg = "#06335a",fg = "#fff",
                            font="Arial 13")
        frameMenuPeriodo1_1_title.pack(fill="x")

        getPeriodo_text = StringVar()
        inputPeriodo = Entry(frameMenuPeriodo1,bd = 1,relief="flat",font="Arial 12")
        inputPeriodo.pack()

        frameMenuPeriodo1_1_title = Label(frameMenuPeriodo1,text="",bg= "#06335a")
        frameMenuPeriodo1_1_title.pack()

        getPeriodo_btn = Button(frameMenuPeriodo1, text="Calcular CR",
                                command = lambda:getPeriodo(inputPeriodo, getPeriodo_text),
                                bg = "#fff",
                                font="Arial 12",
                                bd = 2,relief="raised",width=20)
        getPeriodo_btn.pack()                        
        
        
        frameResult = Label(frameMenuPeriodo1,textvariable = getPeriodo_text,
                            bg = "#06335a", fg = "#fff",
                            font = "Arial 15 bold")
        frameResult.pack()
        
        frameMenuPeriodo1_1_btn = Button(frameMenuPeriodo1, text="Voltar",command = frameMenu1_1,
                            bg = "#fff",
                            font="Arial 12",
                            bd = 2,relief="raised")
        frameMenuPeriodo1_1_btn.pack()

        show_frame(frameMenuPeriodo1)
    except:
        popUpError("Erro ao executar a opção escolhida")
       
#==========Frame Menu code
def frameMenu1_1():
    clearFrame(frameMenu1)

    try:
       
        if(not path): #Se ainda não tem arquivo
            show_frame(frame1)
        else:
            #conteúdo
            frameMenu1_1_title = Label(frameMenu1,text = f"\n Caminho do Arquivo: {path}\n\n", 
                                bg= "#06335a",fg = "#ffffff",
                                font = "Arial 11 bold",
                                anchor=W, justify=LEFT, wraplength=largura)#wraplength quebrar o texto
            frameMenu1_1_title.pack(fill="x")

            frameMenu1_1_btn = Button(frameMenu1, text="Calcular CR atual",
                                command = frameCRAtual1_1,
                                bg = "#fff",
                                font="Arial 12",
                                bd = 2,relief="raised",width=40)
            frameMenu1_1_btn.pack()

            frameMenu1_1_title = Label(frameMenu1,text="",bg= "#06335a")
            frameMenu1_1_title.pack()

            frameMenu1_1_btn = Button(frameMenu1, text="Calcular o CR até um determinado período",
                                command = frameMenuPeriodo1_1,
                                bg = "#fff",
                                font="Arial 12",
                                bd = 2,relief="raised",width=40)
            frameMenu1_1_btn.pack()

            frameMenu1_1_title = Label(frameMenu1,text="",bg= "#06335a")
            frameMenu1_1_title.pack()

            frameMenu1_1_btn = Button(frameMenu1, text="Simular o CR com notas",
                                command = frameMenuSimulacao1_1,
                                bg = "#fff",
                                font="Arial 12",
                                bd = 2,relief="raised",width=40)
            frameMenu1_1_btn.pack()

            frameMenu1_1_title = Label(frameMenu1,text="",bg= "#06335a")
            frameMenu1_1_title.pack()

            frameMenu1_1_btn = Button(frameMenu1, text="Voltar",
                                command = frameFirstScreen,
                                bg = "#fff",
                                font="Arial 12",
                                bd = 2,relief="raised")
            frameMenu1_1_btn.pack()

            frameMenu1_1_title = Label(frameMenu1,text="\nOBS: Pode demorar alguns segundos para apresentar o resultado",
                            bg="#06335a",fg= "#FFEF3D",
                            font = "Arial 11")
            frameMenu1_1_title.pack()
        
            
            show_frame(frameMenu1)

    except:
        popUpError("Erro ao executar o menu principal")
        

#==========Frame Sobre code
def frameSobre1():
    clearFrame(frameSobre)

    try:
        #conteúdo
        frameSobre_Label = Label(frameSobre,text = "Sobre",bg = "#06335a",fg = "#fff",
                                font = "Arial 16 bold",width = 5)
        frameSobre_Label.grid(row = 0, column = 0,sticky = N, padx = 320, pady = 10)

        frameSobre_Label = Label(frameSobre,text = "Criado por: Julia Robaina",
                                bg = "#06335a", fg = "#fff",
                                font = "Arial 13")
        frameSobre_Label.grid(row = 1, column = 0, sticky = W, padx = 5)

        frameSobre_Label = Label(frameSobre,text = "Ícones de erro e atenção, criado por: Hopstarter",
                                bg = "#06335a", fg = "#fff",
                                font = "Arial 13")
        frameSobre_Label.grid(row = 2, column = 0, sticky = W, padx = 5,pady = 5)

        frameSobre_btn = Button(frameSobre, text="Voltar",
                                command = frameFirstScreen,
                                bg = "#fff",
                                font="Arial 12",
                                bd = 2,relief="raised")
        frameSobre_btn.grid(row = 3, column = 0, pady = 50)

        show_frame(frameSobre)
    except:
        popUpError("Erro ao executar a opção escolhida")
       
#==========Frame da primeira tela code
def frameFirstScreen():
    clearFrame(frame1)

    try:
        #conteúdo
        frame1_title = Label(frame1,text = "\nQual é o meu Coeficiente de Rendimento?", bg= "#06335a",fg = "#ffffff",font = "Arial 18 bold")
        frame1_title.pack(fill="x")
        frame1_title = Label(frame1,
                            text = "\n*Aqui você poderá:\n\n *Calcular o CR atual\n *Calcular o CR até um determinado período\n *Simular o CR com notas\n\nSelecione o seu histórico para acessar as opções acima.\n",
                            bg= "#06335a",fg = "#ffffff",
                            font = "Arial 13 ", 
                            anchor=W, justify=LEFT)
        frame1_title.pack(fill="x")
        
        frame1_btn = Button(frame1, text="Selecione o seu histórico",command = openWindowFileDialog, bg = "#fff",width=20,font="Arial 12",bd = 2,relief="raised")
        frame1_btn.pack()
        frame1_title = Label(frame1,text="",bg= "#06335a")
        frame1_title.pack()
        frame1_btn = Button(frame1, text="Sobre", command = frameSobre1, 
                            bg = "#fff",font="Arial 12",bd = 2,relief="raised")
        frame1_btn.pack(anchor = E,pady = 30,padx = 10)

        show_frame(frame1)
    except:
        popUpError("Erro ao executar o programa")
        

#Primeira tela a ser exibida
frameFirstScreen()

#Para fechar com CTRL + W
window.bind("<Control_L><w>", lambda x: window.destroy())

#Loop Principal
window.mainloop()