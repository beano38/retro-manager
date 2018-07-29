
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk

code = ""


def key(event):
    global code
    """shows key or tk code for the key"""
    if event.keysym == 'Escape':
        root.destroy()
    if event.char == event.keysym:
        # normal number and letter characters
        print('Normal Key {} code {}'.format(event.char, event.keycode))
        code = event.keycode
        # root.destroy()
    elif len(event.char) == 1:
        # characters like []/.,><#$ also Return and ctrl/key
        print('Punctuation Key {} code {}'.format(event.keysym, event.keycode))
        code = event.keycode
        # root.destroy()
    else:
        # f1 to f12, shift keys, caps lock, Home, End, Delete ...
        print('Special Key {} code {}'.format(event.keysym, event.keycode))
        code = event.keycode
        # root.destroy()


root = tk.Tk()
print("Press a key (Escape key to exit):")
root.bind_all('<Key>', key)
# don't show the tk window
root.withdraw()
root.mainloop()

print("The code is: {}, char is {}".format(code, chr(code)))


