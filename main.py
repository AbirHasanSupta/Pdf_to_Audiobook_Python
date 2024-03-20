from tkinter import *
from tkinter import filedialog
import PyPDF2
import pyttsx3

FONT = ("Courier", 15, "bold")
BACKGROUND = "#ACE2E1"

window = Tk()
window.title("AudifyPDF")
window.config(padx=30, pady=30, background=BACKGROUND)
window.minsize(width=650, height=770)
window.resizable(width=False, height=False)


def upload_file():
    global text, filename, dl
    text = ""
    try:
        file = filedialog.askopenfilename(title="Open A PDF", initialdir="/Users/User/Downloads",
                                          filetypes=[("PDF files", "*.pdf")])
        filed = file.split("/")[-1]
        filename = filed.split(".")[0]
        reader = PyPDF2.PdfReader(file)
        for pages in reader.pages:
            text += pages.extract_text()
        try:
            dl.destroy()
        except NameError:
            pass
        label.config(text=f"File Uploaded: {filename}.pdf")
    except FileNotFoundError:
        pass


def download():
    global text, filename, dl

    try:
        if text:
            engine = pyttsx3.init()
            rate = engine.getProperty("rate")
            engine.setProperty("rate", rate - 10)

            save_path = filedialog.asksaveasfilename(
                title="Save AudioBook",
                defaultextension=".mp3",
                filetypes=[("MP3 files", "*.mp3")],
                initialfile=f"{filename}.mp3")

            if save_path:
                engine.save_to_file(text, save_path)
                engine.runAndWait()
                label.config(text="Upload a New PDF Here.")
                dl = Label(text=f"Audiobook downloaded as {filename}.mp3 ", bg=BACKGROUND, font=FONT)
                dl.grid(row=4, column=1)
                text = ""

    except NameError:
        pass


canvas = Canvas(width=600, height=400, bg="#F7EEDD", highlightthickness=0)
canvas.create_text(300, 30, text="AudifyPDF", font=("Courier", 20, "bold"), fill="#FF204E")
canvas.create_text(
        300, 370,
        text="Convert your PDF to an audiobook in one click!",
        font=FONT,
        fill="#124076"
                )
image = PhotoImage(file="theme.png")
canvas.create_image(285, 190, image=image)
canvas.grid(row=2, column=1, padx=20, pady=20)

label = Label(text="Upload Your PDF Here.", bg=BACKGROUND, font=FONT)
label.grid(row=0, column=1)

down_img = PhotoImage(file="download.png").subsample(3)
up_img = PhotoImage(file="upload.jpg").subsample(6)

upload = Button(image=up_img, command=upload_file, highlightthickness=0, bg="#A8CD9F")
upload.grid(row=1, column=1)

download_b = Button(image=down_img, command=download, highlightthickness=0, bg="#A8CD9F")
download_b.grid(row=3, column=1)


window.mainloop()
