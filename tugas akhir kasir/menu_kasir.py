import tkinter as tk
from tkinter import ttk, messagebox
from db import get_db
import datetime

def open_menu_kasir(id_pegawai, nama_pegawai):
    win = tk.Toplevel()
    win.title(f"Menu Kasir - {nama_pegawai}")
    win.geometry("1200x750")  # Tinggi ditambah sedikit
    win.configure(bg="#1e1e2e")
    
    # Variabel global
    cart_items = []
    total_harga = tk.IntVar(value=0)
    
    # ========== HEADER MODERN ==========
    header_frame = tk.Frame(win, bg="#520c61", height=100)
    header_frame.pack(fill="x", padx=0, pady=0)
    header_frame.pack_propagate(False)
    
    # Logo/Kiri Header
    left_header = tk.Frame(header_frame, bg="#520c61")
    left_header.pack(side="left", padx=30, pady=15)
    
    tk.Label(left_header, text="🛒", font=("Arial", 28, "bold"), 
             bg="#520c61", fg="white").pack(side="left", padx=(0, 15))
    
    title_frame = tk.Frame(left_header, bg="#520c61")
    title_frame.pack(side="left")
    
    tk.Label(title_frame, text="KASIR TOKO", font=("Arial", 24, "bold"), 
             bg="#520c61", fg="white").pack(anchor="w")
    tk.Label(title_frame, text="Snack Haven POS System", font=("Arial", 10), 
             bg="#520c61", fg="#b19cd9").pack(anchor="w")
    
    # Kanan Header - Info Kasir
    right_header = tk.Frame(header_frame, bg="#520c61")
    right_header.pack(side="right", padx=30, pady=15)
    
    info_frame = tk.Frame(right_header, bg="#520c61")
    info_frame.pack(anchor="e")
    
    tk.Label(info_frame, text=f"👤 {nama_pegawai}", font=("Arial", 12, "bold"), 
             bg="#520c61", fg="white").pack(anchor="e")
    
    current_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    tk.Label(info_frame, text=f"📅 {current_date}", font=("Arial", 10), 
             bg="#520c61", fg="#b19cd9").pack(anchor="e")
    
    tk.Label(info_frame, text=f"🆔 ID: {id_pegawai}", font=("Arial", 9), 
             bg="#520c61", fg="#b19cd9").pack(anchor="e")
    
    # ========== MAIN CONTENT FRAME ==========
    main_frame = tk.Frame(win, bg="#2d2d44")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # ========== LEFT FRAME - DAFTAR BARANG ==========
    left_card = tk.Frame(main_frame, bg="#3a3a5d", relief="flat", bd=0)
    left_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
    
    # Header Card Kiri
    left_header_card = tk.Frame(left_card, bg="#520c61", height=50)
    left_header_card.pack(fill="x", padx=0, pady=0)
    left_header_card.pack_propagate(False)
    
    tk.Label(left_header_card, text="📋 DAFTAR BARANG", font=("Arial", 14, "bold"), 
             bg="#520c61", fg="white").pack(pady=15)
    
    # Search frame
    search_frame = tk.Frame(left_card, bg="#3a3a5d")
    search_frame.pack(fill="x", padx=20, pady=15)
    
    search_var = tk.StringVar()
    
    # Search box dengan style modern
    search_container = tk.Frame(search_frame, bg="#2d2d44", relief="flat", bd=1)
    search_container.pack(fill="x", pady=5)
    
    tk.Label(search_container, text="🔍", bg="#2d2d44", fg="#b19cd9", 
             font=("Arial", 12)).pack(side="left", padx=10)
    
    ent_search = tk.Entry(search_container, textvariable=search_var, 
                         bg="#2d2d44", fg="white", 
                         insertbackground="white",
                         font=("Arial", 11), bd=0)
    ent_search.pack(side="left", fill="x", expand=True, padx=5, pady=10)
    ent_search.insert(0, "Cari barang...")
    
    def on_search_focus_in(event):
        if ent_search.get() == "Cari barang...":
            ent_search.delete(0, tk.END)
            ent_search.config(fg="white")
    
    def on_search_focus_out(event):
        if not ent_search.get():
            ent_search.insert(0, "Cari barang...")
            ent_search.config(fg="gray")
    
    ent_search.bind("<FocusIn>", on_search_focus_in)
    ent_search.bind("<FocusOut>", on_search_focus_out)
    ent_search.bind("<Return>", lambda e: load_barang(tree_barang, search_var.get()))
    
    # Treeview barang
    tree_frame = tk.Frame(left_card, bg="#3a3a5d")
    tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    # Style untuk treeview
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Custom.Treeview",
                    background="#2d2d44",
                    foreground="white",
                    fieldbackground="#2d2d44",
                    borderwidth=0,
                    font=('Arial', 10))
    style.configure("Custom.Treeview.Heading",
                    background="#520c61",
                    foreground="white",
                    font=('Arial', 11, 'bold'),
                    relief="flat")
    style.map("Custom.Treeview.Heading",
              background=[('active', '#6a1b9a')])
    
    cols_barang = ("ID", "Nama Barang", "Harga", "Stok", "Satuan")
    tree_barang = ttk.Treeview(tree_frame, columns=cols_barang, 
                              show="headings", height=15,
                              style="Custom.Treeview")
    
    for col in cols_barang:
        tree_barang.heading(col, text=col)
        if col == "Nama Barang":
            tree_barang.column(col, width=280, anchor="w")
        elif col == "Harga":
            tree_barang.column(col, width=120, anchor="center")
        elif col == "Stok":
            tree_barang.column(col, width=80, anchor="center")
        else:
            tree_barang.column(col, width=80, anchor="center")
    
    # Scrollbar
    vsb_barang = ttk.Scrollbar(tree_frame, orient="vertical", 
                               command=tree_barang.yview)
    tree_barang.configure(yscroll=vsb_barang.set)
    vsb_barang.pack(side="right", fill="y")
    tree_barang.pack(side="left", fill="both", expand=True)
    
    # ========== RIGHT FRAME - KERANJANG BELANJA ==========
    right_card = tk.Frame(main_frame, bg="#3a3a5d", relief="flat", bd=0)
    right_card.pack(side="right", fill="both", expand=True, padx=(10, 0))
    
    # Header Card Kanan
    right_header_card = tk.Frame(right_card, bg="#520c61", height=50)
    right_header_card.pack(fill="x", padx=0, pady=0)
    right_header_card.pack_propagate(False)
    
    tk.Label(right_header_card, text="🛍️ KERANJANG BELANJA", font=("Arial", 14, "bold"), 
             bg="#520c61", fg="white").pack(pady=15)
    
    # Treeview keranjang
    tree_keranjang_frame = tk.Frame(right_card, bg="#3a3a5d")
    tree_keranjang_frame.pack(fill="both", expand=True, padx=20, pady=15)
    
    tree_keranjang = ttk.Treeview(tree_keranjang_frame, 
                                 columns=("No", "Nama Barang", "Jumlah", "Harga", "Subtotal"), 
                                 show="headings", height=12,
                                 style="Custom.Treeview")
    
    tree_keranjang.heading("No", text="No")
    tree_keranjang.heading("Nama Barang", text="Nama Barang")
    tree_keranjang.heading("Jumlah", text="Jumlah")
    tree_keranjang.heading("Harga", text="Harga")
    tree_keranjang.heading("Subtotal", text="Subtotal")
    
    tree_keranjang.column("No", width=50, anchor="center")
    tree_keranjang.column("Nama Barang", width=220, anchor="w")
    tree_keranjang.column("Jumlah", width=80, anchor="center")
    tree_keranjang.column("Harga", width=100, anchor="center")
    tree_keranjang.column("Subtotal", width=120, anchor="center")
    
    # Scrollbar keranjang
    vsb_keranjang = ttk.Scrollbar(tree_keranjang_frame, orient="vertical", 
                                  command=tree_keranjang.yview)
    tree_keranjang.configure(yscroll=vsb_keranjang.set)
    vsb_keranjang.pack(side="right", fill="y")
    tree_keranjang.pack(side="left", fill="both", expand=True)
    
    # Input frame untuk tambah barang
    input_frame = tk.Frame(right_card, bg="#3a3a5d")
    input_frame.pack(fill="x", padx=20, pady=10)
    
    # Jumlah beli
    jumlah_frame = tk.Frame(input_frame, bg="#2d2d44", relief="flat", bd=1)
    jumlah_frame.pack(side="left", padx=(0, 10))
    
    tk.Label(jumlah_frame, text="Jumlah:", bg="#2d2d44", fg="#b19cd9",
             font=("Arial", 10)).pack(side="left", padx=10, pady=8)
    
    ent_jumlah = tk.Entry(jumlah_frame, width=8, bg="#2d2d44", fg="white",
                         insertbackground="white",
                         font=("Arial", 11), bd=0)
    ent_jumlah.pack(side="left", padx=(0, 10), pady=8)
    ent_jumlah.insert(0, "1")
    
    # Tombol dengan style modern
    btn_style = {
        "font": ("Arial", 10, "bold"),
        "bd": 0,
        "relief": "flat",
        "width": 15,
        "height": 1,
        "cursor": "hand2"
    }
    
    btn_tambah_keranjang = tk.Button(input_frame, 
                                    text="➕ Tambah",
                                    bg="#27ae60", 
                                    fg="white",
                                    activebackground="#219653",
                                    activeforeground="white",
                                    command=lambda: tambah_ke_keranjang(tree_barang, tree_keranjang, ent_jumlah, cart_items, total_harga),
                                    **btn_style)
    btn_tambah_keranjang.pack(side="left", padx=5)
    
    btn_hapus_item = tk.Button(input_frame, 
                              text="🗑️ Hapus",
                              bg="#e74c3c", 
                              fg="white",
                              activebackground="#c0392b",
                              activeforeground="white",
                              command=lambda: hapus_dari_keranjang(tree_keranjang, cart_items, total_harga),
                              **btn_style)
    btn_hapus_item.pack(side="left", padx=5)
    
    # Total harga frame
    total_frame = tk.Frame(right_card, bg="#520c61", height=80)
    total_frame.pack(fill="x", padx=20, pady=(10, 20))
    total_frame.pack_propagate(False)
    
    total_inner = tk.Frame(total_frame, bg="#520c61")
    total_inner.pack(expand=True)
    
    tk.Label(total_inner, text="TOTAL:", font=("Arial", 18, "bold"), 
             bg="#520c61", fg="white").pack(side="left", padx=20)
    
    lbl_total = tk.Label(total_inner, textvariable=total_harga, 
                        font=("Arial", 22, "bold"), 
                        bg="#520c61", fg="#FFD700")
    lbl_total.pack(side="left", padx=20)
    
    # Button frame
    button_frame = tk.Frame(right_card, bg="#3a3a5d")
    button_frame.pack(fill="x", padx=20, pady=(0, 20))
    
    btn_main_style = {
        "font": ("Arial", 11, "bold"),
        "bd": 0,
        "relief": "flat",
        "width": 18,
        "height": 2,
        "cursor": "hand2"
    }
    
    # Tombol utama dalam grid
    btn_proses = tk.Button(button_frame, 
                          text="💳 PROSES TRANSAKSI",
                          bg="#9b59b6",
                          fg="white",
                          activebackground="#8e44ad",
                          activeforeground="white",
                          command=lambda: proses_transaksi(tree_keranjang, cart_items, total_harga, id_pegawai, nama_pegawai, win),
                          **btn_main_style)
    btn_proses.grid(row=0, column=0, padx=5, pady=5)
    
    btn_reset = tk.Button(button_frame, 
                         text="🔄 RESET",
                         bg="#3498db",
                         fg="white",
                         activebackground="#2980b9",
                         activeforeground="white",
                         command=lambda: reset_keranjang(tree_keranjang, cart_items, total_harga),
                         **btn_main_style)
    btn_reset.grid(row=0, column=1, padx=5, pady=5)
    
    btn_kembali = tk.Button(button_frame, 
                           text="← KEMBALI",
                           bg="#95a5a6",
                           fg="white",
                           activebackground="#7f8c8d",
                           activeforeground="white",
                           command=win.destroy,
                           **btn_main_style)
    btn_kembali.grid(row=0, column=2, padx=5, pady=5)
    
    # Configure grid columns
    for i in range(3):
        button_frame.columnconfigure(i, weight=1)
    
    # ========== FUNGSI-FUNGSI ==========
    
    def load_barang(tree, filter_text=""):
        for row in tree.get_children():
            tree.delete(row)
        
        conn = get_db()
        cur = conn.cursor()
        
        if filter_text and filter_text != "Cari barang...":
            q = f"%{filter_text}%"
            cur.execute(
                "SELECT * FROM barang WHERE (id_barang LIKE ? OR nama_barang LIKE ?) AND stok > 0 ORDER BY nama_barang ASC",
                (q, q),
            )
        else:
            cur.execute("SELECT * FROM barang WHERE stok > 0 ORDER BY nama_barang ASC")
        
        data = cur.fetchall()
        conn.close()
        
        for item in data:
            tree.insert(
                "",
                "end",
                values=(
                    item["id_barang"],
                    item["nama_barang"],
                    f"Rp {item['harga']:,}",
                    item["stok"],
                    item["satuan"] if item["satuan"] else "pcs"
                )
            )
    
    def tambah_ke_keranjang(tree_barang, tree_keranjang, ent_jumlah, cart_items, total_harga_var):
        selected = tree_barang.focus()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih barang terlebih dahulu!")
            return
        
        item_values = tree_barang.item(selected)["values"]
        if not item_values:
            return
        
        try:
            jumlah = int(ent_jumlah.get())
            if jumlah <= 0:
                messagebox.showerror("Error", "Jumlah harus lebih dari 0!")
                return
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka!")
            return
        
        id_barang = item_values[0]
        nama_barang = item_values[1]
        harga = int(item_values[2].replace("Rp ", "").replace(",", ""))
        stok = item_values[3]
        
        # Cek stok
        if jumlah > stok:
            messagebox.showerror("Error", f"Stok tidak cukup! Stok tersedia: {stok}")
            return
        
        # Cek apakah barang sudah ada di keranjang
        for i, item in enumerate(cart_items):
            if item["id_barang"] == id_barang:
                # Update jumlah jika sudah ada
                new_jumlah = item["jumlah"] + jumlah
                if new_jumlah > stok:
                    messagebox.showerror("Error", f"Stok tidak cukup! Stok tersedia: {stok}")
                    return
                
                cart_items[i]["jumlah"] = new_jumlah
                cart_items[i]["subtotal"] = new_jumlah * harga
                
                # Update treeview
                for child in tree_keranjang.get_children():
                    if tree_keranjang.item(child)["values"][0] == i + 1:
                        tree_keranjang.item(child, values=(
                            i + 1, nama_barang, new_jumlah, f"Rp {harga:,}", f"Rp {new_jumlah * harga:,}"
                        ))
                        break
                
                update_total_harga(cart_items, total_harga_var)
                return
        
        # Tambah barang baru ke keranjang
        subtotal = jumlah * harga
        cart_items.append({
            "id_barang": id_barang,
            "nama_barang": nama_barang,
            "harga": harga,
            "jumlah": jumlah,
            "subtotal": subtotal
        })
        
        # Update treeview
        tree_keranjang.insert(
            "",
            "end",
            values=(
                len(cart_items),
                nama_barang,
                jumlah,
                f"Rp {harga:,}",
                f"Rp {subtotal:,}"
            )
        )
        
        update_total_harga(cart_items, total_harga_var)
        ent_jumlah.delete(0, tk.END)
        ent_jumlah.insert(0, "1")
    
    def hapus_dari_keranjang(tree_keranjang, cart_items, total_harga_var):
        selected = tree_keranjang.focus()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih item yang ingin dihapus!")
            return
        
        item_index = tree_keranjang.item(selected)["values"][0] - 1
        
        if 0 <= item_index < len(cart_items):
            cart_items.pop(item_index)
            tree_keranjang.delete(selected)
            
            # Update nomor urut
            for i, child in enumerate(tree_keranjang.get_children()):
                values = list(tree_keranjang.item(child)["values"])
                values[0] = i + 1
                tree_keranjang.item(child, values=values)
            
            update_total_harga(cart_items, total_harga_var)
    
    def update_total_harga(cart_items, total_harga_var):
        total = sum(item["subtotal"] for item in cart_items)
        total_harga_var.set(f"Rp {total:,}")
    
    def reset_keranjang(tree_keranjang, cart_items, total_harga_var):
        if cart_items:
            if messagebox.askyesno("Konfirmasi", "Yakin ingin mengosongkan keranjang?"):
                for row in tree_keranjang.get_children():
                    tree_keranjang.delete(row)
                cart_items.clear()
                total_harga_var.set("Rp 0")
    
    def proses_transaksi(tree_keranjang, cart_items, total_harga_var, id_pegawai, nama_pegawai, parent_window):
        if not cart_items:
            messagebox.showwarning("Peringatan", "Keranjang belanja kosong!")
            return
        
        total_bayar = sum(item["subtotal"] for item in cart_items)
        
        # Konfirmasi transaksi
        if not messagebox.askyesno("Konfirmasi", f"Total yang harus dibayar: Rp {total_bayar:,}\n\nProses transaksi?"):
            return
        
        conn = get_db()
        cur = conn.cursor()
        
        try:
            # Update stok dan simpan transaksi
            for item in cart_items:
                # Update stok barang
                cur.execute("UPDATE barang SET stok = stok - ? WHERE id_barang = ?", 
                           (item["jumlah"], item["id_barang"]))
                
                # Simpan transaksi
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cur.execute(
                    "INSERT INTO transaksi (tgl, id_pegawai, nama_pegawai, id_barang, nama_barang, jumlah, total_harga) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (current_time, id_pegawai, nama_pegawai, item["id_barang"], item["nama_barang"], item["jumlah"], item["subtotal"])
                )
            
            conn.commit()
            messagebox.showinfo("Sukses", f"Transaksi berhasil!\nTotal: Rp {total_bayar:,}")
            
            # Reset keranjang
            reset_keranjang(tree_keranjang, cart_items, total_harga_var)
            # Reload data barang untuk update stok
            load_barang(tree_barang)
            
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Gagal memproses transaksi:\n{str(e)}")
        finally:
            conn.close()
    
    # ========== EVENT BINDINGS ==========
    
    # Load data barang pertama kali
    load_barang(tree_barang)
    
    # Bind double click untuk tambah cepat
    def on_double_click(event):
        tambah_ke_keranjang(tree_barang, tree_keranjang, ent_jumlah, cart_items, total_harga)
    
    tree_barang.bind("<Double-1>", on_double_click)
    
    # Bind enter di search
    def on_search_change(*args):
        load_barang(tree_barang, search_var.get())
    
    search_var.trace("w", on_search_change)
    
    # Focus ke search box
    ent_search.focus()
    
    return win

# Untuk testing
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_menu_kasir("TEST001", "Kasir Test")
    root.mainloop()