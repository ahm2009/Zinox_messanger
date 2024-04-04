from tkinter import *
import threading
import webbrowser
import easygui
import wave
import pyaudio
import os
import time




def receive(nickname , txt , root , client , c , object_list):  # Receive function


    while True:  
        
        message= client.recv(1024).decode('latin-1')
        if message == 'file':
            c+=1
            filename=client.recv(1024).decode('latin-1')
            file_pas=filename.split('.')

            i=1
            check_v_file=True

            while check_v_file:
                if os.path.exists(f'received files/received_file_{i}.{file_pas[len(file_pas)-1]}'):
                    i+=1
                else:
                    check_v_file=False

            save_as = f"received files\\received_file_{i}.{file_pas[len(file_pas)-1]}"
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
            if client_check==nickname:

                file=Received(filename , file_size , file_data)
            else:
                file=Received(save_as , file_size , file_data)
                file.receive_file()
            object_list.append(file)
            
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
                    command= lambda m=file: file_open(m.filename)
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
                    command= lambda m=file: file_open(m.filename)
                )
            txt.window_create(END, window=button)
            txt.insert(END,'\n')
            

        elif message=='voice':
            c+=1
            filename=client.recv(1024).decode('latin-1')
            file_pas=filename.split('.')
            
            i=1
            check_v_file=True

            while check_v_file:
                if os.path.exists(f'received voices/received_file_{i}.{file_pas[len(file_pas)-1]}'):
                    i+=1
                else:
                    check_v_file=False

            save_as = f"received voices/received_file_{i}.{file_pas[len(file_pas)-1]}"
            client_check=client.recv(1024).decode('latin-1')
            def played_voice(voice_object):
                
                voice_object.play_voice()

            def handel(object_v , c):
                if object_v.paused:
                    object_v.paused = False
                else:
                    
                    for i in range(len(object_list)):
                        if i!=c:
                            if object_list[i].paused == True:
                                object_list[i].paused = False

                    object_v.paused = True

                    # btn_choose_voice.config(text='record')
                    if object_v.s_stream:
                        threading.Thread(target=lambda : played_voice(object_v)).start()
                    object_v.s_stream = False
            # Receive the file size from the client
            file_size = int(client.recv(1024).decode('utf-8'))
            

            # Receive the file content from the client
            file_data = b""
            while len(file_data) < file_size:
                remaining_bytes = file_size - len(file_data)
                file_data += client.recv(remaining_bytes)

            # Save the received file to disk
            if client_check==nickname:
                voice=Received(filename , file_size , file_data)
            else:
                voice=Received(save_as , file_size , file_data)
                voice.receive_voice()
            object_list.append(voice)
                
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
                    command= lambda m=voice , c=c-1: handel(m , c)
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
                    command= lambda m=voice: handel(m)
                )
            
            txt.window_create(END, window=button)
            txt.insert(END,'\n')
            
        else:
            client_check=client.recv(1024).decode('latin-1')
            if message=="":
                pass
            elif message!=nickname:
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
                
                if client_check==nickname:
                    lbl.config(bg='#5EE87D' ,)
                else:
                    lbl.config(text=f'{client_check}:{message}')


class Received():
    def __init__(self , filename , filesize , data):
        self.filename = filename
        self.recording = True
        self.filesize = filesize
        self.data = data
        self.paused = False
        self.s_stream = True
    def play_voice(self):

        # you audio here
        wf = wave.open(self.filename, 'rb')

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
        if self.s_stream:
            stream.start_stream()

        while stream.is_active():
            if self.paused==False:
                stream.stop_stream()
            if stream.is_stopped():
                stream.start_stream()
            



        self.paused = False
        # stop stream
        stream.stop_stream()
        self.s_stream = True
        stream.close()
        wf.close()

        # close PyAudio
        p.terminate()
    def receive_voice(self):
        # Save the received file to disk
        with open(self.filename, "wb") as file:
            file.write(self.data)
    def receive_file(self):

            with open(self.filename, "wb") as file:
                file.write(self.data)



def write(entry , nickname , client): # Send function
    client_message=entry.get()    
    while True:
        if client_message == '':
            break


        if "file" not  in client_message and 'voice' not in client_message:
            message= f'{client_message}'
            client.send(message.encode('ascii'))
            client.send(nickname.encode('ascii'))
            with open('client_messages.txt' , 'a') as writer:
                writer.write(f'{message}\n')
                
        entry.delete(0, END)
        break

def send_file(nickname , client):
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