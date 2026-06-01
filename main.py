import customtkinter as ctk
from tkinter import messagebox
from generator import generate_password, evaluate_strength
from history_manager import add_to_history, get_history, clear_history, MAX_HISTORY

#Ustawienia globalne wyglądu
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PasswordGeneratorApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        #Konfiguracja okna
        self.title("Password Generator")
        self.geometry("520x750")
        self.resizable(False, False)    # blokujemy zmianę rozmiaru okna

        #Zmienne powiązane z widżetami
        self.length_var = ctk.IntVar(value=12)
        self.hard_var   = ctk.BooleanVar(value=False)

        #interfejs
        self._build_ui()


    def _build_ui(self):

        #tytuł
        ctk.CTkLabel(
            self,
            text="🔐 Password Generator",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            self,
            text="Generate secure passwords instantly",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(pady=(0, 20))

        #SEKCJA: DŁUGOŚĆ HASŁA
        length_frame = ctk.CTkFrame(self, corner_radius=12)
        length_frame.pack(padx=32, fill="x", pady=6)

        ctk.CTkLabel(
            length_frame,
            text="Password length",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=16, pady=(12, 4))

        #aktualna wartość suwaka
        self.length_label = ctk.CTkLabel(
            length_frame,
            textvariable=self.length_var,
            font=ctk.CTkFont(size=13)
        )
        self.length_label.pack(anchor="e", padx=16)

        ctk.CTkSlider(
            length_frame,
            from_=7, to=20,                 # zakres suwaka
            number_of_steps=13,             # kroki co 1
            variable=self.length_var,       # powiązany ze zmienną
        ).pack(padx=16, pady=(0, 12), fill="x")

        #SEKCJA: TRYB TRUDNOŚCI
        mode_frame = ctk.CTkFrame(self, corner_radius=12)
        mode_frame.pack(padx=32, fill="x", pady=6)

        ctk.CTkLabel(
            mode_frame,
            text="Difficulty mode",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=16, pady=(12, 8))

        ctk.CTkRadioButton(
            mode_frame,
            text="Easy  (letters + digits)",
            variable=self.hard_var,
            value=False
        ).pack(anchor="w", padx=24, pady=2)

        ctk.CTkRadioButton(
            mode_frame,
            text="Hard  (letters + digits + symbols: !@#$%^&*_+-=?)",
            variable=self.hard_var,
            value=True
        ).pack(anchor="w", padx=24, pady=(2, 12))

        #SEKCJA: WYGENEROWANE HASŁO
        pass_frame = ctk.CTkFrame(self, corner_radius=12)
        pass_frame.pack(padx=32, fill="x", pady=6)

        ctk.CTkLabel(
            pass_frame,
            text="Generated password",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=16, pady=(12, 6))

        # Pole wyświetlające hasło
        self.password_entry = ctk.CTkEntry(
            pass_frame,
            font=ctk.CTkFont(size=15, family="Courier"),
            height=42,
            justify="center",
            state="readonly"
        )
        self.password_entry.pack(padx=16, fill="x")

        # Pasek siły hasła
        self.strength_bar = ctk.CTkProgressBar(pass_frame, height=8)
        self.strength_bar.set(0)
        self.strength_bar.pack(padx=16, pady=(8, 4), fill="x")

        # Etykieta z oceną słowną (Easy / Medium / Hard)
        self.strength_label = ctk.CTkLabel(
            pass_frame,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.strength_label.pack(pady=(0, 12))

        #PRZYCISKI AKCJI
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(padx=32, fill="x", pady=10)

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        ctk.CTkButton(
            btn_frame,
            text="⚡ Generate",
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._on_generate
        ).grid(row=0, column=0, padx=(0, 6), sticky="ew")

        ctk.CTkButton(
            btn_frame,
            text="📋 Copy",
            height=42,
            font=ctk.CTkFont(size=14),
            fg_color="#2d6a4f",
            hover_color="#1b4332",
            command=self._on_copy
        ).grid(row=0, column=1, padx=(6, 0), sticky="ew")

#SEKCJA: HISTORIA
        history_header = ctk.CTkFrame(self, fg_color="transparent")
        history_header.pack(padx=32, fill="x", pady=(14, 0))
        history_header.columnconfigure(0, weight=1)
        history_header.columnconfigure(1, weight=0)

        ctk.CTkLabel(
            history_header,
            text="History",
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            history_header,
            text="Clear",
            width=60,
            height=26,
            font=ctk.CTkFont(size=12),
            fg_color="#555",
            hover_color="#333",
            command=self._on_clear_history
        ).grid(row=0, column=1, sticky="e")

        self.history_frame = ctk.CTkScrollableFrame(self, corner_radius=12, height=150)
        self.history_frame.pack(padx=32, fill="x", pady=(6, 20))

        self.history_rows = []
        for i in range(MAX_HISTORY):
            row = ctk.CTkLabel(
                self.history_frame,
                text="",
                font=ctk.CTkFont(size=12, family="Courier"),
                anchor="w",
                text_color="gray"
            )
            row.pack(anchor="w", padx=16, pady=2)
            self.history_rows.append(row)

        self._refresh_history()

    #OBSŁUGA ZDARZEŃ

    def _on_generate(self):

        length = self.length_var.get()   # pobieramy wartość suwaka
        hard   = self.hard_var.get()     # pobieramy tryb trudności

        password, error = generate_password(length, hard)

        if error:
            messagebox.showerror("Error", error)
            return

        self.password_entry.configure(state="normal")
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)
        self.password_entry.configure(state="readonly")

        # Aktualizacja paska siły
        strength = evaluate_strength(password)
        self.strength_bar.set(strength["value"])
        self.strength_bar.configure(progress_color=strength["color"])
        self.strength_label.configure(
            text=f"Strength: {strength['label']}",
            text_color=strength["color"]
        )

        # Zapis do historii i odświeżenie jej widoku
        add_to_history(password, hard)
        self._refresh_history()


    def _on_copy(self):

        password = self.password_entry.get()

        if not password:
            messagebox.showwarning("Warning", "Generate a password first!")
            return

        self.clipboard_clear()
        self.clipboard_append(password)
        self.update()

        messagebox.showinfo("Copied!", "Password copied to clipboard ✓")


    def _on_clear_history(self):

        if not get_history():
            return  # historia pusta

        confirm = messagebox.askyesno(
            "Clear history",
            "Are you sure you want to clear all history?"
        )
        if confirm:
            clear_history()
            self._refresh_history()


    def _refresh_history(self):

        history = get_history()

        for i, row in enumerate(self.history_rows):
            if i < len(history):
                entry = history[i]
                text = f"{entry['type']:<4}  {entry['password']}"
                row.configure(text=text, text_color="white")
            else:
                row.configure(text="–", text_color="gray")

#URUCHOMIENIE APLIKACJI
if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()          # pętla główna – utrzymuje okno otwarte