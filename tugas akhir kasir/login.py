import tkinter as tk
from tkinter import messagebox
from db import get_db

def open_login():
    win = tk.Tk()
    win.title("Login Pegawai")
    win.geometry("400x450")
    win.configure(bg="#1e1e2e")
    win.resizable(False, False)
    
    # Center window
    win.eval('tk::PlaceWindow . center')

    # Header
    header_frame = tk.Frame(win, bg="#520c61", height=80)
    header_frame.pack(fill="x", padx=0, pady=0)
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="🔐 LOGIN PEGAWAI", font=("Arial", 16, "bold"), 
             bg="#520c61", fg="white").pack(expand=True)

    # Main frame
    main_frame = tk.Frame(win, bg="#2d2d44")
    main_frame.pack(fill="both", expand=True, padx=30, pady=25)

    # Form frame
    form_frame = tk.Frame(main_frame, bg="#2d2d44")
    form_frame.pack(fill="x", pady=15)

    tk.Label(form_frame, text="ID Pegawai:", font=("Arial", 11, "bold"), 
             bg="#2d2d44", fg="#b19cd9").grid(row=0, column=0, sticky="w", pady=12, padx=(0, 10))
    entry_id = tk.Entry(form_frame, width=20, font=("Arial", 10), 
                       bg="#3a3a5d", fg="white", insertbackground="white")
    entry_id.grid(row=0, column=1, pady=12, sticky="ew")
    entry_id.focus()

    tk.Label(form_frame, text="Password:", font=("Arial", 11, "bold"), 
             bg="#2d2d44", fg="#b19cd9").grid(row=1, column=0, sticky="w", pady=12, padx=(0, 10))
    entry_pwd = tk.Entry(form_frame, width=20, font=("Arial", 10), show="*",
                        bg="#3a3a5d", fg="white", insertbackground="white")
    entry_pwd.grid(row=1, column=1, pady=12, sticky="ew")

    # Configure grid weights
    form_frame.columnconfigure(1, weight=1)

    def login():
        idp = entry_id.get().strip()
        pwd = entry_pwd.get().strip()

        if not idp or not pwd:
            messagebox.showerror("Error", "ID dan Password harus diisi!")
            return

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM pegawai WHERE id_pegawai=? AND password=?", (idp, pwd))
        user = cur.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Login", f"Login berhasil!\nSelamat datang {user['nama']}")
            win.destroy()
            import main_menu
            main_menu.open_main_menu(user["id_pegawai"], user["nama"])
        else:
            messagebox.showerror("Error", "ID atau Password salah!")

    # Button frame
    btn_frame = tk.Frame(main_frame, bg="#2d2d44")
    btn_frame.pack(fill="x", pady=15)

    # Main Login Button
    login_btn = tk.Button(btn_frame, text="🔓 LOGIN", 
                         bg="#27ae60", fg="white", 
                         activebackground="#219653", activeforeground="white",
                         font=("Arial", 10, "bold"),
                         width=15, height=1,
                         bd=0, relief="flat",
                         command=login)
    login_btn.pack(pady=8)

    # Secondary buttons
    secondary_frame = tk.Frame(btn_frame, bg="#2d2d44")
    secondary_frame.pack(fill="x", pady=8)

    def goto_register():
        win.destroy()
        import register_pegawai
        register_pegawai.open_register()

    register_btn = tk.Button(secondary_frame, 
                           text="📝 Daftar", 
                           bg="#3498db", fg="white",
                           activebackground="#2980b9", activeforeground="white",
                           font=("Arial", 9),
                           width=10, height=1,
                           bd=0, relief="flat",
                           command=goto_register)
    register_btn.pack(side="left", expand=True, padx=5)

    def back_to_welcome():
        win.destroy()
        import welcome
        welcome.open_welcome()

    back_btn = tk.Button(secondary_frame, 
                        text="← Kembali", 
                        bg="#95a5a6", fg="white",
                        activebackground="#7f8c8d", activeforeground="white",
                        font=("Arial", 9),
                        width=10, height=1,
                        bd=0, relief="flat",
                        command=back_to_welcome)
    back_btn.pack(side="left", expand=True, padx=5)

    # Bind Enter key untuk login
    win.bind('<Return>', lambda event: login())

    return win

if __name__ == "__main__":
    open_login()