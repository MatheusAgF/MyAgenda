import customtkinter as ctk
from PIL import Image
from datetime import datetime
import agenda


app = ctk.CTk(fg_color='#d8d9e6')
app.geometry('1005x590')
app.resizable(width=False, height=False)
app.title('MyAgenda')

def erro(texto):
    def fade_out(label, i=0):
        esmaecer = ["#ff0000","#ff0000","#ff0000","#ff0000","#e6001a",
                    "#cc0033","#b3004d","#990066","#800080","#660099",
                    "#4d00b3","#0f1cbe"]
        
        if i < len(esmaecer):
            label.configure(text_color=esmaecer[i])
            app.after(250, fade_out, label, i + 1)
        else:
            mensagem_erro.destroy()

    mensagem_erro = ctk.CTkLabel(
        frame,
        text=texto,
        text_color="#d94747",
        fg_color='#0f1cbe',
        bg_color='#0f1cbe',
        font=ctk.CTkFont(slant='roman',size=17, weight='bold'),)
    mensagem_erro.place(x=330,y=9.5)
    fade_out(mensagem_erro)



frame = ctk.CTkFrame(
    app,
    width=991,
    height=47,
    fg_color='#0f1cbe',
    bg_color='transparent')
frame.place(x=7, y=8)

text = ctk.CTkLabel(
    frame,
    text='MyAgenda',
    text_color='#d8d9e6',
    fg_color='transparent',
    font=ctk.CTkFont(slant='italic',size=20, weight='bold'))
text.place(x=54,y=9.5)

img = ctk.CTkImage(
    Image.open('icone.png'), size=(30,30))
inicio = ctk.CTkLabel(
    frame,
    image=img,
    text='')
inicio.place(x=16, y=8)

data_atual = datetime.today()
today = data_atual.strftime(r"%d/%m/%Y")
data = ctk.CTkLabel(
    frame,
    text=f'{today}',
    text_color='#d8d9e6',
    fg_color='transparent',
    font=ctk.CTkFont(slant='italic',size=17, weight='bold'))
data.place(x=870, y=10)



def frameAdicionar():
    frame = ctk.CTkFrame(
        app, 
        width=991,
        height=47,
        fg_color='#b2b3c2',
        bg_color='transparent')
    frame.place(x=7,y=58)

    entrada = ctk.CTkEntry(
        frame, 
        placeholder_text='Adicionar tarefa', 
        placeholder_text_color='#e8e8f0',
        text_color='#4d4d53',
        font=ctk.CTkFont(slant='italic',size=12, weight='bold'),
        fg_color='transparent', 
        bg_color='transparent',
        width=780)
    entrada.place(x=30,y=8)


    def adicionar():
        text = entrada.get()
        comando = ['a'] + text.split()
        try:
            agenda.processarComandos(comando)
            entrada.delete(0, 'end')
        except IndexError:
            erro('Adicione conteúdo ao texto para adicionar')


    btn_adicionar = ctk.CTkButton(
        frame,
        text='ADICIONAR',
        fg_color="#06ba54",
        bg_color='transparent',
        text_color="#d8d9e6",
        hover_color="#23a159",
        font=ctk.CTkFont(slant='italic',size=14, weight='bold'),
        command=adicionar)
    btn_adicionar.place(x=820,y=8)
lixeira = ctk.CTkImage(Image.open('lixeira.png'), size=(30,30))
frame_list = None
def frameLista(comando):
    global frame_list

    if frame_list is not None and frame_list.winfo_exists():
        frame_list.destroy()

    frame_list = ctk.CTkScrollableFrame(
        ToDo,
        label_text='Tarefas',
        width=950,
        height=350,
        orientation='vertical',
        fg_color='#b2b3c2',
        label_fg_color='#0f1cbe',
        bg_color='transparent')
    frame_list.place(x=3,y=0)

    def criarTarefa(tarefa):
        def concluir():
            agenda.processarComandos(['f',f'{tarefa[3]+1}'])
            frameLista(comando)

        def priorizar(escolha):
            agenda.processarComandos(['p',f'{tarefa[3]+1}',f'{escolha}'])
            frameLista(comando)

        def remover():
            agenda.processarComandos(['r',f'{tarefa[3]+1}'])
            frameLista(comando)
        try:
            data_tarefa = f'{tarefa[0][0]}{tarefa[0][1]}/{tarefa[0][2]}{tarefa[0][3]}/{tarefa[0][4]}{tarefa[0][5]}{tarefa[0][6]}{tarefa[0][7]}'
        except:
            data_tarefa = ''
        try:
            hora_tarefa = f'- {tarefa[1][0]}{tarefa[1][1]}:{tarefa[1][2]}{tarefa[1][3]}'
        except:
            hora_tarefa = ''

        
        tarefa_frame = ctk.CTkFrame(
            frame_list,        
            width=960,
            height=50,
            fg_color="#9e9fab",
            bg_color='transparent')
        tarefa_frame.pack(pady=2)

        tarefa_text = ctk.CTkCheckBox(
            tarefa_frame,
            width=100,
            height=30,
            text=f'{tarefa[2]}',
            font=('arial',18),
            text_color='black',
            hover_color="#77787c",
            command=concluir)
        tarefa_text.place(x=30, y=9)

        data = ctk.CTkLabel(
            tarefa_frame,
            text=f'{data_tarefa} {hora_tarefa}',
            text_color='red',
            font=ctk.CTkFont('roman',11),
            bg_color='transparent',
            fg_color='transparent',
            height=10)
        data.place(x=60, y=33)

        select_priorizar = ctk.CTkOptionMenu(
            tarefa_frame,
            values=['#','A','B','C','D','E','F','G','H'],
            fg_color='#b2b3c2',
            text_color='black',
            button_color='#0f1cbe',
            dropdown_fg_color="#898995",
            width=22,
            height=22,
            font=ctk.CTkFont(slant='roman',size=15),
            dropdown_font=ctk.CTkFont(slant='roman',size=15),
            command=priorizar)
        select_priorizar.place(x=830,y=15)

        btn_remover = ctk.CTkButton(
            tarefa_frame,
            image=lixeira,
            bg_color='transparent',
            fg_color='transparent',
            hover_color="#8a8b94",
            text='',
            width=22,
            height=29,
            command=remover)
        btn_remover.place(x=880, y=7)

    try:
        lista = agenda.processarComandos(comando)
        for tarefa in lista:
            criarTarefa(tarefa)
    except:
        erro('Não foi possível realizar o comando')
        frameLista(['l'])
    return



frame_list_Done = None
def concluidos(comando):
    global frame_list_Done
    if frame_list_Done is not None and frame_list_Done.winfo_exists():
        frame_list_Done.destroy()

    frame_list_Done = ctk.CTkScrollableFrame(
        Done,
        label_text='Tarefas',
        width=950,
        height=350,
        orientation='vertical',
        fg_color='#b2b3c2',
        label_fg_color='#0f1cbe',
        bg_color='transparent')
    frame_list_Done.place(x=3,y=0)

    def criarTarefa(tarefa):
        def desfazer():
            agenda.processarComandos(['D',f'{tarefa[3]+1}'])
            concluidos(comando)

        def remover():
            agenda.processarComandos(['R',f'{tarefa[3]+1}'])
            concluidos(comando)

        try:
            data_tarefa = f'{tarefa[0][0]}{tarefa[0][1]}/{tarefa[0][2]}{tarefa[0][3]}/{tarefa[0][4]}{tarefa[0][5]}{tarefa[0][6]}{tarefa[0][7]}'
        except:
            data_tarefa = ''
        try:
            hora_tarefa = f'- {tarefa[1][0]}{tarefa[1][1]}:{tarefa[1][2]}{tarefa[1][3]}'
        except:
            hora_tarefa = ''

        
        tarefa_frame = ctk.CTkFrame(
            frame_list_Done,        
            width=960,
            height=50,
            fg_color="#9e9fab",
            bg_color='transparent')
        tarefa_frame.pack(pady=2)

        tarefa_text = ctk.CTkCheckBox(
            tarefa_frame,
            width=100,
            height=30,
            text=f'{tarefa[2]}',
            font=('arial',18),
            text_color='black',
            hover_color="#77787c",
            command=desfazer)
        tarefa_text.place(x=30, y=9)
        tarefa_text.select()

        data = ctk.CTkLabel(
            tarefa_frame,
            text=f'{data_tarefa} {hora_tarefa}',
            text_color='red',
            font=ctk.CTkFont('roman',11),
            bg_color='transparent',
            fg_color='transparent',
            height=10)
        data.place(x=60, y=33)

        btn_remover = ctk.CTkButton(
            tarefa_frame,
            image=lixeira,
            bg_color='transparent',
            fg_color='transparent',
            hover_color="#8a8b94",
            text='',
            width=22,
            height=29,
            command=remover)
        btn_remover.place(x=880, y=7)

    try:
        lista = agenda.processarComandos(comando)
        for tarefa in lista:
            criarTarefa(tarefa)
    except:
        erro('Não foi possível realizar o comando')
        frameLista(['l'])
    return


def mudarAba():
    aba = tabview.get()
    if aba == 'Done':
        concluidos(['d'])
    # if aba == 'To-Do':
    #     frameLista(['l'])


tabview = ctk.CTkTabview(
    app,
    width=991,
    height=450,
    border_color='#b2b3c2',
    command=mudarAba)
tabview.place(x=7,y=135)
tabview.add('To-Do')
tabview.add('Done')
ToDo = tabview.tab('To-Do')
ToDo.grid_columnconfigure(0, weight=1)
Done = tabview.tab('Done')
Done.grid_columnconfigure(0, weight=1)


def Menu():
    filtro = None
    def entrada(escolha):
        nonlocal filtro

        if filtro is not None and filtro.winfo_exists():
            filtro.destroy()
            filtro = None

        if escolha == 'Padrão':
            return
        
        filtro = ctk.CTkEntry(
            app,
            placeholder_text=escolha,
            placeholder_text_color='black',
            text_color='black',
            font=ctk.CTkFont(slant='roman', size=13, weight='bold'),
            fg_color='transparent',
            bg_color='transparent',
            width=695)
        filtro.place(x=7, y=115)
    

    menu = ctk.CTkOptionMenu(
        app,
        values=['Padrão','Prioridades','Contexto','Projeto'],
        fg_color='#b2b3c2',
        text_color='black',
        button_color='#0f1cbe',
        dropdown_fg_color="#898995",
        font=ctk.CTkFont(slant='roman',size=15),
        dropdown_font=ctk.CTkFont(slant='roman',size=15),
        command=entrada)
    menu.place(x=710,y=115)


    def selecionar():
        comando = ['l']
        if filtro != None:
            text = filtro.get()
            if menu.get() == 'Contexto':
                text = '@' + filtro.get()

            if menu.get() == 'Projeto':
                text = '+' + filtro.get()
            comando = ['l'] + [text]
            filtro.delete(0, 'end')
        return frameLista(comando)
        

    confirmar = ctk.CTkButton(
        app,
        text='Listar',
        fg_color='#06ba54',
        text_color='#d8d9e6',
        hover_color="#23a159",
        bg_color='transparent',
        font=ctk.CTkFont(slant='roman',size=15),
        command=selecionar)
    confirmar.place(x=856,y=115)



frameAdicionar()
Menu()
app.mainloop()