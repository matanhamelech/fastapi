import tkinter as tk
import requests


def main():
    """
    run interactive tkinter envinroment as client
    """
    root = tk.Tk()
    canvas1 = tk.Canvas(root, width=800, height=300)
    canvas1.pack()
    global label3
    label3 = tk.Label(root, text="")
    label3.config(font=('helvetice', 14))
    label3.pack(side="left")
    entry1 = tk.Entry(root, width=80)
    canvas1.create_window(400, 200, window=entry1)
    button1 = tk.Button(text="run command",
                        command=lambda: send_command(entry1, canvas1, root))
    canvas1.create_window(400, 250, window=button1)

    label1 = tk.Label(root, text="run a command")
    label1.config(font=('helvetica', 30))
    canvas1.create_window(400, 60, window=label1)

    label2 = tk.Label(root, text="type the command here:")
    label2.config(font=('helvetica', 22))
    canvas1.create_window(400, 150, window=label2)
    root.mainloop()


def send_command(entry1, canvas1, root):
    """
    send the command the user enters to server and present output using tkinter
    :param entry1: the tkinter entry in which the user writes the command
    :param canvas1: the tkinter canvas with buttons and labels
    :param root: tkinter window
    """
    global label3
    x = entry1.get()
    if x[0:8] == "download":
        path = x
        path = path.split('/')
        filename = path[len(path) - 1]
        response = requests.put('http://127.0.0.1:8000/download/',
                                data="".join(filename))
        content = response.content.decode()
        path = x[10::]
        with open(str(path), 'w') as file:
            file.write(eval(content))
        label3['text'] = f"file downloaded successfully to {path}"


    elif x[0:6] == "upload":
        path = x[8::]
        with open(path, 'r') as file:
            content = file.read()
        x = x.split("/")
        response = requests.put('http://127.0.0.1:8000/upload/',
                                data=f"{x[len(x) - 1]},{str(content)}")
        content2 = response.content.decode()
        label3['text'] = "file uploaded successfully"


    else:
        response = requests.put('http://127.0.0.1:8000/regular/',
                                data="".join(x))
        content = response.content.decode('unicode_escape')
        content = content[1:len(content) - 1]
        label3['text'] = f"output:\n{content}"


if __name__=="__main__":
    main()
