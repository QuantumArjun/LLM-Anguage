import tkinter as tk

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App")

        # Create the chat frame
        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the chat text widget
        self.chat_text = tk.Text(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the scrollbar
        self.scrollbar = tk.Scrollbar(self.chat_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the scrollbar
        self.scrollbar.config(command=self.chat_text.yview)
        self.chat_text.config(yscrollcommand=self.scrollbar.set)

        # Start updating the chat box
        self.update_chat()

    def update_chat(self):
        # Simulated chat messages
        messages = ["Hello!", "How are you?", "I'm doing well, thank you!"]

        # Enable the chat text widget to modify its contents
        self.chat_text.config(state=tk.NORMAL)

        # Add new messages to the chat box
        for message in messages:
            self.chat_text.insert(tk.END, message + "\n")

        # Disable the chat text widget to prevent modification
        self.chat_text.config(state=tk.DISABLED)

        # Scroll to the end of the chat box
        self.chat_text.see(tk.END)

        # Schedule the next update after 1 second (1000 milliseconds)
        self.root.after(1000, self.update_chat)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()