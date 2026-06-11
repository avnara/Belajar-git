import tkinter as tk
from tkinter import messagebox
from db import get_db

def open_login():
    win = tk.Tk()
    win.title("Login Pegawai")
    win.geometry("350x300")
    win.configure(bg="#f8f9fa")
    win.resizable(False, False)
    
    # Center window
    win.eval('tk::PlaceWindow . center')

    # Header
    header_frame = tk.Frame(win, bg="#2c3e50", height=80)
    header_frame.pack(fill="x", padx=0, pady=0)
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="LOGIN PEGAWAI", font=("Arial", 16, "bold"), 
             bg="#2c3e50", fg="white").pack(expand=True)

    frame = tk.Frame(win, padx=20, pady=20, bg="#f8f9fa")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="ID Pegawai:", font=("Arial", 10, "bold"), 
             bg="#f8f9fa").grid(row=0, column=0, sticky="w", pady=10)
    entry_id = tk.Entry(frame, width=25, font=("Arial", 10))
    entry_id.grid(row=0, column=1, pady=10, padx=10)
    entry_id.focus()

    tk.Label(frame, text="Password:", font=("Arial", 10, "bold"), 
             bg="#f8f9fa").grid(row=1, column=0, sticky="w", pady=10)
    entry_pwd = tk.Entry(frame, width=25, font=("Arial", 10), show="*")
    entry_pwd.grid(row=1, column=1, pady=10, padx=10)

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
    btn_frame = tk.Frame(frame, bg="#f8f9fa")
    btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

    tk.Button(btn_frame, text="Login", width=15, font=("Arial", 10, "bold"),
              bg="#27ae60", fg="white", command=login).pack(pady=5)

    def goto_register():
        win.destroy()
        import register_pegawai
        register_pegawai.open_register()

    tk.Button(btn_frame, text="Daftar Pegawai Baru", width=15, font=("Arial", 10),
              bg="#3498db", fg="white", command=goto_register).pack(pady=5)

    def back_to_welcome():
        win.destroy()
        import welcome
        welcome.open_welcome()

    tk.Button(btn_frame, text="Kembali", width=15, font=("Arial", 10),
              bg="#95a5a6", fg="white", command=back_to_welcome).pack(pady=5)

    # Bind Enter key untuk login
    win.bind('<Return>', lambda event: login())

    win.mainloop()

if __name__ == "__main__":
    open_login()