import tkinter as tk
from tkinter import messagebox
from generator import generate_replies
import json
import os
import threading


class ReplyWriterProGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoForge Reply Writer Pro")
        self.root.configure(bg="#0f172a")
        self.root.state("zoomed")

        self.reply_cards = []
        self.build_ui()

    def save_api_key(self, key):
        with open("user_config.json", "w", encoding="utf-8") as f:
            json.dump({"api_key": key}, f)

    def load_api_key(self):
        if os.path.exists("user_config.json"):
            with open("user_config.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("api_key", "")
        return ""

    def paste_text(self, widget):
        try:
            widget.insert(tk.INSERT, self.root.clipboard_get())
        except Exception:
            pass

    def copy_text(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Copied", "Reply copied to clipboard.")

    def copy_all_replies(self):
        if not self.reply_cards:
            messagebox.showwarning("No Replies", "Generate replies first.")
            return

        all_text = []
        for i, reply in enumerate(self.reply_cards, start=1):
            all_text.append(f"Reply {i}:\n{reply}\n")

        final_text = "\n".join(all_text)
        self.root.clipboard_clear()
        self.root.clipboard_append(final_text)
        messagebox.showinfo("Copied", "All replies copied.")

    def export_replies(self):
        if not self.reply_cards:
            messagebox.showwarning("No Replies", "Generate replies first.")
            return

        all_text = []
        for i, reply in enumerate(self.reply_cards, start=1):
            all_text.append(f"Reply {i}:\n{reply}\n")

        final_text = "\n".join(all_text)

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, "reply_output.txt")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_text)

        messagebox.showinfo("Exported", f"Saved to {filepath}")

    def clear_all(self):
        self.message_box.delete("1.0", tk.END)
        self.clear_reply_cards()
        self.status_label.config(text="Ready")

    def clear_reply_cards(self):
        self.reply_cards = []
        for widget in self.output_frame.winfo_children():
            widget.destroy()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="AutoForge Reply Writer Pro",
            font=("Segoe UI", 30, "bold"),
            bg="#0f172a",
            fg="white"
        )
        title.pack(pady=(20, 8))

        subtitle = tk.Label(
            self.root,
            text="Turn comments and messages into smart replies instantly",
            font=("Segoe UI", 13),
            bg="#0f172a",
            fg="#94a3b8"
        )
        subtitle.pack(pady=(0, 18))

        api_label = tk.Label(
            self.root,
            text="Enter your OpenAI API Key:",
            font=("Segoe UI", 12, "bold"),
            bg="#0f172a",
            fg="white"
        )
        api_label.pack()

        self.api_entry = tk.Entry(
            self.root,
            font=("Segoe UI", 12),
            width=80,
            show="*",
            justify="center"
        )
        self.api_entry.pack(pady=(6, 14), ipady=8)

        saved_key = self.load_api_key()
        if saved_key:
            self.api_entry.insert(0, saved_key)

        controls = tk.Frame(self.root, bg="#0f172a")
        controls.pack(pady=(0, 12))

        tone_label = tk.Label(
            controls,
            text="Tone:",
            font=("Segoe UI", 12, "bold"),
            bg="#0f172a",
            fg="white"
        )
        tone_label.grid(row=0, column=0, padx=(0, 8))

        self.tone_var = tk.StringVar(value="Professional")
        tone_menu = tk.OptionMenu(
            controls,
            self.tone_var,
            "Professional",
            "Casual",
            "Friendly",
            "Persuasive"
        )
        tone_menu.config(font=("Segoe UI", 11), bg="white", width=12)
        tone_menu.grid(row=0, column=1, padx=(0, 20))

        platform_label = tk.Label(
            controls,
            text="Platform:",
            font=("Segoe UI", 12, "bold"),
            bg="#0f172a",
            fg="white"
        )
        platform_label.grid(row=0, column=2, padx=(0, 8))

        self.platform_var = tk.StringVar(value="General")
        platform_menu = tk.OptionMenu(
            controls,
            self.platform_var,
            "General",
            "TikTok",
            "Reddit",
            "X / Twitter",
            "Email",
            "DM"
        )
        platform_menu.config(font=("Segoe UI", 11), bg="white", width=12)
        platform_menu.grid(row=0, column=3)

        message_label = tk.Label(
            self.root,
            text="Paste comment / message:",
            font=("Segoe UI", 12, "bold"),
            bg="#0f172a",
            fg="white"
        )
        message_label.pack()

        self.message_box = tk.Text(
            self.root,
            font=("Segoe UI", 12),
            width=95,
            height=7,
            wrap="word",
            bg="white",
            fg="black",
            relief="flat",
            bd=0
        )
        self.message_box.pack(pady=(6, 14))

        button_frame = tk.Frame(self.root, bg="#0f172a")
        button_frame.pack(pady=(0, 16))

        self.generate_button = tk.Button(
            button_frame,
            text="Generate Replies",
            font=("Segoe UI", 12, "bold"),
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            activeforeground="white",
            width=18,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.on_generate
        )
        self.generate_button.grid(row=0, column=0, padx=8, ipady=8)

        self.regenerate_button = tk.Button(
            button_frame,
            text="Regenerate",
            font=("Segoe UI", 12, "bold"),
            bg="#f59e0b",
            fg="white",
            activebackground="#d97706",
            activeforeground="white",
            width=12,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.on_generate
        )
        self.regenerate_button.grid(row=0, column=1, padx=8, ipady=8)

        clear_button = tk.Button(
            button_frame,
            text="Clear",
            font=("Segoe UI", 12, "bold"),
            bg="#ef4444",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            width=10,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.clear_all
        )
        clear_button.grid(row=0, column=2, padx=8, ipady=8)

        copy_all_button = tk.Button(
            button_frame,
            text="Copy All",
            font=("Segoe UI", 12, "bold"),
            bg="#6366f1",
            fg="white",
            activebackground="#4f46e5",
            activeforeground="white",
            width=12,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.copy_all_replies
        )
        copy_all_button.grid(row=0, column=3, padx=8, ipady=8)

        export_button = tk.Button(
            button_frame,
            text="Export TXT",
            font=("Segoe UI", 12, "bold"),
            bg="#06b6d4",
            fg="white",
            activebackground="#0891b2",
            activeforeground="white",
            width=12,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.export_replies
        )
        export_button.grid(row=0, column=4, padx=8, ipady=8)

        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Segoe UI", 11),
            bg="#0f172a",
            fg="#94a3b8"
        )
        self.status_label.pack(pady=(0, 10))

        container = tk.Frame(self.root, bg="#0f172a")
        container.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        self.canvas = tk.Canvas(container, bg="#0f172a", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)

        self.output_frame = tk.Frame(self.canvas, bg="#0f172a")

        self.output_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.output_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.api_entry.bind("<Control-v>", lambda e: self.paste_text(self.api_entry))
        self.api_entry.bind("<Button-3>", lambda e: self.paste_text(self.api_entry))
        self.message_box.bind("<Control-v>", lambda e: self.paste_text(self.message_box))
        self.message_box.bind("<Button-3>", lambda e: self.paste_text(self.message_box))

    def on_generate(self):
        api_key = self.api_entry.get().strip()
        message = self.message_box.get("1.0", tk.END).strip()

        if not api_key:
            messagebox.showerror("Missing API Key", "Enter your OpenAI API key.")
            return

        if not message:
            messagebox.showerror("Missing Input", "Paste a message first.")
            return

        self.save_api_key(api_key)
        self.generate_button.config(state="disabled", text="Generating...")
        self.regenerate_button.config(state="disabled")
        self.status_label.config(text="Generating replies...")
        self.clear_reply_cards()

        thread = threading.Thread(
            target=self._generate_replies_thread,
            args=(message, api_key, self.tone_var.get(), self.platform_var.get()),
            daemon=True
        )
        thread.start()

    def _generate_replies_thread(self, message, api_key, tone, platform):
        try:
            result = generate_replies(message, api_key, tone, platform)
            self.root.after(0, lambda: self.display_replies(result["raw"]))
            self.root.after(0, lambda: self.status_label.config(text="Replies generated successfully."))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Generation Error", str(e)))
            self.root.after(0, lambda: self.status_label.config(text="Generation failed."))
        finally:
            self.root.after(0, lambda: self.generate_button.config(state="normal", text="Generate Replies"))
            self.root.after(0, lambda: self.regenerate_button.config(state="normal"))

    def display_replies(self, raw_text):
        self.clear_reply_cards()

        sections = raw_text.split("REPLY OPTION")
        replies = []

        for section in sections:
            section = section.strip()
            if not section:
                continue

            if ":" in section:
                _, reply_text = section.split(":", 1)
                reply_text = reply_text.strip()
                if reply_text:
                    replies.append(reply_text)

        if not replies:
            replies = [raw_text.strip()]

        for index, reply in enumerate(replies, start=1):
            self.reply_cards.append(reply)

            card = tk.Frame(self.output_frame, bg="white", bd=0, relief="flat")
            card.pack(fill="x", pady=8, padx=8)

            header = tk.Frame(card, bg="#e5e7eb")
            header.pack(fill="x")

            title = tk.Label(
                header,
                text=f"Reply Option {index}",
                font=("Segoe UI", 12, "bold"),
                bg="#e5e7eb",
                fg="#111827"
            )
            title.pack(side="left", padx=12, pady=10)

            copy_btn = tk.Button(
                header,
                text="Copy",
                font=("Segoe UI", 10, "bold"),
                bg="#3b82f6",
                fg="white",
                activebackground="#2563eb",
                activeforeground="white",
                width=8,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda t=reply: self.copy_text(t)
            )
            copy_btn.pack(side="right", padx=12, pady=8)

            body = tk.Label(
                card,
                text=reply,
                justify="left",
                anchor="w",
                wraplength=1200,
                bg="white",
                fg="black",
                font=("Segoe UI", 12)
            )
            body.pack(fill="x", padx=14, pady=14)