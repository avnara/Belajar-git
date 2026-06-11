import tkinter as tk
from tkinter import messagebox
import stok_barang
import menu_kasir

def open_main_menu(id_pegawai, nama_pegawai):
    win = tk.Toplevel()
    win.title("Menu Utama - Sistem POS")
    win.geometry("500x500")
    win.configure(bg="#1e1e2e")

    # Header
    header_frame = tk.Frame(win, bg="#520c61", height=100)
    header_frame.pack(fill="x", padx=0, pady=0)
    header_frame.pack_propagate(False)

    tk.Label(header_frame, text=f"Selamat Datang, {nama_pegawai}", 
             font=("Arial", 16, "bold"), bg="#520c61", fg="white").pack(expand=True, pady=5)
    
    tk.Label(header_frame, text=f"🆔 ID: {id_pegawai}", 
             font=("Arial", 10), bg="#520c61", fg="#b19cd9").pack(expand=True)

    # Main content
    main_frame = tk.Frame(win, bg="#2d2d44")
    main_frame.pack(fill="both", expand=True, padx=40, pady=30)

    # Style untuk tombol
    btn_style = {
        "font": ("Arial", 12, "bold"),
        "width": 22,
        "height": 2,
        "bd": 0,
        "relief": "flat",
        "cursor": "hand2"
    }

    btn_stok = tk.Button(main_frame, text="📦 KELOLA STOK BARANG", 
                        bg="#3498db", fg="white",
                        activebackground="#2980b9", activeforeground="white",
                        command=stok_barang.open_stok_barang, **btn_style)
    btn_stok.pack(pady=15)

    btn_kasir = tk.Button(main_frame, text="💰 MULAI KASIR", 
                         bg="#27ae60", fg="white",
                         activebackground="#219653", activeforeground="white",
                         command=lambda: menu_kasir.open_menu_kasir(id_pegawai, nama_pegawai), **btn_style)
    btn_kasir.pack(pady=15)

    def buka_laporan():
        try:
            import laporan_penjualan
            laporan_penjualan.open_laporan_penjualan()
        except ImportError as e:
            messagebox.showerror("Error", f"Modul laporan tidak ditemukan: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuka laporan: {e}")

    btn_laporan = tk.Button(main_frame, text="📊 LAPORAN PENJUALAN", 
                           bg="#f39c12", fg="white",
                           activebackground="#e67e22", activeforeground="white",
                           command=buka_laporan, **btn_style)
    btn_laporan.pack(pady=15)

    # Tombol logout
    btn_logout = tk.Button(main_frame, text="🚪 LOGOUT", 
                          bg="#e74c3c", fg="white",
                          activebackground="#c0392b", activeforeground="white",
                          command=win.destroy, **btn_style)
    btn_logout.pack(pady=15)

    # Status bar
    status_frame = tk.Frame(win, bg="#34495e", height=30)
    status_frame.pack(fill="x", side="bottom")
    status_frame.pack_propagate(False)
    
    tk.Label(status_frame, text="Snack Haven POS System v1.0", 
             font=("Arial", 9), bg="#34495e", fg="#b19cd9").pack(side="left", padx=10)