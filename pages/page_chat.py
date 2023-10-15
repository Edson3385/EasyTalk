import flet as ft
import socket 
import threading
import time


import sys

sys.path.insert(1, "./functions")

sys.path.insert(2, "./functions")

sys.path.insert(3, "./functions")

sys.path.insert(4, "./functions")

sys.path.insert(5, "./functions")

sys.path.insert(6, "./functions")


import users as us
import f_tradutor as td
import f_audio as ad
import f_transcricao as tr
import f_corretor as ct
import image as img



def main(page: ft.Page):

    # new_message = ft.TextField()

    # def on_message(message: Message):
    #     chat.controls.append(ft.Text(f"{message.user}: {message.text}"))
    #     page.update()

    # page.pubsub.subscribe(on_message)


    # def send_click(e):
    #     page.pubsub.send_all(Message(user=page.session_id, text=new_message.value))
    #     new_message.value = ""
    #     page.update()

    

    # coluna = ft.Column(controls=[chat, ft.Row(controls=[new_message, ft.ElevatedButton("Send", on_click=send_click)])])


    chat = ft.Column(height=550, scroll=ft.ScrollMode.ALWAYS)

    def txt_on_focus(e):
        e.control.label = "" 
        e.control.update()

    def txt_on_blur(e):
        e.control.label = "Escreva uma mensagem" 
        e.control.update()

    
    def show_banner(e):
        page.banner.open = True
        page.update()

    def close_banner(e):
        page.banner.open = False
        page.update()

    

    SERVER_IP = '192.168.15.121'
    SERVER_PORT = 8080

    def send_click(e):
        
        # Conecta o cliente ao servidor
       # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #client.connect((SERVER_IP, SERVER_PORT))

        txt_message = ft.Text(new_message.value, size=30, text_align=ft.CrossAxisAlignment.END, color=ft.colors.BLACK)

        if new_message.value.__len__() >= 26:
            txt_message.width = 400
            page.update()

        chat.controls.append(
                ft.Row(
                    controls=[
                                ft.Container(content=txt_message, bgcolor=ft.colors.WHITE, border_radius=10, padding=10)
                            ],
                         
                            width = 1500, 
                            alignment=ft.MainAxisAlignment.END,
                            vertical_alignment=ft.MainAxisAlignment.END
                )
        )
    

        page.update()

        # As mensagens vão para o servidor
        messages = new_message.value
        client.send((us.User.getUser() + ": " + messages).encode('utf-8'))

        new_message.value = ""

        page.update()
        
        #message = client.recv(1024).decode('utf-8')


    def btn_traduzir(e):
        
         txt_original = e.value
         traducao = td.Tradutor(txt_original)

         msg_traduzida = traducao.traduzir()

         print(msg_traduzida)

         e.value = msg_traduzida

         page.update()

         time.sleep(10)

         e.value = txt_original

         page.update()


    def ouvir(e):

        msg = e.value

        corretor = ct.Corretor(msg)
        msg_corrigida = corretor.corrigir()
        
        ad.audiodescricao(msg_corrigida)


    

         

        
    def receive_messages(usuario_socket):
        while True:
            try:
                message_recebida = usuario_socket.recv(1024).decode('utf-8')
                msg = message_recebida.split(":")
                user = msg[0]
                mensagem_exibida = msg[1]
                print(user[0])
                txt_mensagem = ft.Text(mensagem_exibida, size=30, text_align=ft.CrossAxisAlignment.END, color=ft.colors.BLACK)
                txt_message = ft.Column(controls=[  
                ft.Row(controls=[ft.CircleAvatar(bgcolor=ft.colors.PURPLE), ft.Text(user, color=ft.colors.BLACK, weight="bold")]),
                txt_mensagem,
                ft.Row(controls=[ft.IconButton(icon=ft.icons.TRANSLATE, icon_color="#771AC9", on_click=lambda e: btn_traduzir(txt_mensagem)), 
                                 ft.IconButton(icon=ft.icons.MULTITRACK_AUDIO, icon_color="#771AC9", on_click=lambda e: ouvir(txt_mensagem))])])
                
                print('recebe: '+ mensagem_exibida)

                
                if mensagem_exibida.__len__() >= 26:
                    txt_message.width = 400
                    page.update()


                container_msg = ft.Container(content=txt_message, bgcolor=ft.colors.WHITE, border_radius=10, padding=10)
                
                chat.controls.append(
                ft.Row(
                    controls=[
                                container_msg
                            ],
                         
                            width = 1500, 
                            alignment=ft.MainAxisAlignment.START,
                )
                )
                page.update()
            except:
                print("Erro.")
                usuario_socket.close()
                break

    def multiline(e):

        if new_message.value.__len__() >= 64:
            new_message.multiline = True
            new_message.height = 70
        else:
            new_message.multiline = False
            new_message.height = 50

        page.update()

        


    new_message = ft.TextField(label="Escreva uma mensagem", width=700,  border_radius=15,
        color=ft.colors.BLACK,
        border='NONE',
        on_focus=txt_on_focus,
        on_blur=txt_on_blur,
        on_submit=send_click,
        on_change=multiline,
        multiline=False,
        height=50
        )
    
    
    def transcrever(e):
        
        try:
            msg_transcrita = tr.transcrever()
            new_message.label = ""
            new_message.value = msg_transcrita
            send_click(e)
            page.update()
            time.sleep(5)
            pass
        except:
            page.banner.leading = ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40)
            page.banner.content = ft.Text("Não conseguimos te escutar. Verifique se o seu microfone está funcionando perfeitamente e tente novamente.", color=ft.colors.BLACK)
            page.banner.actions = [ft.TextButton(content=ft.Text("OK", color=ft.colors.BLACK), on_click=close_banner)]
            show_banner(e)
            time.sleep(10)
            page.banner.open = False
            page.update()



    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, SERVER_PORT))
    receive_thread = threading.Thread(target=receive_messages, args=(client, ))
    receive_thread.start()
    # receive_thread = threading.Thread(target=receba)
    # receive_thread.start()

     #uso dos dados do arquivo
    def pick_files_result(e: ft.FilePickerResultEvent):
        
            try:
                caminho =  (
                  ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
                );

                new_message.label = ""
                new_message.value = img.camImagem(caminho)
                multiline(e)
                page.update()

            except:
                page.banner.leading = ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.RED, size=40)
                page.banner.content = ft.Text("Não conseguimos ler a imagem selecionada. Verifique se o arquivo não está corrompido ou se a imagem está nítida o suficiente.", color=ft.colors.BLACK)
                page.banner.actions = [ft.TextButton(content=ft.Text("OK", color=ft.colors.BLACK), on_click=close_banner)]
                show_banner(e)
                time.sleep(10)
                page.banner.open = False
                page.update()
        #   selected_files.update()
        
    #botao para abrir o arquivo
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
  


    send_message = ft.IconButton(icon=ft.icons.SEND_ROUNDED, icon_color="#771AC9",on_click=send_click)
    transcribe_msg = ft.IconButton(icon=ft.icons.MIC, icon_color="#771AC9",on_click=transcrever)
    transcribe_img = ft.IconButton(icon=ft.icons.IMAGE_SEARCH, icon_color="#771AC9", on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=True, file_type= ft.FilePickerFileType.IMAGE))
    
    page.overlay.append(pick_files_dialog)

    column_send_message = ft.Column(
        controls=[
            ft.Row(controls=[new_message, transcribe_img, transcribe_msg, send_message], alignment="CENTER"),
        ],
        alignment=ft.MainAxisAlignment.CENTER
        )
    
    container_send_message = ft.Container(
        content=column_send_message, 
        bgcolor=ft.colors.WHITE, 
        width=1500, 
        height=70,  
        border_radius=15
        )
    


    column_chat = ft.Column(
        controls=[
            chat,
            container_send_message],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            expand=True,
            )

  

    def txt_chat_on_blur(e):
        e.control.label = "Pesquise ou inicie uma nova conversa"
        e.control.update()

    new_chat = ft.TextField(label="Pesquise ou inicie uma nova conversa",
                             color=ft.colors.WHITE,
                            border='NONE',
                            width=380,
                            on_focus=txt_on_focus,
                            on_blur=txt_chat_on_blur)

    search = ft.IconButton(icon=ft.icons.SEARCH, icon_color=ft.colors.WHITE)

    column_search_chat = ft.Column(
        controls=[
            ft.Row(controls=[new_chat, search], alignment="CENTER"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    container_search_chat = ft.Container(
        content=column_search_chat, 
        bgcolor="#771AC9", 
        width=450, 
        height=60,  
        border_radius=15
    )
    


    rail = ft.NavigationRail(
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=500,
        min_extended_width=400,
        leading=container_search_chat,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(

            ),
        ],
        bgcolor=ft.colors.WHITE
    )

    container = ft.Container(content=rail, border_radius=15)
   
    linha = ft.Row(
        controls=[
            container,
            column_chat
        ],
           expand=True,
           width=page.window_max_width)
    


    view = ft.View(
        "/page_chat",
        [
            linha
        ],
        bgcolor="#771AC9",
        vertical_alignment='END',
        horizontal_alignment="CENTER",
        
    )

    return view
