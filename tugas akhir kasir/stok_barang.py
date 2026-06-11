import tkinter as tk
from tkinter import ttk, messagebox
from db import get_db

# ---------------------------
#   Konfigurasi satuan & konversi
# ---------------------------
VALID_SATUAN = ["pcs", "dus", "kg", "box", "pack"]
KONVERSI = {
    "dus": 12,   # 1 dus = 12 pcs
    "box": 10,   # 1 box = 10 pcs
    "pack": 6    # 1 pack = 6 pcs
}

# ---------------------------
#   UTILS - FIXED
# ---------------------------
def to_pcs(quantity: int, satuan: str) -> int:
    satuan = (satuan or "").lower()
    if satuan in KONVERSI:
        return quantity * KONVERSI[satuan]
    return quantity

def safe_get(row, key, default=None):
    """Safe method to get values from sqlite3.Row"""
    try:
        value = row[key]
        return value if value is not None else default
    except (KeyError, TypeError):
        return default

# ---------------------------
#   LOAD DATA (dengan filter) - FIXED
# ---------------------------
def load_data(tree, filter_text=""):
    # kosongkan tree
    for row in tree.get_children():
        tree.delete(row)

    conn = get_db()
    cur = conn.cursor()

    if filter_text:
        q = f"%{filter_text}%"
        cur.execute(
            "SELECT * FROM barang WHERE id_barang LIKE ? OR nama_barang LIKE ? ORDER BY nama_barang ASC",
            (q, q),
        )
    else:
        cur.execute("SELECT * FROM barang ORDER BY nama_barang ASC")

    data = cur.fetchall()
    conn.close()

    for item in data:
        stok = safe_get(item, "stok", 0)
        satuan = safe_get(item, "satuan", "pcs")
        
        warna = "normal"
        if stok <= 5:
            warna = "merah"
        elif 5 < stok <= 10:
            warna = "kuning"

        tree.insert(
            "",
            "end",
            values=(
                safe_get(item, "id_barang", ""),
                safe_get(item, "nama_barang", ""),
                safe_get(item, "harga", 0),
                stok,
                satuan
            ),
            tags=(warna,),
        )

# ---------------------------
#   TAMBAH BARANG - STYLE DARK
# ---------------------------
def tambah_barang(tree):
    win = tk.Toplevel()
    win.title("Tambah Barang")
    win.geometry("400x380")
    win.resizable(False, False)
    win.configure(bg="#1e1e2e")

    # Header
    tk.Label(win, text="➕ TAMBAH BARANG BARU", font=("Arial", 14, "bold"), 
             bg="#1e1e2e", fg="white").pack(pady=10)

    # Frame input
    input_frame = tk.Frame(win, bg="#1e1e2e")
    input_frame.pack(pady=10, padx=20, fill="both")

    # Nama Barang
    tk.Label(input_frame, text="Nama Barang *", bg="#1e1e2e", 
             font=("Arial", 10), fg="#b19cd9").grid(row=0, column=0, sticky="w", pady=8)
    ent_nama = tk.Entry(input_frame, width=30, font=("Arial", 10), 
                       bg="#2d2d44", fg="white", insertbackground="white")
    ent_nama.grid(row=0, column=1, padx=10, pady=8)

    # Harga
    tk.Label(input_frame, text="Harga (Rp) *", bg="#1e1e2e", 
             font=("Arial", 10), fg="#b19cd9").grid(row=1, column=0, sticky="w", pady=8)
    ent_harga = tk.Entry(input_frame, width=30, font=("Arial", 10), 
                        bg="#2d2d44", fg="white", insertbackground="white")
    ent_harga.grid(row=1, column=1, padx=10, pady=8)

    # Stok
    tk.Label(input_frame, text="Stok Awal *", bg="#1e1e2e", 
             font=("Arial", 10), fg="#b19cd9").grid(row=2, column=0, sticky="w", pady=8)
    ent_stok = tk.Entry(input_frame, width=30, font=("Arial", 10), 
                       bg="#2d2d44", fg="white", insertbackground="white")
    ent_stok.grid(row=2, column=1, padx=10, pady=8)

    # Satuan
    tk.Label(input_frame, text=f"Satuan *", bg="#1e1e2e", 
             font=("Arial", 10), fg="#b19cd9").grid(row=3, column=0, sticky="w", pady=8)
    ent_satuan = ttk.Combobox(input_frame, values=VALID_SATUAN, state="readonly", 
                             width=27, font=("Arial", 10))
    ent_satuan.set("pcs")
    ent_satuan.grid(row=3, column=1, padx=10, pady=8)

    def simpan():
        nama = ent_nama.get().strip()
        harga = ent_harga.get().strip()
        stok_in = ent_stok.get().strip()
        satuan = ent_satuan.get().strip().lower()

        # Validasi
        if not all([nama, harga, stok_in, satuan]):
            messagebox.showerror("Error", "Semua kolom harus diisi!")
            return

        if satuan not in VALID_SATUAN:
            messagebox.showerror("Error", f"Satuan tidak valid. Pilih: {', '.join(VALID_SATUAN)}")
            return

        try:
            harga_int = int(harga)
            stok_int = int(stok_in)
            if harga_int < 0 or stok_int < 0:
                messagebox.showerror("Error", "Harga dan Stok tidak boleh negatif!")
                return
        except ValueError:
            messagebox.showerror("Error", "Harga dan Stok harus berupa angka!")
            return

        # Konversi stok ke pcs
        stok_final = to_pcs(stok_int, satuan)

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO barang (nama_barang, harga, stok, satuan) VALUES (?, ?, ?, ?)",
                (nama, harga_int, stok_final, satuan)
            )
            conn.commit()
            messagebox.showinfo("Sukses", f"Barang '{nama}' berhasil ditambahkan!")
            win.destroy()
            load_data(tree)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambahkan barang:\n{str(e)}")
        finally:
            conn.close()

    # Frame tombol
    btn_frame = tk.Frame(win, bg="#1e1e2e")
    btn_frame.pack(pady=20)

    tk.Button(btn_frame, text="💾 Simpan", command=simpan, 
              bg="#27ae60", fg="white", activebackground="#219653",
              font=("Arial", 10, "bold"), width=12, height=1,
              bd=0, relief="flat").pack(side="left", padx=10)
    
    tk.Button(btn_frame, text="❌ Batal", command=win.destroy, 
              bg="#e74c3c", fg="white", activebackground="#c0392b",
              font=("Arial", 10), width=12, height=1,
              bd=0, relief="flat").pack(side="left", padx=10)

    # Focus ke input pertama
    ent_nama.focus()

# ---------------------------
#   EDIT BARANG - STYLE DARK
# ---------------------------
def edit_barang(tree):
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Pilih barang yang ingin di-edit terlebih dahulu.")
        return

    item = tree.item(selected)["values"]
    if not item:
        return
        
    idb = item[0]

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM barang WHERE id_barang=?", (idb,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        messagebox.showerror("Error", "Data barang tidak ditemukan di database.")
        return

    win = tk.Toplevel()
    win.title("Edit Barang")
    win.geometry("400x400")
    win.resizable(False, False)
    win.configure(bg="#1e1e2e")

    # Header
    tk.Label(win, text="✏️ EDIT BARANG", font=("Arial", 14, "bold"), 
             bg="#1e1e2e", fg="white").pack(pady=10)

    # Frame input
    input_frame = tk.Frame(win, bg="#1e1e2e")
    input_frame.pack(pady=10, padx=20, fill="both")

    # ID Barang (readonly)
    tk.Label(input_frame, text="ID Barang", bg="#1e1e2e", 
             font=("Arial", 10), fg="#b19cd9").grid(row=0, column=0, sticky="w", pady=8)
    ent_id = tk.Entry(input_frame, width=30, font=("Arial", 10), 
                     state="readonly", bg="#3a3a5d", fg="white")
    ent_id.grid(row=0, column=1, padx=10, pady=8)
    ent_id.insert(0, str(safe_get(row, "id_barang", "")))

    # Nama Barang
    tk.Label(input_frame, text="Nama Barang *", bg="#1e1e2e", 
             font=("Arial", 10), fg="#b19cd9").grid(row=1, column=0, sticky="w", pady=8)
    ent_nama = tk.Entry(input_frame, width=30, font=("Arial", 10), 
                       bg="#2d2d44", fg="white", insertbackground="white")
    ent_nama.grid(row=1, column=1, padx=10, pady=8)
    ent_nama.insert(0, safe_get(row, "nama_barang", ""))

    # Harga
    tk.Label(input_frame, text="Harga (Rp) *", bg="#1e1e2e", 
             font=("Arial", 10), fg="#b19cd9").grid(row=2, column=0, sticky="w", pady=8)
    ent_harga = tk.Entry(input_frame, width=30, font=("Arial", 10), 
                        bg="#2d2d44", fg="white", insertbackground="white")
    ent_harga.grid(row=2, column=1, padx=10, pady=8)
    ent_harga.insert(0, str(safe_get(row, "harga", 0)))

    # Stok
    tk.Label(input_frame, text="Stok *", bg="#1e1e2e", 
             font=("Arial", 10), fg="#b19cd9").grid(row=3, column=0, sticky="w", pady=8)
    ent_stok = tk.Entry(input_frame, width=30, font=("Arial", 10), 
                       bg="#2d2d44", fg="white", insertbackground="white")
    ent_stok.grid(row=3, column=1, padx=10, pady=8)
    
    # Tampilkan stok sesuai satuan asli
    displayed_stok = safe_get(row, "stok", 0)
    satuan_sekarang = safe_get(row, "satuan", "pcs")
    if satuan_sekarang in KONVERSI:
        displayed_stok = safe_get(row, "stok", 0) // KONVERSI[satuan_sekarang]
    ent_stok.insert(0, str(displayed_stok))

    # Satuan
    tk.Label(input_frame, text="Satuan *", bg="#1e1e2e", 
             font=("Arial", 10), fg="#b19cd9").grid(row=4, column=0, sticky="w", pady=8)
    ent_satuan = ttk.Combobox(input_frame, values=VALID_SATUAN, state="readonly", 
                             width=27, font=("Arial", 10))
    ent_satuan.set(satuan_sekarang)
    ent_satuan.grid(row=4, column=1, padx=10, pady=8)

    def simpan_edit():
        nama = ent_nama.get().strip()
        harga = ent_harga.get().strip()
        stok_in = ent_stok.get().strip()
        satuan_new = ent_satuan.get().strip().lower()

        if not all([nama, harga, stok_in, satuan_new]):
            messagebox.showerror("Error", "Semua kolom harus diisi!")
            return
            
        if satuan_new not in VALID_SATUAN:
            messagebox.showerror("Error", f"Satuan tidak valid. Pilih: {', '.join(VALID_SATUAN)}")
            return
            
        try:
            harga_int = int(harga)
            stok_int = int(stok_in)
            if harga_int < 0 or stok_int < 0:
                messagebox.showerror("Error", "Harga dan Stok tidak boleh negatif!")
                return
        except ValueError:
            messagebox.showerror("Error", "Harga dan Stok harus berupa angka!")
            return

        # Konversi stok ke pcs
        stok_final = to_pcs(stok_int, satuan_new)

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE barang SET nama_barang=?, harga=?, stok=?, satuan=? WHERE id_barang=?",
                (nama, harga_int, stok_final, satuan_new, idb)
            )
            conn.commit()
            messagebox.showinfo("Sukses", "Data barang berhasil diperbarui!")
            win.destroy()
            load_data(tree)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan perubahan:\n{str(e)}")
        finally:
            conn.close()

    # Frame tombol
    btn_frame = tk.Frame(win, bg="#1e1e2e")
    btn_frame.pack(pady=20)

    tk.Button(btn_frame, text="💾 Simpan", command=simpan_edit, 
              bg="#27ae60", fg="white", activebackground="#219653",
              font=("Arial", 10, "bold"), width=15, height=1,
              bd=0, relief="flat").pack(side="left", padx=10)
    
    tk.Button(btn_frame, text="❌ Batal", command=win.destroy, 
              bg="#e74c3c", fg="white", activebackground="#c0392b",
              font=("Arial", 10), width=12, height=1,
              bd=0, relief="flat").pack(side="left", padx=10)

# ---------------------------
#   HAPUS BARANG
# ---------------------------
def hapus_barang(tree):
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Pilih barang yang ingin dihapus!")
        return

    item = tree.item(selected)["values"]
    if not item:
        return
        
    idb = item[0]
    nama = item[1]

    if messagebox.askyesno("Konfirmasi Hapus", f"Yakin ingin menghapus barang:\n'{nama}'?"):
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM barang WHERE id_barang=?", (idb,))
            conn.commit()
            messagebox.showinfo("Sukses", "Barang berhasil dihapus!")
            load_data(tree)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus barang:\n{str(e)}")
        finally:
            conn.close()

# ---------------------------
#   TAMBAH STOK BARANG - FIXED
# ---------------------------
def tambah_stok(tree, entry_id, entry_jumlah):
    idb = entry_id.get().strip()
    jml_raw = entry_jumlah.get().strip()

    if not idb or not jml_raw:
        messagebox.showerror("Error", "ID Barang dan jumlah harus diisi!")
        return

    try:
        jml = int(jml_raw)
        if jml <= 0:
            messagebox.showerror("Error", "Jumlah harus lebih dari 0!")
            return
    except ValueError:
        messagebox.showerror("Error", "Jumlah harus berupa angka!")
        return

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT stok, nama_barang, satuan FROM barang WHERE id_barang=?", (idb,))
    row = cur.fetchone()

    if row is None:
        messagebox.showerror("Error", "ID Barang tidak ditemukan!")
        conn.close()
        return

    # Konversi jumlah yang diinput ke pcs
    satuan_barang = safe_get(row, "satuan", "pcs")
    tambah = to_pcs(jml, satuan_barang)
    new_stok = safe_get(row, "stok", 0) + tambah

    cur.execute("UPDATE barang SET stok=? WHERE id_barang=?", (new_stok, idb))
    conn.commit()
    conn.close()

    # Peringatan jika stok rendah
    if new_stok <= 5:
        messagebox.showwarning("Peringatan", 
                             f"Stok '{safe_get(row, 'nama_barang', '')}' rendah!\nSisa: {new_stok} pcs")

    messagebox.showinfo("Sukses", f"Stok berhasil ditambahkan!\nStok baru: {new_stok} pcs")
    load_data(tree)
    entry_jumlah.delete(0, tk.END)

# ---------------------------
#   HALAMAN UTAMA STOK - DARK THEME
# ---------------------------
def open_stok_barang():
    win = tk.Toplevel()
    win.title("Manajemen Stok Barang")
    win.geometry("1000x650")
    win.configure(bg="#1e1e2e")

    # Header
    header_frame = tk.Frame(win, bg="#520c61", height=80)
    header_frame.pack(fill="x", padx=0, pady=0)
    header_frame.pack_propagate(False)

    tk.Label(header_frame, text="📦 MANAJEMEN STOK BARANG", 
             font=("Arial", 18, "bold"), bg="#520c61", fg="white").pack(expand=True)

    # Search frame
    search_frame = tk.Frame(win, bg="#2d2d44")
    search_frame.pack(fill="x", padx=20, pady=15)

    tk.Label(search_frame, text="Cari Barang:", font=("Arial", 11, "bold"), 
             bg="#2d2d44", fg="#b19cd9").pack(side="left", padx=(0, 10))
    
    search_var = tk.StringVar()
    ent_search = tk.Entry(search_frame, textvariable=search_var, width=40, 
                         font=("Arial", 10), bg="#3a3a5d", fg="white",
                         insertbackground="white")
    ent_search.pack(side="left")
    ent_search.bind("<Return>", lambda e: load_data(tree, search_var.get()))

    # Main content frame
    main_frame = tk.Frame(win, bg="#2d2d44")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Treeview
    tree_frame = tk.Frame(main_frame, bg="#2d2d44")
    tree_frame.pack(fill="both", expand=True)

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
    
    cols = ("ID", "Nama Barang", "Harga (Rp)", "Stok (pcs)", "Satuan")
    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", 
                       height=20, style="Custom.Treeview")

    # Configure columns
    tree.heading("ID", text="ID")
    tree.heading("Nama Barang", text="Nama Barang")
    tree.heading("Harga (Rp)", text="Harga (Rp)")
    tree.heading("Stok (pcs)", text="Stok (pcs)")
    tree.heading("Satuan", text="Satuan")

    tree.column("ID", width=80, anchor="center")
    tree.column("Nama Barang", width=400, anchor="w")
    tree.column("Harga (Rp)", width=150, anchor="center")
    tree.column("Stok (pcs)", width=120, anchor="center")
    tree.column("Satuan", width=100, anchor="center")

    # Scrollbar
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=vsb.set)
    vsb.pack(side="right", fill="y")

    tree.pack(side="left", fill="both", expand=True)

    # Configure tags for colors
    tree.tag_configure("merah", background="#ff5252", foreground="white")
    tree.tag_configure("kuning", background="#ffb74d", foreground="black")
    tree.tag_configure("normal", background="#2d2d44", foreground="white")

    # Control panel
    control_frame = tk.Frame(win, bg="#3a3a5d", height=140)
    control_frame.pack(fill="x", padx=20, pady=15)
    control_frame.pack_propagate(False)

    # Left side - Tambah Stok
    left_frame = tk.Frame(control_frame, bg="#3a3a5d")
    left_frame.pack(side="left", fill="both", padx=20, pady=15)

    tk.Label(left_frame, text="➕ Tambah Stok Cepat", font=("Arial", 11, "bold"), 
             bg="#3a3a5d", fg="#b19cd9").grid(row=0, column=0, columnspan=5, pady=(0, 10), sticky="w")

    tk.Label(left_frame, text="ID Barang:", bg="#3a3a5d", 
             font=("Arial", 9), fg="white").grid(row=1, column=0, sticky="w", padx=(0, 5))
    ent_id = tk.Entry(left_frame, width=15, font=("Arial", 9), 
                     bg="#2d2d44", fg="white", insertbackground="white")
    ent_id.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(left_frame, text="Jumlah:", bg="#3a3a5d", 
             font=("Arial", 9), fg="white").grid(row=1, column=2, sticky="w", padx=(10, 5))
    ent_tambah = tk.Entry(left_frame, width=15, font=("Arial", 9), 
                         bg="#2d2d44", fg="white", insertbackground="white")
    ent_tambah.grid(row=1, column=3, padx=5, pady=2)

    btn_style = {
        "font": ("Arial", 9, "bold"),
        "bd": 0,
        "relief": "flat",
        "width": 12,
        "height": 1,
        "cursor": "hand2"
    }
    
    btn_tambah_stok = tk.Button(left_frame, text="➕ Tambah", bg="#27ae60", fg="white",
                               activebackground="#219653", activeforeground="white",
                               command=lambda: tambah_stok(tree, ent_id, ent_tambah),
                               **btn_style)
    btn_tambah_stok.grid(row=1, column=4, padx=10, pady=2)

    # Right side - Action Buttons
    right_frame = tk.Frame(control_frame, bg="#3a3a5d")
    right_frame.pack(side="right", fill="both", padx=20, pady=15)

    # Frame untuk tombol aksi
    action_frame = tk.Frame(right_frame, bg="#3a3a5d")
    action_frame.pack(expand=True)

    btn_main_style = {
        "font": ("Arial", 10, "bold"),
        "bd": 0,
        "relief": "flat",
        "width": 15,
        "height": 1,
        "cursor": "hand2"
    }

    btn_add = tk.Button(action_frame, text="➕ Tambah Barang", bg="#2980b9", fg="white",
                       activebackground="#3498db", activeforeground="white",
                       command=lambda: tambah_barang(tree), **btn_main_style)
    btn_add.grid(row=0, column=0, padx=8, pady=5, sticky="ew")

    btn_edit = tk.Button(action_frame, text="✏️ Edit Barang", bg="#f39c12", fg="white",
                        activebackground="#f1c40f", activeforeground="white",
                        command=lambda: edit_barang(tree), **btn_main_style)
    btn_edit.grid(row=0, column=1, padx=8, pady=5, sticky="ew")

    btn_delete = tk.Button(action_frame, text="🗑️ Hapus Barang", bg="#e74c3c", fg="white",
                          activebackground="#c0392b", activeforeground="white",
                          command=lambda: hapus_barang(tree), **btn_main_style)
    btn_delete.grid(row=0, column=2, padx=8, pady=5, sticky="ew")

    # Bind events
    def on_tree_select(event):
        selected = tree.focus()
        if selected:
            item = tree.item(selected)["values"]
            if item:
                ent_id.delete(0, tk.END)
                ent_id.insert(0, str(item[0]))

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    def on_search_change(*args):
        load_data(tree, search_var.get())

    search_var.trace("w", on_search_change)

    # Load initial data
    load_data(tree)

    # Focus on search box
    ent_search.focus()

    return win