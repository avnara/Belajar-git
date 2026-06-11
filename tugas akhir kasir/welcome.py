import tkinter as tk
from tkinter import ttk, messagebox
import login
import register_pegawai

def open_welcome():
    # Buat window welcome
    welcome_win = tk.Tk()
    welcome_win.title("Snack Haven POS System")
    welcome_win.geometry("500x600")
    welcome_win.configure(bg="#1e1e2e")
    welcome_win.resizable(False, False)
    
    # Center window
    welcome_win.eval('tk::PlaceWindow . center')
    
    # Frame utama
    main_frame = tk.Frame(welcome_win, bg="#1e1e2e")
    main_frame.pack(fill="both", expand=True, padx=35, pady=25)
    
    # Logo/Header
    logo_frame = tk.Frame(main_frame, bg="#1e1e2e")
    logo_frame.pack(pady=(0, 15))
    
    # Logo text 
    logo_text = tk.Label(logo_frame, 
                        text="🛒 Snack Haven", 
                        font=("Arial", 24, "bold"),
                        bg="#1e1e2e", 
                        fg="white")
    logo_text.pack(pady=8)
    
    # Subtitle
    subtitle = tk.Label(logo_frame,
                       text="Surganya Camilan Unik & Lezat",
                       font=("Arial", 12),
                       bg="#1e1e2e",
                       fg="#b19cd9")
    subtitle.pack()
    
    # Card container
    card_frame = tk.Frame(main_frame, bg="#2d2d44", relief="flat", bd=1)
    card_frame.pack(fill="both", expand=True, pady=15)
    
    # Welcome message
    welcome_msg = tk.Label(card_frame,
                          text="Selamat Datang di\nSnack Haven POS System",
                          font=("Arial", 14, "bold"),
                          bg="#2d2d44",
                          fg="white",
                          justify="center")
    welcome_msg.pack(pady=20)
    
    # Features list
    features_frame = tk.Frame(card_frame, bg="#2d2d44")
    features_frame.pack(pady=10, padx=30)
    
    features = [
        "✓ Manajemen Stok Barang Lengkap",
        "✓ Sistem Kasir Modern & Cepat",
        "✓ Laporan Penjualan Real-time",
        "✓ Analisis Data Visual",
        "✓ Multi-user Support"
    ]
    
    for feature in features:
        feature_frame = tk.Frame(features_frame, bg="#2d2d44")
        feature_frame.pack(fill="x", pady=5)    
        
        feature_label = tk.Label(feature_frame,
                                text=feature,
                                font=("Arial", 10),
                                bg="#2d2d44",
                                fg="#b19cd9",
                                anchor="w")
        feature_label.pack(fill="x")
    
    # Button frame untuk opsi lain
    button_frame = tk.Frame(card_frame, bg="#2d2d44")
    button_frame.pack(pady=15)
    
    # Style untuk tombol
    btn_style = {
        "font": ("Arial", 10, "bold"),
        "width": 16,
        "height": 1,
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }
    
    # Tombol Login
    login_btn = tk.Button(button_frame,
                         text="🔐 LOGIN",
                         bg="#27ae60",
                         fg="white",
                         activebackground="#219653",
                         activeforeground="white",
                         command=lambda: goto_login(welcome_win),
                         **btn_style)
    login_btn.grid(row=0, column=0, padx=5, pady=5)
    
    # Tombol Register
    register_btn = tk.Button(button_frame,
                            text="📝 REGISTER", 
                            bg="#3498db", 
                            fg="white",
                            activebackground="#2980b9",
                            activeforeground="white",
                            command=lambda: goto_register(welcome_win),
                            **btn_style)
    register_btn.grid(row=0, column=1, padx=5, pady=5)
    
    # Tombol Exit
    exit_btn = tk.Button(button_frame,
                        text="🚪 KELUAR",
                        bg="#e74c3c",
                        fg="white",
                        activebackground="#c0392b",
                        activeforeground="white",
                        command=welcome_win.quit,
                        **btn_style)
    exit_btn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    
    # Footer
    footer_frame = tk.Frame(main_frame, bg="#1e1e2e")
    footer_frame.pack(side="bottom", fill="x", pady=10)
    
    footer_text = tk.Label(footer_frame,
                          text="© 2024 Snack Haven POS System - v2.0",
                          font=("Arial", 8),
                          bg="#1e1e2e",
                          fg="#7f8c8d")
    footer_text.pack()
    
    # Fungsi untuk navigasi
    def goto_login(parent_window):
        parent_window.destroy()
        login.open_login()
    
    def goto_register(parent_window):
        parent_window.destroy()
        register_pegawai.open_register()
    
    return welcome_win

if __name__ == "__main__":
    app = open_welcome()
    app.mainloop()