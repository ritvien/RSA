import tkinter as tk
from tkinter import * 
from tkinter import messagebox
import src
import time


def show_custom_message(message):
    dialog = tk.Toplevel(root)
    dialog.title("Thông báo")
    
    label = tk.Label(dialog, text="Khóa bí mật (d,n) là:", font=('Arial', 10))
    label.pack(pady=10)
    
    text_box = tk.Text(dialog, wrap='word', height=5, width=50)
    text_box.pack(padx=10, pady=10)
    text_box.insert('1.0', message)
    text_box.config(state='disabled')  
    
    close_button = tk.Button(dialog, text="Đóng", command=dialog.destroy)
    close_button.pack(pady=10)

def display_get_input():
    try:
        num = int(entry_N.get())
        large_prime_number = src.generate_large_prime(num)
        large_prime_number_label = tk.Label(root,
                                            text=f"Số nguyên tố lớn hơn {num} là: {large_prime_number}",
                                            fg='green',
                                            font=('Arial', 10),
                                            wraplength=200)
        large_prime_number_label.place(x=25,y=200,anchor='nw')
        entry_N.config(state='disabled')
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập một số nguyên hợp lệ")
        
def display_gen_key():
    global public_key, private_key,public_key_label,time_gen_key
    try:
        bit_size = int(entry_bitlength_key.get())
        if bit_size < 8 or bit_size > 2048:
            raise ValueError()
        start_time = time.time()
        public_key,private_key = src.generate_rsa_keys(bit_size)
        end_time = time.time()
        time_gen_key = end_time - start_time
        public_key_label = tk.Label(root,
                                    text=f"Khóa công khai (e,n) là: {public_key}",
                                    fg='green',
                                    font=('Arial', 8),
                                    wraplength=350)
        public_key_label.place(x=400,y=225,anchor='nw')
        show_custom_message(f"{private_key}, hãy copy hoặc ghi nhớ lại và không chia sẻ cho bất kỳ ai!!!!")

        entry_bitlength_key.config(state='disabled')
        button_start_encode.config(state='disabled')
        button_encrypt.place(x=600,y=195, anchor='nw')
        time_gen_key_label = tk.Label(root,text=f'Thời gian tạo khóa là: {time_gen_key}(s)',bg="#f7b681")
        time_gen_key_label.place(x=75,y=300,anchor='nw')
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập một số nguyên hợp lệ trong đoạn từ 8 đến 2048.")
        
def display_get_num_to_encode():
    global num_to_encode
    try:
        num_to_encode = int(entry_num_to_encode.get())
        check_num_label.place(x=650,y=130,anchor='nw')
        entry_num_to_encode.config(state='disabled')
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập một số nguyên hợp lệ")
        
def display_start_encrypt():
    global num_to_encode,number_encoded,public_key,time_encrypt
    try:
        if num_to_encode == None:
            raise ValueError()
        public_key_label.place(x=1000,y=1000,anchor='nw')
        start_time = time.time()
        number_encoded = src.encrypt(num_to_encode,public_key)
        end_time = time.time()
        time_encrypt = end_time - start_time
        number_encoded_label = tk.Label(root,
                                text=f"Số {num_to_encode} sau khi mã hóa là: {number_encoded}",
                                fg='green',
                                font=('Arial', 10),
                                wraplength=350)
        number_encoded_label.place(x=400,y=225,anchor='nw')
        time_encrypt_label = tk.Label(root,text=f'Thời gian mã hóa là: {time_encrypt}(s)',bg="#f7b681")
        time_encrypt_label.place(x=75,y=330,anchor='nw')
        start_decrypt_btn.place(x=400,y=500,anchor='nw')
    except ValueError:
        messagebox.showerror("Lỗi", "Lỗi nhập số cần mã hóa!")
        
def display_button_check_interger(type_key,position_y,entry,entry_str):
    global d_number_private,n_number_private
    try:
        num_entry = int(entry_str)
        check_num_label = tk.Label(root,
                                   text=f"Số {type_key} thỏa mãn ✅",
                                   fg='green',
                                   font=('Arial', 8))
        check_num_label.place(x=400,y=position_y, anchor='nw')
        entry.config(state='disable')
        if type_key == 'd':
            d_number_private = num_entry
            d_private_key_button.config(state='disable')
            click_n_to_start_decrypt.place(x=670,y=500,anchor='nw')
        else:
            n_number_private = num_entry
            if d_number_private == None:
                type_key = 'd'
                raise ValueError()
            if (d_number_private != None) or (n_number_private != None):
                decrypt_btn.place(x=670,y=555,anchor='nw')
    except ValueError:
        messagebox.showerror("Lỗi", f"Lỗi nhập số  {type_key}")

def display_decrypt():
    global number_encoded, private_key,d_number_private,n_number_private,time_decrypt
    decrypt_btn.config(state='disable')
    start_time = time.time()
    number_decrypted = src.decrypt(number_encoded,(d_number_private,n_number_private))
    end_time = time.time()
    time_decrypt = end_time - start_time
    number_truth_decryted = src.decrypt(number_encoded,private_key)      
    number_decrypted_label = tk.Label(root,
                            text=f"Số sau khi giải mã là: {number_decrypted}",
                            fg='red',
                            font=('Arial', 8),
                            wraplength=350)
    number_decrypted_label.place(x=100,y=560,anchor='nw')
    if number_decrypted != number_truth_decryted:
        false_decrypted_label = tk.Label(root,
                            text=f"Có vẻ bạn đã nhập sai khóa bí mật!!",
                            fg='red',
                            font=('Arial', 8),
                            wraplength=350)
        false_decrypted_label.place(x=100,y=540,anchor='nw')
        close_button.place(x=100,y=500,anchor='nw')
    else:
        true_decrypted_label = tk.Label(root,
                            text=f"Khóa khớp, giải mã thành công",
                            fg='red',
                            font=('Arial', 8),
                            wraplength=350)
        true_decrypted_label.place(x=100,y=540,anchor='nw')
        time_decrypt_label = tk.Label(root,text=f'Thời gian giải mã là: {time_decrypt}(s)',bg="#f7b681")
        time_decrypt_label.place(x=75,y=360,anchor='nw')
        close_button.place(x=100,y=500,anchor='nw')

        
def display_entry_private_key():
    global number_encoded,private_key
    start_decrypt_btn.config(state='disabled')
    entry_private_key_label.place(x=500,y=500, anchor='nw')
    
    d_private_key_entry.place(x=400, y=530, anchor='nw')
    n_private_key_entry.place(x=400, y=555, anchor='nw')
    

    d_private_key_button.place(x=600,y=530, anchor='nw')
    n_private_key_button.place(x=600,y=555, anchor='nw')

root = Tk()
root.title("Chương trình sinh số nguyên tố lớn vã mã hóa RSA")
root.geometry('800x600')
root.resizable(0,0)

root.configure(bg='light blue')

hust_label = tk.Label(root, text="ĐẠI HỌC BÁCH KHOA HÀ NỘI", fg='red',font=('Arial', 10))
hust_label.place(x=400,y=10, anchor='center')



#_______________________________________________SINH SỐ NGUYÊN TỐ_____________________________________________#

p_number_label = tk.Label(root, text="SINH SỐ NGUYÊN TỐ", fg='black',bg='#05ff16',font=('Arial', 10))
p_number_label.place(x=150,y=75, anchor='center')

label_input_N = tk.Label(root, text="Hãy nhập một số nguyên N:",bg='sky blue')
label_input_N.place(x=25,y=100, anchor='nw')

entry_N = tk.Entry(root,width=30)
entry_N.place(x=25, y=130, anchor='nw')

button_get_N = tk.Button(root, text="Sinh số nguyên tố lớn hơn N", command=display_get_input,activebackground='red')
button_get_N.place(x=25,y=160, anchor='nw')


#__________________________________________________MÃ HÓA RSA__________________________________________________#

# Nhập số cần mã hóa

num_to_encode = None
number_encoded = None

rsa_label = tk.Label(root, text="MÃ HÓA RSA", fg='black',bg='#05ff16',font=('Arial', 10))
rsa_label.place(x=600,y=75, anchor='center')

label_input_num_to_encode = tk.Label(root, text="Hãy số cần mã hóa:",bg='sky blue')
label_input_num_to_encode.place(x=400,y=100, anchor='nw')

entry_num_to_encode = tk.Entry(root,width=30)
entry_num_to_encode.place(x=530, y=100, anchor='nw')

button_start_encode = tk.Button(root, text="Bắt đầu mã hóa",command=display_get_num_to_encode,activebackground='red')
button_start_encode.place(x=530,y=130, anchor='nw')

# Sinh khóa

public_key = None
private_key = None
public_key_label = None
time_gen_key = None

label_input_bitlength_key = tk.Label(root, text="Hãy độ dài khóa (bit):",bg='sky blue')
label_input_bitlength_key.place(x=400,y=160, anchor='nw')

entry_bitlength_key = tk.Entry(root,width=10)
entry_bitlength_key.place(x=530, y=160, anchor='nw')

label_rcm_bitlength = tk.Label(root, text="Độ dài bit của khóa nên trong khoảng:[8,2048]",bg='yellow',wraplength=150)
label_rcm_bitlength.place(x=600,y=155, anchor='nw')

button_start_encode = tk.Button(root, text="Sinh khóa",command=display_gen_key,activebackground='red')
button_start_encode.place(x=530,y=195, anchor='nw')



#____________________________________________ Mã hóa__________________________________________#

time_encrypt = None

button_encrypt = tk.Button(root,
                           text="Mã hóa bằng cặp khóa dưới đây",
                           bg='#ff8a05',
                           command=display_start_encrypt,
                           activebackground='green')
check_num_label = tk.Label(root,
                           text=f"Số đã thỏa mãn ✅",
                           fg='green',
                           font=('Arial', 10))


#____________________________________________ Giải mã__________________________________________#
d_number_private = None
n_number_private = None
time_decrypt = None

start_decrypt_btn = tk.Button(root,text="Bắt đầu giải mã",fg='black',command=display_entry_private_key)
entry_private_key_label = tk.Label(root, text="Nhập khóa bí mật (d và n):", fg='black',font=('Arial', 10))
d_private_key_entry = tk.Entry(root,width=30)
n_private_key_entry = tk.Entry(root,width=30)


d_private_key_button = tk.Button(root,
                                 text="Nhập d",
                                 command=lambda: display_button_check_interger('d',530,d_private_key_entry,
                                                                               d_private_key_entry.get()),
                                 activebackground='red')
n_private_key_button = tk.Button(root,
                             text="Nhập n",
                             command=lambda: display_button_check_interger('n',555,n_private_key_entry,
                                                                           n_private_key_entry.get()),
                             activebackground='red')


click_n_to_start_decrypt = tk.Label(root,text="Click nhập n để hoàn tất nhập khóa",wraplength=100)

decrypt_btn = tk.Button(root,text="Giải mã 👈 ",fg='black',bg='#ff8a05',command=display_decrypt)
close_button = tk.Button(root, text="Để đảm bảo an toàn, Click để đóng chương trình", command=root.destroy,wraplength=200)
