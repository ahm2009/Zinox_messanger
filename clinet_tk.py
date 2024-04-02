from tkinter import *
import socket
import threading
import webbrowser
import pass_Tk
import easygui
import keyboard
import wave
import pyaudio
import os
import time
from pynput import keyboard as keyboardnput
c=0
step_message=1.0
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',55555))

window=Tk()
save_as_list=[]
local_save_list=[]
paused = False
recording=True

if not os.path.exists('received files/'):
    os.mkdir('received files')
if not os.path.exists('received voices/'):
    os.mkdir('received voices')
if not os.path.exists('sent voices/'):
    os.mkdir('sent voices')



def main(): # function for login
    with open('password_usernames.txt' , 'r') as f:
        while True:
            line=f.readline()
            line1=line.split(':')
            if line == '':
                check_pass=False
                lbl_error['text']='password or username is not correct'
                break
            elif pass_input.get() in line1[1] and user_input.get() in line1[0] :
                check_pass=True
                break

    if len(pass_input.get())<8:
        lbl_error['text']='password must be at least 8 characters'
        pass_input.delete(0, END)
    
    elif check_pass == True:
         
        nickname=user_input.get()
        client.send(nickname.encode('ascii'))
        # GUI
        root = Tk()
        root.title("zinox")
        
        TEXT_COLOR = "gray1"
        FONT = "Tahoma 14"
        FONT_BOLD = "Helvetica 13 bold"
        
        window.destroy() #close window
        
        def receive():
            global c
            global step_message
            while True:  # Receive function
                
                message= client.recv(1024).decode('latin-1')
                if message=='no_text':
                    break
                elif message == 'file':
                    c+=1
                    filename=client.recv(1024).decode('latin-1')
                    local_save_list.append(filename)
                    file_pas=filename.split('.')

                    i=1
                    check_v_file=True

                    while check_v_file:
                        if os.path.exists(f'received files/received_file_{i}.{file_pas[len(file_pas)-1]}'):
                            i+=1
                        else:
                            check_v_file=False

                    save_as = f"received files\\received_file_{i}.{file_pas[len(file_pas)-1]}"
                    save_as_list.append(save_as)
                    client_check=client.recv(1024).decode('latin-1')
                    def file_open(filename):
                        webbrowser.open(filename)
                # Receive the file size from the client
                    file_size = int(float(client.recv(1024).decode('utf-8')))

                # Receive the file content from the client
                    file_data = b""
                    while len(file_data) < file_size:
                        remaining_bytes = file_size - len(file_data)
                        file_data += client.recv(remaining_bytes)
                # Save the received file to disk
                    if client_check!=nickname:
                        with open(save_as, "wb") as file:
                            file.write(file_data)
                    
                    txt.insert(END,'\n')
                    text_btn=f"File received successfully{c}."
                    if client_check==nickname:
                        button = Button(
                            root,
                            text='sent file',
                            padx=2,
                            pady=2,
                            bd=1,
                            highlightthickness=0,
                            font='timesnewroman 14',
                            bg='#5EE87D',
                            command= lambda m=c-1: file_open(local_save_list[m])
                        )
                    else:
                        button = Button(
                            root,
                            text=text_btn,
                            padx=2,
                            pady=2,
                            bd=1,
                            highlightthickness=0,
                            font='timesnewroman 14',
                            command= lambda m=c-1: file_open(save_as_list[m])
                        )
                    txt.window_create(END, window=button)
                    txt.insert(END,'\n')
                    step_message+=2

                elif message=='voice':
                    c+=1
                    filename=client.recv(1024).decode('latin-1')
                    local_save_list.append(filename)
                    file_pas=filename.split('.')
                    
                    i=1
                    check_v_file=True

                    while check_v_file:
                        if os.path.exists(f'received voices/received_file_{i}.{file_pas[len(file_pas)-1]}'):
                            i+=1
                        else:
                            check_v_file=False

                    save_as = f"received voices/received_file_{i}.{file_pas[len(file_pas)-1]}"
                    save_as_list.append(save_as)
                    client_check=client.recv(1024).decode('latin-1')
                    def play_voice(filename):
                        
                        global paused
                        # paused = False    # global to track if the audio is paused

                        
                        # you audio here
                        wf = wave.open(filename, 'rb')

                        # instantiate PyAudio
                        p = pyaudio.PyAudio()

                        # define callback
                        def callback(in_data, frame_count, time_info, status):
                            data = wf.readframes(frame_count)
                            return (data, pyaudio.paContinue)

                        # open stream using callback
                        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                        channels=wf.getnchannels(),
                                        rate=wf.getframerate(),
                                        output=True,
                                        stream_callback=callback)

                        # start the stream
                        stream.start_stream()

                        while stream.is_active() and paused==True:
                            stream.start_stream()
                        if paused==False:
                            stream.stop_stream()
                        paused = False


                        # stop stream
                        stream.stop_stream()
                        stream.close()
                        wf.close()

                        # close PyAudio
                        p.terminate()



                    def handel(filename):
                        global paused
                        if paused:
                            paused = False
                        else:
                            paused = True
                            # choose_voice.config(text='record')
                            threading.Thread(target=lambda : play_voice(filename)).start()
                        
                    # Receive the file size from the client
                    file_size = int(client.recv(1024).decode('utf-8'))
                    

                    # Receive the file content from the client
                    file_data = b""
                    while len(file_data) < file_size:
                        remaining_bytes = file_size - len(file_data)
                        file_data += client.recv(remaining_bytes)

                    # Save the received file to disk
                    if client_check!=nickname:
                        with open(save_as, "wb") as file:
                            file.write(file_data)
                        
                    txt.insert(END,'\n')
                    text_btn=f"voice received successfully{c}."
                    if client_check==nickname:
                        button = Button(
                            root,
                            text='sent voice',
                            padx=2,
                            pady=2,
                            bd=1,
                            highlightthickness=0,
                            font='timesnewroman 14',
                            bg='#5EE87D',
                            command= lambda m=c-1: handel(local_save_list[m])
                        )
                    else:
                        button = Button(
                            root,
                            text=text_btn,
                            padx=2,
                            pady=2,
                            bd=1,
                            highlightthickness=0,
                            font='timesnewroman 14',
                            command= lambda m=c-1: handel(save_as_list[m])
                        )
                    
                    txt.window_create(END, window=button)
                    txt.insert(END,'\n')
                    step_message+=2
                elif message!='':
                    client_check=client.recv(1024).decode('latin-1')
                    txt.insert(END,'\n')
                    lbl =Label(
                        root,
                        text=message,
                        padx=2,
                        pady=2,
                        bd=1,
                        font='timesnewroman 14',
                    )
                    txt.window_create(END, window=lbl)
                    txt.insert(END,'\n')
                    step_message+=2
                    if client_check==nickname:
                        lbl.config(bg='#5EE87D' ,)
                    else:
                        lbl.config(text=f'{client_check}:{message}')


        def write(): # Send function
            global check_voice
            global step_message     
            while True:
                client_message=e.get()

                if "" not  in client_message:
                    client.send('no_text'.encode('ascii'))
                    break

                elif "file" not  in client_message and 'voice' not in client_message:
                    message= f'{client_message}'
                    client.send(message.encode('ascii'))
                    client.send(nickname.encode('ascii'))
                    with open('client_messages.txt' , 'a') as writer:
                        writer.write(f'{message}\n')
                        
                e.delete(0, END)
                break

        def set_text(): # set file in input text
            e.delete(0,END)
            e.insert(0,'file')
        def set_voice(): # set voice in input text
            e.delete(0,END)
            e.insert(0,'voice')

        def record():
            global recording
            client.send('voice'.encode('ascii'))
            time.sleep(0.1)
            format = pyaudio.paInt16
            channels = 1
            rate = 44100
            chunk = 1024
            i=1
            check_v_file=True

            while check_v_file:
                if os.path.exists(f'sent voices/sent_file_{i}.wav'):
                    i+=1
                else:
                    check_v_file=False
            filename= f'sent voices/sent_file_{i}.wav'
            

            audio = pyaudio.PyAudio()
            stream = audio.open(format=format , channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
            frames= []
            start=time.time()
            while recording:
                    data=stream.read(chunk)
                    frames.append(data)

                    stop_time=time.time() - start
                    secs= stop_time%60
                    mins=stop_time//60
                    hour=mins//60
                    choose_voice.config(text=f'{int(hour):02d}:{int(mins):02d}:{int(secs):02d}')
            choose_voice.config(text='🎙')
            stream.start_stream()
            stream.close()
            audio.terminate()

            file= wave.open(filename , 'wb')
            file.setnchannels(channels)
            file.setsampwidth(audio.get_sample_size(format))
            file.setframerate(rate)
            file.writeframes(b''.join(frames))
            file.close()

            # Open the file in binary mode
            
            client.send(filename.encode('ascii'))
            time.sleep(0.1)
            client.send(nickname.encode('ascii'))
            time.sleep(0.1)
            with open(filename, "rb") as file:
                # Read the file content
                file_data = file.read()

            # Send the file size to the server
            client.sendall(str(len(file_data)).encode('utf-8'))
            time.sleep(0.1)
            # Send the file content to the server
            client.sendall(file_data)
            

            

        def handel():
            global recording
            if recording:
                recording = False
                choose_voice.config(text='🎙')
            else:
                recording = True
                # choose_voice.config(text='record')
                threading.Thread(target=record).start()
        def send_file():
            filename = easygui.fileopenbox()
            if filename!=None:


                client.send('file'.encode('ascii'))
                time.sleep(0.1)
            # Open the file in binary mode
                
                client.send(filename.encode('ascii'))
                time.sleep(0.1)
                client.send(nickname.encode('ascii'))
                time.sleep(0.1)
                with open(filename, "rb") as file:
                # Read the file content
                    file_data = file.read()

                client.send(str(len(file_data)).encode('utf-8'))
                time.sleep(0.1)
            # Send the file content to the server
                client.send(file_data)
                
                
                


        
        lable1 = Label(
            root,
            bg='#FFB74D',
            fg=TEXT_COLOR,
            text=nickname,
            font='tahoma 14 bold italic',
            pady=20,
            width=20,
            height=1
        )
        lable1.grid(row=0)

        txt = Text(root, fg=TEXT_COLOR, font='times 16 italic bold',width=85 , bg='#A6ACAF')
        txt.grid(row=1, column=0, columnspan=4 , sticky=(S,W))
        
        scrollbar = Scrollbar(txt)
        scrollbar.place(relheight=1, relx=0.974)
        
        e = Entry(root, bg='#BF360C', font=FONT, width=60)
        e.grid(row=2, column=0, sticky=(W,E))
    
        send = Button(
            master=root,
            text="✍",
            font='Helvetica 15 bold',
            bg='#FF9800',
            command=write,
        )

        send.grid(row=2, column=1 , sticky=(W,E))


        choose_file=Button(
            root,
            text="📂",
            font='Helvetica 15 bold',
            bg='#FF9800',
            command=send_file,
        )

        choose_file.grid(row= 2 , column=2 , sticky=(W,E))

        choose_voice=Button(
            root,
            text="🎙",
            font='Helvetica 15 bold',
            bg='#FF9800',
            command=handel,
        )

        choose_voice.grid(row= 2 , column=3 , sticky=(W,E))


        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        # write_thread = threading.Thread(target=write)
        # write_thread.start()

        threading.Thread(target=handel).start()
        # threading.Thread(target=send_file).start()



        root.mainloop()

def sing_up(): # function for sing up 
    window2=Tk()
    window.destroy()

    def main_sing(): # function for open new window
        if len(pass_input.get())<8:
            lbl_error['text']='password must be at least 8 characters'
            pass_input.delete(0, END)
        elif pass_input.get()!=pass_input2.get():
            lbl_error['text']='password and password again not equal'
        elif user_input.get == '' or last_name_input.get()=='' or first_name_input.get()=='':
            lbl_error['text']='some filed is empty '
        else:
            with open ('password_usernames.txt' , 'a') as f:
                f.write(user_input.get() + ':'+  pass_input.get()+ '\n')
                

            nickname=user_input.get()
            client.send(nickname.encode('ascii'))
            # GUI
            root = Tk()
            root.title("zinox")
            
            TEXT_COLOR = "gray1"
            FONT = "Tahoma 14"
            FONT_BOLD = "Helvetica 13 bold"
            
            window2.destroy() #close window
            
            def receive():
                global c
                global step_message
                while True:  # Receive function
                    
                    message= client.recv(1024).decode('latin-1')
                    if message=='no_text':
                        break
                    elif message == 'file':
                        c+=1
                        filename=client.recv(1024).decode('latin-1')
                        local_save_list.append(filename)
                        file_pas=filename.split('.')

                        i=1
                        check_v_file=True

                        while check_v_file:
                            if os.path.exists(f'received files/received_file_{i}.{file_pas[len(file_pas)-1]}'):
                                i+=1
                            else:
                                check_v_file=False

                        save_as = f"received files\\received_file_{i}.{file_pas[len(file_pas)-1]}"
                        save_as_list.append(save_as)
                        client_check=client.recv(1024).decode('latin-1')
                        def file_open(filename):
                            webbrowser.open(filename)
                    # Receive the file size from the client
                        file_size = int(float(client.recv(1024).decode('utf-8')))

                    # Receive the file content from the client
                        file_data = b""
                        while len(file_data) < file_size:
                            remaining_bytes = file_size - len(file_data)
                            file_data += client.recv(remaining_bytes)
                    # Save the received file to disk
                        if client_check!=nickname:
                            with open(save_as, "wb") as file:
                                file.write(file_data)
                        
                        txt.insert(END,'\n')
                        text_btn=f"File received successfully{c}."
                        if client_check==nickname:
                            button = Button(
                                root,
                                text='sent file',
                                padx=2,
                                pady=2,
                                bd=1,
                                highlightthickness=0,
                                font='timesnewroman 14',
                                bg='#5EE87D',
                                command= lambda m=c-1: file_open(local_save_list[m])
                            )
                        else:
                            button = Button(
                                root,
                                text=text_btn,
                                padx=2,
                                pady=2,
                                bd=1,
                                highlightthickness=0,
                                font='timesnewroman 14',
                                command= lambda m=c-1: file_open(save_as_list[m])
                            )
                        txt.window_create(END, window=button)
                        txt.insert(END,'\n')
                        step_message+=2

                    elif message=='voice':
                        c+=1
                        filename=client.recv(1024).decode('latin-1')
                        local_save_list.append(filename)
                        file_pas=filename.split('.')
                        
                        i=1
                        check_v_file=True

                        while check_v_file:
                            if os.path.exists(f'received voices/received_file_{i}.{file_pas[len(file_pas)-1]}'):
                                i+=1
                            else:
                                check_v_file=False

                        save_as = f"received voices/received_file_{i}.{file_pas[len(file_pas)-1]}"
                        save_as_list.append(save_as)
                        client_check=client.recv(1024).decode('latin-1')
                        def play_voice(filename):
                            
                            global paused
                            # paused = False    # global to track if the audio is paused

                            
                            # you audio here
                            wf = wave.open(filename, 'rb')

                            # instantiate PyAudio
                            p = pyaudio.PyAudio()

                            # define callback
                            def callback(in_data, frame_count, time_info, status):
                                data = wf.readframes(frame_count)
                                return (data, pyaudio.paContinue)

                            # open stream using callback
                            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                            channels=wf.getnchannels(),
                                            rate=wf.getframerate(),
                                            output=True,
                                            stream_callback=callback)

                            # start the stream
                            stream.start_stream()

                            while stream.is_active() and paused==True:
                                stream.start_stream()
                            if paused==False:
                                stream.stop_stream()
                            paused = False


                            # stop stream
                            stream.stop_stream()
                            stream.close()
                            wf.close()

                            # close PyAudio
                            p.terminate()



                        def handel(filename):
                            global paused
                            if paused:
                                paused = False
                            else:
                                paused = True
                                # choose_voice.config(text='record')
                                threading.Thread(target=lambda : play_voice(filename)).start()
                            
                        # Receive the file size from the client
                        file_size = int(client.recv(1024).decode('utf-8'))
                        

                        # Receive the file content from the client
                        file_data = b""
                        while len(file_data) < file_size:
                            remaining_bytes = file_size - len(file_data)
                            file_data += client.recv(remaining_bytes)

                        # Save the received file to disk
                        if client_check!=nickname:
                            with open(save_as, "wb") as file:
                                file.write(file_data)
                            
                        txt.insert(END,'\n')
                        text_btn=f"voice received successfully{c}."
                        if client_check==nickname:
                            button = Button(
                                root,
                                text='sent voice',
                                padx=2,
                                pady=2,
                                bd=1,
                                highlightthickness=0,
                                font='timesnewroman 14',
                                bg='#5EE87D',
                                command= lambda m=c-1: handel(local_save_list[m])
                            )
                        else:
                            button = Button(
                                root,
                                text=text_btn,
                                padx=2,
                                pady=2,
                                bd=1,
                                highlightthickness=0,
                                font='timesnewroman 14',
                                command= lambda m=c-1: handel(save_as_list[m])
                            )
                        
                        txt.window_create(END, window=button)
                        txt.insert(END,'\n')
                        step_message+=2
                    elif message!='':
                        client_check=client.recv(1024).decode('latin-1')
                        txt.insert(END,'\n')
                        lbl =Label(
                            root,
                            text=message,
                            padx=2,
                            pady=2,
                            bd=1,
                            font='timesnewroman 14',
                        )
                        txt.window_create(END, window=lbl)
                        txt.insert(END,'\n')
                        step_message+=2
                        if client_check==nickname:
                            lbl.config(bg='#5EE87D' ,)
                        else:
                            lbl.config(text=f'{client_check}:{message}')


            def write(): # Send function
                global check_voice
                global step_message     
                while True:
                    client_message=e.get()

                    if "" not  in client_message:
                        client.send('no_text'.encode('ascii'))
                        break

                    elif "file" not  in client_message and 'voice' not in client_message:
                        message= f'{client_message}'
                        client.send(message.encode('ascii'))
                        client.send(nickname.encode('ascii'))
                        with open('client_messages.txt' , 'a') as writer:
                            writer.write(f'{message}\n')
                            
                    e.delete(0, END)
                    break

            def set_text(): # set file in input text
                e.delete(0,END)
                e.insert(0,'file')
            def set_voice(): # set voice in input text
                e.delete(0,END)
                e.insert(0,'voice')

            def record():
                global recording
                client.send('voice'.encode('ascii'))
                time.sleep(0.1)
                format = pyaudio.paInt16
                channels = 1
                rate = 44100
                chunk = 1024
                i=1
                check_v_file=True

                while check_v_file:
                    if os.path.exists(f'sent voices/sent_file_{i}.wav'):
                        i+=1
                    else:
                        check_v_file=False
                filename= f'sent voices/sent_file_{i}.wav'
                

                audio = pyaudio.PyAudio()
                stream = audio.open(format=format , channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
                frames= []
                start=time.time()
                while recording:
                        data=stream.read(chunk)
                        frames.append(data)

                        stop_time=time.time() - start
                        secs= stop_time%60
                        mins=stop_time//60
                        hour=mins//60
                        choose_voice.config(text=f'{int(hour):02d}:{int(mins):02d}:{int(secs):02d}')
                choose_voice.config(text='🎙')
                stream.start_stream()
                stream.close()
                audio.terminate()

                file= wave.open(filename , 'wb')
                file.setnchannels(channels)
                file.setsampwidth(audio.get_sample_size(format))
                file.setframerate(rate)
                file.writeframes(b''.join(frames))
                file.close()

                # Open the file in binary mode
                
                client.send(filename.encode('ascii'))
                time.sleep(0.1)
                client.send(nickname.encode('ascii'))
                time.sleep(0.1)
                with open(filename, "rb") as file:
                    # Read the file content
                    file_data = file.read()

                # Send the file size to the server
                client.sendall(str(len(file_data)).encode('utf-8'))
                time.sleep(0.1)
                # Send the file content to the server
                client.sendall(file_data)
                

                

            def handel():
                global recording
                if recording:
                    recording = False
                    choose_voice.config(text='🎙')
                else:
                    recording = True
                    # choose_voice.config(text='record')
                    threading.Thread(target=record).start()
            def send_file():
                filename = easygui.fileopenbox()
                if filename!=None:


                    client.send('file'.encode('ascii'))
                    time.sleep(0.1)
                # Open the file in binary mode
                    
                    client.send(filename.encode('ascii'))
                    time.sleep(0.1)
                    client.send(nickname.encode('ascii'))
                    time.sleep(0.1)
                    with open(filename, "rb") as file:
                    # Read the file content
                        file_data = file.read()

                    client.send(str(len(file_data)).encode('utf-8'))
                    time.sleep(0.1)
                # Send the file content to the server
                    client.send(file_data)
                    
                    
                    


            
            lable1 = Label(
                root,
                bg='#FFB74D',
                fg=TEXT_COLOR,
                text=nickname,
                font='tahoma 14 bold italic',
                pady=20,
                width=20,
                height=1
            )
            lable1.grid(row=0)

            txt = Text(root, fg=TEXT_COLOR, font='times 16 italic bold',width=85 , bg='#A6ACAF')
            txt.grid(row=1, column=0, columnspan=4 , sticky=(S,W))
            
            scrollbar = Scrollbar(txt)
            scrollbar.place(relheight=1, relx=0.974)
            
            e = Entry(root, bg='#BF360C', font=FONT, width=60)
            e.grid(row=2, column=0, sticky=(W,E))
        
            send = Button(
                master=root,
                text="✍",
                font='Helvetica 15 bold',
                bg='#FF9800',
                command=write,
            )

            send.grid(row=2, column=1 , sticky=(W,E))


            choose_file=Button(
                root,
                text="📂",
                font='Helvetica 15 bold',
                bg='#FF9800',
                command=send_file,
            )

            choose_file.grid(row= 2 , column=2 , sticky=(W,E))

            choose_voice=Button(
                root,
                text="🎙",
                font='Helvetica 15 bold',
                bg='#FF9800',
                command=handel,
            )

            choose_voice.grid(row= 2 , column=3 , sticky=(W,E))


            receive_thread = threading.Thread(target=receive)
            receive_thread.start()

            # write_thread = threading.Thread(target=write)
            # write_thread.start()

            threading.Thread(target=handel).start()
            # threading.Thread(target=send_file).start()
            root.mainloop()
    
    lbl_first_name= Label(
        master=window2,
        text='Enter a first name: ',
        width=20,
        height=1,
        font="Helvetica 13 bold",
    )

    lbl_last_name= Label(
        master=window2,
        text='Enter a last name: ',
        width=20,
        height=1,
        font="Helvetica 13 bold",
    )

    user_name_enter= Label(
        master=window2,
        text='chose a username: ',
        width=20,
        height=1,
        font="Helvetica 13 bold",
    )

    lbl_password= Label(
        master=window2,
        text='Enter a password: ',
        width=20,
        height=1,
        font="Helvetica 13 bold",
    )

    lbl_password2= Label(
        master=window2,
        text='Enter a password again : ',
        width=20,
        height=1,
        font="Helvetica 13 bold",
    )

    lbl_error= Label(
        master=window2,
        text='welcome ',
        font="Helvetica 13 bold"
    )

    user_input=Entry(
        master=window2,
        width=35,
        font="Helvetica 15",
    )

    pass_input=Entry(
        master=window2,
        width=35,
        font="Helvetica 15",
    )

    pass_input2=Entry(
        master=window2,
        width=35,
        font="Helvetica 15",
    )

    first_name_input=Entry(
        master=window2,
        width=35,
        font="Helvetica 15",
    )

    last_name_input=Entry(
        master=window2,
        width=35,
        font="Helvetica 15",
    )

    sing_up=Button(
        master=window2,
        text='sing up',
        width=40,
        height=2,
        command=main_sing
    )

    btn_make_password=Button(
        master=window2,
        text='use password generation',
        width=40,
        height=2,
        command=pass_Tk.password_generator,
        font="Helvetica 13 bold",
        background='aqua'
    )
    
    
    lbl_first_name.grid(row=0 , column=0 , pady=10 , padx=10)
    first_name_input.grid(row=0 , column= 1 , pady=10 , padx=(10 , 50))
    lbl_last_name.grid(row=1 , column=0 , pady=10 , padx=10)
    last_name_input.grid(row=1 , column= 1 , pady=10 , padx=(10 , 50))
    user_name_enter.grid(row=2 , column=0 , pady=10 , padx=10)
    user_input.grid(row=2 , column= 1 , pady=10 , padx=(10 , 50))
    lbl_password.grid(row=3 , column=0 , sticky=(E,W))
    pass_input.grid(row=3 , column= 1 , pady=10 , padx=(10 , 50))
    lbl_password2.grid(row=4 , column=0 , sticky=(E,W))
    pass_input2.grid(row=4 , column= 1 , pady=10 , padx=(10 , 50))
    sing_up.grid(row = 5 , column=0 , columnspan=2 ,)
    lbl_error.grid(row = 6 , column=0 , columnspan=2 , sticky=(E,W) , pady=30)
    btn_make_password.grid(row =7 , column=0 , columnspan=2 , pady=10)

    window2.mainloop()


user_name_enter= Label(
    master=window,
    text='chose a username: ',
    width=20,
    height=1,
    font="Helvetica 13 bold",
)

lbl_password= Label(
    master=window,
    text='Enter a password: ',
    width=20,
    height=1,
    font="Helvetica 13 bold",
)

lbl_error= Label(
    master=window,
    text='welcome ',
    font="Helvetica 13 bold"
)

user_input=Entry(
    master=window,
    width=35,
    font="Helvetica 15",
)

pass_input=Entry(
    master=window,
    width=35,
    font="Helvetica 15",
)

login=Button(
    master=window,
    text='login',
    width=40,
    height=2,
    command=main
)

btn_signup=Button(
   master=window,
   text='sing up',
   width=20,
   command=sing_up
)


window.bind('<Return>' , main) # for enter 
user_name_enter.grid(row=0 , column=0 , pady=10 , padx=10)
user_input.grid(row=0 , column= 1 , pady=10 , padx=(10 , 50))
lbl_password.grid(row=1 , column=0 , sticky=(E,W))
pass_input.grid(row=1 , column= 1 , pady=10 , padx=(10 , 50))
login.grid(row = 2 , column=0 , columnspan=2 ,)
lbl_error.grid(row = 3 , column=0 , columnspan=2 , sticky=(E,W) , pady=30)
btn_signup.grid(row = 4, column=1 , pady=15, padx=(30,10))
window.mainloop()