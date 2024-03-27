from src_py import depins
import os
import subprocess
import threading
import fileinput
import sys

depins.install_dependencies()

from src_py import genhm
from tkinter import *
from tkinter import filedialog


def intvalfunc(P):
    if (str.isdecimal(P) and int(P) >= 0) or P == "":
        return True
    else:
        return False


def floatvalfunc(P):
    if P == "":
        return True
    try:
        x = float(P)
        if x < 0:
            return False
        return True
    except ValueError:
        return False


window = Tk()
window.geometry("1200x600")
window.config(bg="#26242f")
window.resizable(width=False, height=False)

window.title("AI enhanced voxel game engine simple settings menu")

intregister = window.register(intvalfunc)
floatregister = window.register(floatvalfunc)

lbl = Label(window, text="Screen width", bg="#26242f", fg="white")
lbl.grid(column=0, row=0)
Screenwidth = Entry(
    window, width=150, validate="all", validatecommand=(intregister, "%P")
)
Screenwidth.insert(0, "0")
Screenwidth.grid(column=1, row=0)
lbl = Label(window, text="Enter 0 for default size", bg="#26242f", fg="white")
lbl.grid(column=2, row=0)

lbl = Label(window, text="Screen height", bg="#26242f", fg="white")
lbl.grid(column=0, row=1)
Screenheight = Entry(
    window, width=150, validate="all", validatecommand=(intregister, "%P")
)
Screenheight.insert(0, "0")
Screenheight.grid(column=1, row=1)
lbl = Label(window, text="Enter 0 for default size", bg="#26242f", fg="white")
lbl.grid(column=2, row=1)

lbl = Label(window, text="Sea level", bg="#26242f", fg="white")
lbl.grid(column=0, row=2)
Sealevel = Entry(
    window, width=150, validate="all", validatecommand=(floatregister, "%P")
)
Sealevel.insert(0, "25.2")
Sealevel.grid(column=1, row=2)
lbl = Label(window, text="Enter 0 for no water", bg="#26242f", fg="white")
lbl.grid(column=2, row=2)

lbl = Label(window, text="Chunk size", bg="#26242f", fg="white")
lbl.grid(column=0, row=3)
Chunksize = Entry(
    window, width=150, validate="all", validatecommand=(intregister, "%P")
)
Chunksize.insert(0, "16")
Chunksize.grid(column=1, row=3)

lbl = Label(window, text="Chunk range", bg="#26242f", fg="white")
lbl.grid(column=0, row=4)
Chunkrange = Entry(
    window, width=150, validate="all", validatecommand=(intregister, "%P")
)
Chunkrange.insert(0, "32")
Chunkrange.grid(column=1, row=4)

lbl = Label(window, text="World size x", bg="#26242f", fg="white")
lbl.grid(column=0, row=5)
Worldsizex = Entry(
    window, width=150, validate="all", validatecommand=(intregister, "%P")
)
Worldsizex.insert(0, "2048")
Worldsizex.grid(column=1, row=5)

lbl = Label(window, text="World size z", bg="#26242f", fg="white")
lbl.grid(column=0, row=6)
Worldsizez = Entry(
    window, width=150, validate="all", validatecommand=(intregister, "%P")
)
Worldsizez.insert(0, "2048")
Worldsizez.grid(column=1, row=6)


lbl = Label(window, text="vcvarsall.bat location", bg="#26242f", fg="white")
lbl.grid(column=0, row=7)
path = Entry(window, width=150)
path.insert(
    0,
    "C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\VC\\Auxiliary\\Build\\vcvarsall.bat",
)
path.grid(column=1, row=7)


def browsefunc():
    filename = filedialog.askopenfilename(
        filetypes=(("bat files", "*.bat"), ("All files", "*.*"))
    )
    if filename.__len__() > 0:
        path.delete(0, END)
        path.insert(0, filename)


btn = Button(window, text="Browse", command=browsefunc)
btn.grid(column=2, row=7)

switch_frame = Frame()
switch_frame.grid(column=1, row=8, pady=10)
switch_variable = StringVar(value="")

lblb = Label(window, text="World creation", bg="#26242f", fg="white")
lblb.grid(column=0, row=8)

sub_frame = Frame()
ai_entry = None
seedx = None
seedz = None


def aiclick():
    global sub_frame
    global ai_entry
    global switch_variable
    if switch_variable.get() == "AI":
        return
    sub_frame.destroy()
    sub_frame = Frame()
    sub_frame.grid(column=1, row=9)
    ai_entry = Text(sub_frame, width=100, height=3)
    ai_entry.grid(column=1, row=9)
    ai_entry.insert("end-1c", "Describe your world here...")
    switch_variable = StringVar(value="AI")


aiclick()


def randclick():
    global sub_frame
    global seedx
    global seedz
    global switch_variable
    if switch_variable.get() == "Random":
        return
    sub_frame.destroy()
    sub_frame = Frame()
    sub_frame.grid(column=1, row=9)
    seedx = Entry(
        sub_frame, width=100, validate="all", validatecommand=(intregister, "%P")
    )
    seedx.grid(column=1, row=9)
    seedz = Entry(
        sub_frame, width=100, validate="all", validatecommand=(intregister, "%P")
    )
    seedz.grid(column=1, row=10)
    seedx.insert(0, "1453")
    seedz.insert(0, "1071")
    lblb = Label(sub_frame, text="Seed x", bg="#26242f", fg="white")
    lblb.grid(column=0, row=9)
    lblb = Label(sub_frame, text="Seed z", bg="#26242f", fg="white")
    lblb.grid(column=0, row=10)
    switch_variable = StringVar(value="Random")


ai_button = Radiobutton(
    switch_frame,
    text="AI",
    indicatoron=False,
    value="AI",
    width=8,
    command=aiclick,
)
random_button = Radiobutton(
    switch_frame,
    text="Random",
    indicatoron=False,
    value="Random",
    width=8,
    command=randclick,
)
ai_button.pack(side="left")
random_button.pack(side="left")
ai_button.invoke()


lblb = Label(window, text="", bg="#26242f", fg="white")
lblb.grid(column=1, row=15)


def replace(source_text, modified_text, text_filename):
    with fileinput.FileInput(text_filename, inplace=True) as file:
        for line in file:
            if source_text in line:
                line = modified_text + "\n"
            sys.stdout.write(line)


hm_generator = genhm.hm_ai(True)


def replacing_jobs():
    replace(
        "int windoww",
        "int windoww = " + Screenwidth.get() + ";",
        ".\\src\\main.c",
    )
    replace(
        "int windowh",
        "int windowh = " + Screenheight.get() + ";",
        ".\\src\\main.c",
    )
    replace(
        "float sealevel",
        "float sealevel = " + Sealevel.get() + ";",
        ".\\src\\main.c",
    )
    replace(
        "int chunk_size",
        "int chunk_size = " + Chunksize.get() + ";",
        ".\\src\\main.c",
    )
    replace(
        "int chunk_range",
        "int chunk_range = " + Chunkrange.get() + ";",
        ".\\src\\main.c",
    )
    replace(
        "int dimensionx",
        "int dimensionx = " + Worldsizex.get() + ";",
        ".\\src\\main.c",
    )
    replace(
        "int dimensionz",
        "int dimensionz = " + Worldsizez.get() + ";",
        ".\\src\\main.c",
    )
    if switch_variable.get() == "AI":
        replace(
            "unsigned char usetexture",
            "unsigned char usetexture = 1;",
            ".\\src\\main.c",
        )
        image = hm_generator.use(ai_entry.get("1.0", "end-1c"))
        if os.path.exists(".\\heightmaps\\test.jpeg"):
            add = ""
            while os.path.exists(".\\heightmaps\\test" + add + ".jpeg"):
                add = add + "_"
            os.rename(".\\heightmaps\\test.jpeg", ".\\heightmaps\\test" + add + ".jpeg")
        image = image.convert("L", colors=8)
        image.save(".\\heightmaps\\test.jpeg")
    else:
        replace(
            "unsigned char usetexture",
            "unsigned char usetexture = 0;",
            ".\\src\\main.c",
        )
        replace(
            "int seedx",
            "int seedx = " + seedx.get() + ";",
            ".\\src\\main.c",
        )
        replace(
            "int seedz",
            "int seedz = " + seedz.get() + ";",
            ".\\src\\main.c",
        )


def clicked():
    lblb.configure(text="Compiling...")
    lblb.update()
    replacing_jobs()
    try:
        os.mkdir("build")
        print("Directory 'build' created successfully")
    except FileExistsError:
        print("Directory 'build' already exists")
    os.chdir("build")
    subprocess.run("cmake ..", shell=True)
    msbuildpath = '"' + path.get() + '"'
    compile = (
        "call "
        + msbuildpath
        + " x64 & msbuild voxel_engine.sln /p:Configuration=Release /p:Platform=x64"
    )
    subprocess.run(compile, shell=True)
    os.chdir("..")
    lblb.configure(text="Running...")
    lblb.update()
    subprocess.run(".\\voxel_engine.exe", shell=True)
    lblb.configure(text="")
    lblb.update()


btn = Button(
    window, text="Compile", command=lambda: threading.Thread(target=clicked).start()
)

btn.grid(column=1, row=14, pady=10)


window.mainloop()