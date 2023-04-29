import tkinter
from tkinter import filedialog
import customtkinter
from  PIL import Image, ImageTk
import yt_dlp

# ask user to set download path when save to button is clicked
path = ""
def SetFilePath():
    #enable access to the path variable
    global path 
    path = filedialog.askdirectory()  
    
# get all available qualities of the video link provided
available_qualities = set()
def getQuality():
    #enable access to the available qualities set
    global available_qualities

    # restore the default value
    available_qualities = set()
    result.configure(text = "", fg_color = "transparent")
    result.update()

    try:
        # Set the download options
        ydl_opts = {
            'listformats' : True
        }

        # Create the downloader
        ydl = yt_dlp.YoutubeDL(ydl_opts)

        # Extract the video info
        video_info = ydl.extract_info(link_field.get(), download=False)

        # Get the available formats
        formats = video_info["formats"]

        # store available qualities
        for format in formats:
            if format['vcodec'] != 'none' and format['format_note'] != 'DASH video':
                available_qualities.add(f"{format['height']}")

        # sort the qualities
        available_qualities = sorted(available_qualities, key=int)
        
        # update the quality list
        quality_list.configure(values=available_qualities) 
              
    except:
        result.configure(text="Invalid link", fg_color="red")
        result.update()
        return
    
    # output operation success
    result.configure(text="Available qualities updated", fg_color="green") 
    result.update()

# progress hook function used to update the progress percentage
def my_hook(d):
    
    # display the progress percentage during downloading only
    if d['status'] == 'downloading':
        #calculate the progress percentage
        downloaded_bytes = d['downloaded_bytes']
        total_bytes = d['total_bytes_estimate']

        # calculate the estimated time and adjust the unit
        estimated_time = d['eta']
        unit = 's'
        if estimated_time > 60:
            estimated_time = round(estimated_time/60,2)
            unit = 'm'
        elif estimated_time > 3600:
            estimated_time = round(estimated_time/3600,2)
            unit = 'h'
        elif estimated_time > 86400:
            estimated_time = round(estimated_time/86400,2)
            unit = 'd'

        # round the result to one decimal place
        percent = round(float(downloaded_bytes / total_bytes * 100),1)

        # update the result lable wiht progress percentage
        result.configure(text = f'Downloading ... {percent}% , ETA: {estimated_time}{unit}', fg_color="transparent")
        result.update()

# download video function, it won't download the video unless the user select a path and a quality
def DownloadVideo():
    try:
        # enable access to the path variable
        global path

        # get the quality value
        quality_value = quality_list.get()

        # restore the default value
        result.configure(text = "", fg_color = "transparent")
        result.update()
        
        # check if the user select a valid path 
        if path == "":
            result.configure(text="Please select a path", fg_color="red")
            result.update()
            return
        
        #  check if the user select a valid quality
        if quality_value == "choose quality":
            result.configure(text="Please select a quality", fg_color="red")
            result.update()
            return

        ytLink = link_field.get()

        # Set the download options
        ydl_opts = {
            'format' : f'bestvideo[height <={quality_value}p]+bestaudio/best',
            'outtmpl' : str(path) + '/' + '%(title)s.%(ext)s',
            'progress_hooks': [my_hook],
            
        }
        
        # Create the downloader
        ydl = yt_dlp.YoutubeDL(ydl_opts)

        # Download the video
        ydl.download([ytLink])

    except:
        result.configure(text="Invalid link", fg_color="red")
        result.update()
        return
    
    # output operation success
    result.configure(text="Downloaded", fg_color="green")
    result.update()

# download audio function, it won't download the audio unless the user select a path
def DownloadAudio():
    try:
        # enable access to the path variable
        global path

        # restore the default value
        result.configure(text = "", fg_color = "transparent")
        result.update()

        # check if the user select a valid path
        if path == "":
            result.configure(text="Please select a path", fg_color="red")
            return
        
        ytLink = link_field.get()

        # Set the download options
        ydl_opts = {
            'outtmpl' : str(path) + '/' + '%(title)s.%(ext)s',
            'format' : 'm4a/bestaudio/best',
            'progress_hooks': [my_hook]
        }

        # Create the downloader
        ydl = yt_dlp.YoutubeDL(ydl_opts)

        # Download the video
        ydl.download([ytLink])
    except:
        result.configure(text="Invalid link", fg_color="red")
        result.update()
        return
    
    # output operation success
    result.configure(text="Downloaded", fg_color="green")
    result.update()
    
# set appearance 
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# set application window 
window = customtkinter.CTk()
window.geometry("650x300")
window.resizable(False,False)
window.title("YouTube Downloader")

# set bottom frame
frame = customtkinter.CTkFrame(master= window, width=650, height=120, corner_radius=5)
frame.pack(padx = 10, pady=10, fill = "both", expand = True)
frame.place(relx=0.5, y=295, anchor="center")

# set title
title = customtkinter.CTkLabel(window, text="YouTube Downloader", text_color="white")
title.pack(padx = 10, pady=10)
title.place(x = 20, y = 10)
title.configure(font = ("Arial", 20, "bold"))

# set title bar
title_bar = customtkinter.CTkProgressBar(window, width=150, height= 6, progress_color="white")
title_bar.pack(padx = 10, pady=10)
title_bar.set(0.6)
title_bar.place(x = 20, y = 40)

# set link field 
URL = tkinter.StringVar()
URL.set("Enter YouTube link here")
link_field = customtkinter.CTkEntry(window, width=400, height=35, textvariable=URL)
link_field.pack(padx = 10, pady=10)
link_field.place(x = 20, y= 70)

# set result label
result = customtkinter.CTkLabel(window, text= "", text_color= "white", height= 25, corner_radius= 1000000, font= ("Arial", 13, "bold"), fg_color = "transparent" )
result.pack(padx = 10, pady=10)
result.place(relx=0.5, y= 200, anchor="center")

# set reload button
reload_icon = customtkinter.CTkImage(Image.open("Icons\icons8-refresh-96.png"), size=(30,30))
reload = customtkinter.CTkButton(window, text="",width=5 ,command=getQuality, image=reload_icon, fg_color = "transparent",hover_color= "dark")
reload.pack(padx = 10, pady=10)
reload.place(x = 310, y=110)

# set  quality list
optionbox_var = customtkinter.StringVar(value="choose quality")
quality_list = customtkinter.CTkComboBox(window,variable=optionbox_var ,values=available_qualities, state="readonly")
quality_list.pack(padx = 10, pady=10)
quality_list.place(x = 170, y = 115)

# set download video button
download_video_button = customtkinter.CTkButton(window, text="Download Video",font = ("Arial", 13, "bold"),text_color="white" ,corner_radius= 20 ,command=DownloadVideo)
download_video_button .pack(padx = 10, pady=10)
download_video_button .place(x = 20, y = 115)

# set download audio button
download_audio_button = customtkinter.CTkButton(window, text= "Save as Audio only",font= ("Arial", 13, "underline" ,"bold"), fg_color = "transparent", hover_color= "dark", text_color= "white" ,corner_radius= 20 ,command=DownloadAudio)
download_audio_button.pack(padx = 10, pady=10)
download_audio_button.place(x = 13, y = 145)

# set save button
save_button = customtkinter.CTkButton(window, text= "Save To:",font= ("Arial", 13 ,"bold"), text_color= "white" ,width=5, height=25, border_spacing=5, command=SetFilePath) 
save_button.pack(padx = 10, pady=10)
save_button.place(x = 440, y = 73)

# Run program
window.mainloop()