import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import openai

# Your OpenAI API key should be kept secret. Do not expose it in your code.
openai.api_key = "sk-proj-TBnmxyHJRKiI0BnLlppcT3BlbkFJi7nvzRjDokHu4eeICCKO"

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content'].strip()

def send_message(event=None):
    user_input = entry.get()
    if user_input.lower() in ["quit", "exit", "bye"]:
        root.destroy()
    else:
        # Display sending message
        add_message("You", user_input, "right")
        
        # Clear user input
        entry.delete(0, tk.END)
        
        # Delay before chatbot response
        root.after(1000, lambda: chatbot_response(user_input))

def chatbot_response(user_input):
    response = chat_with_gpt(user_input)
    add_message("Chatbot", response, "left")

def add_message(sender, message, align):
    color = "#C3E6CB" if align == "right" else "#F5F5F5"
    anchor = "e" if align == "right" else "w"
    justify = "right" if align == "right" else "left"

    message_frame = tk.Frame(text_area, bg=color)
    message_frame.pack(fill="x", padx=5, pady=5)

    # The wraplength will be set in the update_wraplength function
    label = tk.Label(message_frame, text=f"{sender}: {message}", anchor=anchor, justify=justify, bg=color, padx=10, pady=5, font=("Arial", 12), fg="#333333")
    label.pack(fill="both", padx=5, pady=5, ipadx=5, ipady=5)

    update_wraplength()

def update_wraplength(event=None):
    # Update wraplength for all messages
    for message_frame in text_area.winfo_children():
        for label in message_frame.winfo_children():
            wraplength = text_area.winfo_width() - 30  # Adjust the subtraction value as necessary
            label.config(wraplength=wraplength)

            # If the text input widget is currently packed, forget it
            if label.master == entry.winfo_parent():
                entry.pack_forget()

            # Repack the text input widget after the label
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

root = tk.Tk()
root.title("Chatbot GUI")
root.geometry("800x600")  # Set window size to 800x600

style = ttk.Style(root)
style.theme_use("clam")

frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

text_area = scrolledtext.ScrolledText(frame, width=80, height=15, font=("Helvetica", 12), spacing1=4, spacing2=4, spacing3=4, bg="#F9F9F9", wrap=tk.WORD)
text_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

# Add a vertical scrollbar to the text area
y_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=text_area.yview)
y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_area.config(yscrollcommand=y_scrollbar.set)

entry = ttk.Entry(frame, width=40, font=("Helvetica", 12))
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

send_button = ttk.Button(frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=5, pady=5)

entry.bind("<Return>", send_message)

# Bind the update_wraplength function to the root window's configure event
root.bind('<Configure>', update_wraplength)

# Bind the MouseWheel event to the text area for scrolling
text_area.bind("<MouseWheel>", lambda event: text_area.yview_scroll(int(-1*(event.delta/120)), "units"))

root.mainloop()
