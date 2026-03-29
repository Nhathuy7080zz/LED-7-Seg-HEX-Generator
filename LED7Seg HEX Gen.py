import tkinter as tk

# Bảng mã K chung (Common Cathode) - mức 1 sáng
KC_MAP = {
    '0': 0x3F, '1': 0x06, '2': 0x5B, '3': 0x4F, '4': 0x66,
    '5': 0x6D, '6': 0x7D, '7': 0x07, '8': 0x7F, '9': 0x6F,
    'A': 0x77, 'a': 0x5F, 'B': 0x7F, 'b': 0x7C, 'C': 0x39, 'c': 0x58,
    'D': 0x3F, 'd': 0x5E, 'E': 0x79, 'e': 0x7B, 'F': 0x71, 'f': 0x71,
    'G': 0x3D, 'g': 0x6F, 'H': 0x76, 'h': 0x74, 'I': 0x06, 'i': 0x04,
    'J': 0x1E, 'j': 0x1E, 'K': 0x7A, 'k': 0x70, 'L': 0x38, 'l': 0x30,
    'M': 0x55, 'm': 0x15, 'N': 0x37, 'n': 0x54, 'O': 0x3F, 'o': 0x5C,
    'P': 0x73, 'p': 0x73, 'Q': 0x67, 'q': 0x67, 'R': 0x77, 'r': 0x50,
    'S': 0x6D, 's': 0x6D, 'T': 0x31, 't': 0x78, 'U': 0x3E, 'u': 0x1C,
    'V': 0x3E, 'v': 0x1C, 'W': 0x7E, 'w': 0x2A, 'X': 0x76, 'x': 0x76,
    'Y': 0x6E, 'y': 0x6E, 'Z': 0x5B, 'z': 0x5B,
    ' ': 0x00, '-': 0x40, '_': 0x08, '=': 0x48, '"': 0x22, "'": 0x20,
    '[': 0x39, ']': 0x0F, '^': 0x23, '*': 0x63, '.': 0x80
}

# Bảng mã A chung (Common Anode) - mức 0 sáng (đảo bit của K chung)
AC_MAP = {k: (~v & 0xFF) for k, v in KC_MAP.items()}

def convert():
    inp = entry_input.get()
    led_count_val = var_led_count.get()
    
    if led_count_val != "Mặc định":
        num_leds = int(led_count_val)
        inp = inp[:num_leds].ljust(num_leds, ' ')
        if entry_input.get() != inp:
            entry_input.delete(0, tk.END)
            entry_input.insert(0, inp)
            
    if not inp:
        text_output.delete("1.0", tk.END)
        return
        
    is_K_chung = var_type.get() == "K"
    bit_choice = var_bit.get() # 3 hoặc 4
    
    mapping = KC_MAP if is_K_chung else AC_MAP
    
    out_list = []
    for char in inp:
        if char in mapping:
            val = mapping[char]
            if bit_choice == 3:
                # VD: 03FH (3 ký tự hex)
                out_str = f"{val:03X}H"
            else:
                # VD: 003FH (4 ký tự hex)
                out_str = f"{val:04X}H"
            out_list.append(out_str)
        else:
            out_list.append("?")
            
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, ", ".join(out_list))

def shift_left():
    inp = entry_input.get()
    if not inp: return
    new_inp = inp[1:] + " "
    entry_input.delete(0, tk.END)
    entry_input.insert(0, new_inp)
    convert()

def shift_right():
    inp = entry_input.get()
    if not inp: return
    new_inp = " " + inp[:-1]
    entry_input.delete(0, tk.END)
    entry_input.insert(0, new_inp)
    convert()

app = tk.Tk()
app.title("LED-7-Seg HEX Generator")
app.geometry("500x450")
app.resizable(False, False)

# Input
tk.Label(app, text="Nhập dãy số:", font=("Tahoma", 10)).pack(pady=5)
entry_input = tk.Entry(app, font=("Tahoma", 12), justify="center")
entry_input.pack(pady=5, ipadx=10, ipady=3)

# Loại LED
var_type = tk.StringVar(value="K")
frame_type = tk.Frame(app)
frame_type.pack(pady=5)
tk.Radiobutton(frame_type, text="K chung", variable=var_type, value="K", font=("Tahoma", 10)).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(frame_type, text="A chung", variable=var_type, value="A", font=("Tahoma", 10)).pack(side=tk.LEFT, padx=10)

# Chọn 3 bit / 4 bit (Format chữ số hiển thị mã HEX)
var_bit = tk.IntVar(value=3)
frame_bit = tk.Frame(app)
frame_bit.pack(pady=5)
tk.Radiobutton(frame_bit, text="3 bit", variable=var_bit, value=3, font=("Tahoma", 10)).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(frame_bit, text="4 bit", variable=var_bit, value=4, font=("Tahoma", 10)).pack(side=tk.LEFT, padx=10)

# Chọn số lượng LED
var_led_count = tk.StringVar(value="Mặc định")
frame_led = tk.Frame(app)
frame_led.pack(pady=5)
tk.Label(frame_led, text="Số lượng chốt LED:", font=("Tahoma", 10)).pack(side=tk.LEFT)
tk.OptionMenu(frame_led, var_led_count, "Mặc định", "2", "4", "8", "16", "32").pack(side=tk.LEFT, padx=5)

# Buttons Container
frame_btn = tk.Frame(app)
frame_btn.pack(pady=10)
tk.Button(frame_btn, text="< Dịch trái", command=shift_left, font=("Tahoma", 10), cursor="hand2").pack(side=tk.LEFT, padx=5)
tk.Button(frame_btn, text="Chuyển đổi", command=convert, bg="#107C41", fg="white", font=("Tahoma", 10, "bold"), cursor="hand2").pack(side=tk.LEFT, padx=5, ipadx=10)
tk.Button(frame_btn, text="Dịch phải >", command=shift_right, font=("Tahoma", 10), cursor="hand2").pack(side=tk.LEFT, padx=5)

# Output
tk.Label(app, text="Kết quả:", font=("Tahoma", 10)).pack()
text_output = tk.Text(app, height=8, width=60, font=("Tahoma", 12))
text_output.pack(pady=5)

tk.Label(app, text="LED 7 Segment HEX Generator by Nhathuy7080zz", font=("Tahoma", 8)).pack(side=tk.BOTTOM, pady=5)

app.mainloop()
