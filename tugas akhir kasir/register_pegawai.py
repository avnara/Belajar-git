import tkinter as tk
from tkinter import messagebox
from db import get_db
import login

def open_register():
    reg = tk.Tk()
    reg.title("Register Pegawai Baru")
    reg.geometry("400x450")
    reg.configure(bg="#1e1e2e")
    reg.resizable(False, False)
    
    # Center window
    reg.eval('tk::PlaceWindow . center')

    # Header
    header_frame = tk.Frame(reg, bg="#520c61", height=80)
    header_frame.pack(fill="x", padx=0, pady=0)
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="📝 REGISTER PEGAWAI BARU", font=("Arial", 14, "bold"), 
             bg="#520c61", fg="white").pack(expand=True)

    # Main frame
    main_frame = tk.Frame(reg, bg="#2d2d44")
    main_frame.pack(fill="both", expand=True, padx=30, pady=20)

    # Form frame dengan grid
    form_frame = tk.Frame(main_frame, bg="#2d2d44")
    form_frame.pack(fill="x", pady=10)

    # Labels dan Entries menggunakan grid
    tk.Label(form_frame, text="ID Pegawai:", font=("Arial", 11, "bold"), 
             bg="#2d2d44", fg="#b19cd9").grid(row=0, column=0, sticky="w", pady=12, padx=(0, 10))
    entry_id = tk.Entry(form_frame, width=25, font=("Arial", 10),
                       bg="#3a3a5d", fg="white", insertbackground="white")
    entry_id.grid(row=0, column=1, pady=12, sticky="ew")
    entry_id.focus()

    tk.Label(form_frame, text="Nama Lengkap:", font=("Arial", 11, "bold"), 
             bg="#2d2d44", fg="#b19cd9").grid(row=1, column=0, sticky="w", pady=12, padx=(0, 10))
    entry_nama = tk.Entry(form_frame, width=25, font=("Arial", 10),
                         bg="#3a3a5d", fg="white", insertbackground="white")
    entry_nama.grid(row=1, column=1, pady=12, sticky="ew")

    tk.Label(form_frame, text="Password:", font=("Arial", 11, "bold"), 
             bg="#2d2d44", fg="#b19cd9").grid(row=2, column=0, sticky="w", pady=12, padx=(0, 10))
    entry_pass = tk.Entry(form_frame, width=25, font=("Arial", 10), show="*",
                         bg="#3a3a5d", fg="white", insertbackground="white")
    entry_pass.grid(row=2, column=1, pady=12, sticky="ew")

    # Configure grid column
    form_frame.columnconfigure(1, weight=1)

    # Info text
    info_label = tk.Label(form_frame, 
                         text="* ID Pegawai akan digunakan untuk login",
                         font=("Arial", 8),
                         bg="#2d2d44",
                         fg="#7f8c8d")
    info_label.grid(row=3, column=0, columnspan=2, sticky="w", pady=8)

    def daftar():
        idp = entry_id.get().strip()
        nama = entry_nama.get().strip()
        pwd = entry_pass.get().strip()

        if not idp or not nama or not pwd:
            messagebox.showerror("Error", "Semua data harus diisi!")
            return

        if len(pwd) < 3:
            messagebox.showerror("Error", "Password harus minimal 3 karakter!")
            return

        conn = get_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO pegawai (id_pegawai, nama, password) VALUES (?, ?, ?)",
                (idp, nama, pwd)
            )
            conn.commit()
            messagebox.showinfo("Sukses", "✅ Registrasi berhasil!\nSilakan login dengan ID dan password Anda.")
            reg.destroy()
            login.open_login()
        except Exception as e:
            messagebox.showerror("Error", f"❌ ID Pegawai sudah ada atau error:\n{str(e)}")
        finally:
            conn.close()

    # Button frame
    btn_frame = tk.Frame(main_frame, bg="#2d2d44")
    btn_frame.pack(fill="x", pady=15)

    # Main Register Button
    register_btn = tk.Button(btn_frame, text="📝 Daftar", 
                           bg="#27ae60", fg="white", 
                           activebackground="#219653", activeforeground="white",
                           font=("Arial", 10, "bold"),
                           width=15, height=1,
                           bd=0, relief="flat",
                           cursor="hand2",
                           command=daftar)
    register_btn.pack(pady=8)

    # Secondary buttons in horizontal layout
    secondary_frame = tk.Frame(btn_frame, bg="#2d2d44")
    secondary_frame.pack(fill="x", pady=5)

    def goto_login():
        reg.destroy()
        login.open_login()

    login_btn = tk.Button(secondary_frame, 
                         text="🔐 Ke Login", 
                         bg="#3498db", fg="white",
                         activebackground="#2980b9", activeforeground="white",
                         font=("Arial", 9),
                         width=12, height=1,
                         bd=0, relief="flat",
                         cursor="hand2",
                         command=goto_login)
    login_btn.pack(side="left", expand=True, padx=5)

    def back_to_welcome():
        reg.destroy()
        import welcome
        welcome.open_welcome()

    back_btn = tk.Button(secondary_frame, 
                        text="← Kembali", 
                        bg="#95a5a6", fg="white",
                        activebackground="#7f8c8d", activeforeground="white",
                        font=("Arial", 9),
                        width=12, height=1,
                        bd=0, relief="flat",
                        cursor="hand2",
                        command=back_to_welcome)
    back_btn.pack(side="left", expand=True, padx=5)

    # Bind Enter key untuk daftar
    reg.bind('<Return>', lambda event: daftar())

    return reg

# Fungsi utama untuk menjalankan register
if __name__ == "__main__":
    open_register()