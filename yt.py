import tkinter as tk
from tkinter import filedialog, ttk
import subprocess
import os
import threading
from PIL import Image, ImageTk

def browse_input():
    filename = filedialog.askopenfilename()
    entry_input.delete(0, tk.END)
    entry_input.insert(tk.END, filename)

def display_output_image():
    output_image = os.path.splitext(entry_input.get())[0] + "_w.png"
    try:
        image = Image.open(output_image)
        image.thumbnail((250, 250))  # 缩放图像尺寸以适应预览
        photo = ImageTk.PhotoImage(image)
        label_output_preview.config(image=photo)
        label_output_preview.image = photo  # 保留对图像的引用，否则图像可能无法显示
    except Exception as e:
        print(e)
        label_output_preview.config(text="无法显示预览")

def run_realesrgan():
    def run_command():
        input_image = entry_input.get()
        output_image = os.path.splitext(input_image)[0] + "_w.png"
        model = var.get()
        
        command = f"realesrgan-ncnn-vulkan.exe -i {input_image} -o {output_image} -n {model} -s 4"
        
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        for line in process.stdout:
            output_text.insert(tk.END, line)
            output_text.see(tk.END)
            output_text.update_idletasks()
    
        process.wait()
        output_text.insert(tk.END, "\n进程执行完毕！\n")
        display_output_image()  # 显示输出图片的预览
    
    threading.Thread(target=run_command).start()

root = tk.Tk()
root.title("图片放大功能")

# 创建布局和部件
button_browse_input = tk.Button(root, text="选择输入图片", command=browse_input)
button_browse_input.grid(row=0, column=0, padx=10, pady=5)

entry_input = tk.Entry(root, width=50)
entry_input.grid(row=0, column=1)

label_model = tk.Label(root, text="选择模型:")
label_model.grid(row=1, column=0)

var = tk.StringVar()
var.set("realesrgan-x4plus")

model_options = ["realesrgan-x4plus", "realesrnet-x4plus", "realesrgan-x4plus-anime", "realesr-animevideov3"]
model_dropdown = ttk.Combobox(root, textvariable=var, values=model_options, state="readonly")
model_dropdown.grid(row=1, column=1, padx=10, pady=5)

run_button = tk.Button(root, text="运行", command=run_realesrgan)
run_button.grid(row=3, column=0)

label_output_preview = tk.Label(root)
label_output_preview.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

output_text = tk.Text(root, height=20, width=70)
output_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
