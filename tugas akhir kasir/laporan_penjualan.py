import tkinter as tk
from tkinter import ttk, messagebox
from db import get_db
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('Agg')

class LaporanPenjualan:
    def __init__(self, window):
        self.window = window
        self.window.title("Laporan Penjualan & Analisis")
        self.window.geometry("1200x800")
        self.window.configure(bg="#1e1e2e")
    
        # Variabel untuk menyimpan canvas
        self.canvas = None
        self.current_figure = None
        
        self.setup_ui()
        self.load_initial_data()
    
    def setup_ui(self):
        # Notebook (Tab)
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Laporan Transaksi
        self.tab1 = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(self.tab1, text="📋 Laporan Transaksi")
        
        # Tab 2: Analisis Penjualan
        self.tab2 = tk.Frame(self.notebook, bg="#1e1e2e")
        self.notebook.add(self.tab2, text="📊 Analisis Penjualan")
        
        self.setup_tab1()
        self.setup_tab2()
    
    def setup_tab1(self):
        # Header
        header_frame = tk.Frame(self.tab1, bg="#520c61", height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="LAPORAN TRANSAKSI", font=("Arial", 18, "bold"), 
                 bg="#520c61", fg="white").pack(expand=True)
        
        # Filter frame
        filter_frame = tk.Frame(self.tab1, bg="#2d2d44")
        filter_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Label(filter_frame, text="Filter Tanggal:", font=("Arial", 11, "bold"), 
                 bg="#2d2d44", fg="#b19cd9").pack(side="left", padx=(0, 10))
        
        # Tanggal mulai
        tk.Label(filter_frame, text="Dari:", bg="#2d2d44", fg="white").pack(side="left", padx=(0, 5))
        self.start_date = tk.Entry(filter_frame, width=12, bg="#3a3a5d", fg="white", 
                                  insertbackground="white", font=("Arial", 10))
        self.start_date.pack(side="left", padx=5)
        self.start_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        
        # Tanggal akhir
        tk.Label(filter_frame, text="Sampai:", bg="#2d2d44", fg="white").pack(side="left", padx=(10, 5))
        self.end_date = tk.Entry(filter_frame, width=12, bg="#3a3a5d", fg="white",
                               insertbackground="white", font=("Arial", 10))
        self.end_date.pack(side="left", padx=5)
        self.end_date.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        
        btn_style = {
            "font": ("Arial", 10, "bold"),
            "bd": 0,
            "relief": "flat",
            "width": 12,
            "height": 1,
            "cursor": "hand2"
        }
        
        btn_filter = tk.Button(filter_frame, text="🔍 Filter", bg="#3498db", fg="white",
                              activebackground="#2980b9", activeforeground="white",
                              command=self.filter_laporan, **btn_style)
        btn_filter.pack(side="left", padx=10)
        
        btn_refresh = tk.Button(filter_frame, text="🔄 Refresh", bg="#27ae60", fg="white",
                               activebackground="#219653", activeforeground="white",
                               command=self.refresh_laporan, **btn_style)
        btn_refresh.pack(side="left", padx=5)
        
        # Main content
        main_frame = tk.Frame(self.tab1, bg="#2d2d44")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Treeview dengan style dark
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
        
        self.tree = ttk.Treeview(main_frame, columns=("No", "Tanggal", "Kasir", "Barang", "Jumlah", "Harga Satuan", "Total"), 
                               show="headings", height=15, style="Custom.Treeview")
        
        self.tree.heading("No", text="No")
        self.tree.heading("Tanggal", text="Tanggal")
        self.tree.heading("Kasir", text="Kasir")
        self.tree.heading("Barang", text="Barang")
        self.tree.heading("Jumlah", text="Jumlah")
        self.tree.heading("Harga Satuan", text="Harga Satuan")
        self.tree.heading("Total", text="Total")
        
        self.tree.column("No", width=50, anchor="center")
        self.tree.column("Tanggal", width=150, anchor="center")
        self.tree.column("Kasir", width=120, anchor="center")
        self.tree.column("Barang", width=250, anchor="w")
        self.tree.column("Jumlah", width=80, anchor="center")
        self.tree.column("Harga Satuan", width=100, anchor="center")
        self.tree.column("Total", width=120, anchor="center")
        
        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Total frame
        self.total_frame = tk.Frame(self.tab1, bg="#520c61", height=60)
        self.total_frame.pack(fill="x", padx=20, pady=10)
        self.total_frame.pack_propagate(False)
        
        self.total_label = tk.Label(self.total_frame, text="Total Penjualan: Rp 0", 
                                  font=("Arial", 14, "bold"), bg="#520c61", fg="#FFD700")
        self.total_label.pack(side="right", padx=20, pady=10)
    
    def setup_tab2(self):
        # Header
        header_frame = tk.Frame(self.tab2, bg="#520c61", height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="ANALISIS PENJUALAN", font=("Arial", 18, "bold"), 
                 bg="#520c61", fg="white").pack(expand=True)
        
        # Filter untuk analisis
        analysis_filter_frame = tk.Frame(self.tab2, bg="#2d2d44")
        analysis_filter_frame.pack(fill="x", padx=20, pady=15)
        
        tk.Label(analysis_filter_frame, text="Periode Analisis:", font=("Arial", 11, "bold"), 
                 bg="#2d2d44", fg="#b19cd9").pack(side="left", padx=(0, 10))
        
        # Tanggal mulai analisis
        tk.Label(analysis_filter_frame, text="Dari:", bg="#2d2d44", fg="white").pack(side="left", padx=(0, 5))
        self.analysis_start = tk.Entry(analysis_filter_frame, width=12, bg="#3a3a5d", fg="white",
                                      insertbackground="white", font=("Arial", 10))
        self.analysis_start.pack(side="left", padx=5)
        self.analysis_start.insert(0, (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d"))
        
        # Tanggal akhir analisis
        tk.Label(analysis_filter_frame, text="Sampai:", bg="#2d2d44", fg="white").pack(side="left", padx=(10, 5))
        self.analysis_end = tk.Entry(analysis_filter_frame, width=12, bg="#3a3a5d", fg="white",
                                    insertbackground="white", font=("Arial", 10))
        self.analysis_end.pack(side="left", padx=5)
        self.analysis_end.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        
        btn_style = {
            "font": ("Arial", 10, "bold"),
            "bd": 0,
            "relief": "flat",
            "width": 15,
            "height": 1,
            "cursor": "hand2"
        }
        
        btn_analyze = tk.Button(analysis_filter_frame, text="📊 Update Diagram", bg="#9b59b6", fg="white",
                               activebackground="#8e44ad", activeforeground="white",
                               command=self.update_all_charts, **btn_style)
        btn_analyze.pack(side="left", padx=10)
        
        btn_auto_refresh = tk.Button(analysis_filter_frame, text="🔄 Auto Refresh", bg="#f39c12", fg="white",
                                    activebackground="#e67e22", activeforeground="white",
                                    command=self.toggle_auto_refresh, **btn_style)
        btn_auto_refresh.pack(side="left", padx=5)
        
        # Status auto refresh
        self.auto_refresh_var = tk.BooleanVar(value=False)
        self.auto_refresh_label = tk.Label(analysis_filter_frame, text="Auto Refresh: OFF", 
                                          bg="#2d2d44", fg="#e74c3c", font=("Arial", 10, "bold"))
        self.auto_refresh_label.pack(side="left", padx=10)
        
        # Frame untuk chart
        self.chart_frame = tk.Frame(self.tab2, bg="#2d2d44")
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    def load_initial_data(self):
        self.load_laporan()
        self.update_all_charts()
    
    def load_laporan(self, start=None, end=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        conn = get_db()
        cur = conn.cursor()
        
        query = """
            SELECT tgl, nama_pegawai, nama_barang, jumlah, 
                   total_harga/jumlah as harga_satuan, total_harga 
            FROM transaksi 
        """
        params = []
        
        if start and end:
            query += " WHERE date(tgl) BETWEEN ? AND ?"
            params = [start, end]
        
        query += " ORDER BY tgl DESC"
        
        cur.execute(query, params)
        data = cur.fetchall()
        conn.close()
        
        total_penjualan = 0
        for i, item in enumerate(data, 1):
            self.tree.insert(
                "",
                "end",
                values=(
                    i,
                    item["tgl"],
                    item["nama_pegawai"],
                    item["nama_barang"],
                    item["jumlah"],
                    f"Rp {item['harga_satuan']:,.0f}",
                    f"Rp {item['total_harga']:,}"
                )
            )
            total_penjualan += item["total_harga"]
        
        self.total_label.config(text=f"Total Penjualan: Rp {total_penjualan:,}")
    
    def filter_laporan(self):
        self.load_laporan(self.start_date.get(), self.end_date.get())
        messagebox.showinfo("Info", "Laporan telah difilter!")
    
    def refresh_laporan(self):
        self.load_laporan()
        messagebox.showinfo("Info", "Laporan telah direfresh!")
    
    def get_sales_analysis(self, start_date, end_date):
        """Mendapatkan data analisis penjualan terbaru"""
        conn = get_db()
        cur = conn.cursor()
        
        # Produk terlaris
        cur.execute("""
            SELECT nama_barang, SUM(jumlah) as total_terjual, SUM(total_harga) as total_pendapatan
            FROM transaksi 
            WHERE date(tgl) BETWEEN ? AND ?
            GROUP BY nama_barang 
            ORDER BY total_terjual DESC
            LIMIT 10
        """, (start_date, end_date))
        top_products = cur.fetchall()
        
        # Penjualan per hari
        cur.execute("""
            SELECT date(tgl) as tanggal, SUM(total_harga) as total_harian
            FROM transaksi 
            WHERE date(tgl) BETWEEN ? AND ?
            GROUP BY date(tgl)
            ORDER BY tanggal
        """, (start_date, end_date))
        daily_sales = cur.fetchall()
        
        # Penjualan per kasir
        cur.execute("""
            SELECT nama_pegawai, SUM(total_harga) as total_penjualan
            FROM transaksi 
            WHERE date(tgl) BETWEEN ? AND ?
            GROUP BY nama_pegawai
            ORDER BY total_penjualan DESC
        """, (start_date, end_date))
        sales_by_cashier = cur.fetchall()
        
        conn.close()
        
        return {
            'top_products': top_products,
            'daily_sales': daily_sales,
            'sales_by_cashier': sales_by_cashier,
            'period': f"{start_date} hingga {end_date}"
        }
    
    def update_all_charts(self):
        """Update semua diagram dengan data terbaru"""
        try:
            # Dapatkan data terbaru
            analysis_data = self.get_sales_analysis(
                self.analysis_start.get(), 
                self.analysis_end.get()
            )
            
            # Hapus chart sebelumnya
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            if self.current_figure:
                plt.close(self.current_figure)
            
            # Buat chart baru
            self.create_charts(analysis_data)
            
            # Refresh label
            status_text = "Auto Refresh: ON" if self.auto_refresh_var.get() else "Auto Refresh: OFF"
            status_color = "#27ae60" if self.auto_refresh_var.get() else "#e74c3c"
            self.auto_refresh_label.config(text=status_text, fg=status_color)
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal update diagram: {str(e)}")
    
    def create_charts(self, analysis_data):
        """Buat diagram dengan layout yang RAPI dan TERORGANISIR"""
        # Hapus widget sebelumnya
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        if not analysis_data['top_products']:
            tk.Label(self.chart_frame, text="📊 Tidak ada data penjualan untuk periode yang dipilih", 
                    font=("Arial", 12), bg="#2d2d44", fg="white").pack(expand=True)
            return
        
        # Buat frame utama untuk diagram
        main_diagram_frame = tk.Frame(self.chart_frame, bg="#2d2d44")
        main_diagram_frame.pack(fill="both", expand=True)
        
        # Frame untuk baris pertama (2 diagram)
        row1_frame = tk.Frame(main_diagram_frame, bg="#2d2d44")
        row1_frame.pack(fill="both", expand=True, pady=5)
        
        # Frame untuk baris kedua (2 diagram)
        row2_frame = tk.Frame(main_diagram_frame, bg="#2d2d44")
        row2_frame.pack(fill="both", expand=True, pady=5)
        
        # ========== DIAGRAM 1: PRODUK TERLARIS ==========
        fig1 = plt.Figure(figsize=(6, 4), dpi=80, facecolor='#2d2d44')
        ax1 = fig1.add_subplot(111, facecolor='#2d2d44')
        
        # Siapkan data
        products = []
        for item in analysis_data['top_products'][:8]:
            name = item['nama_barang']
            if len(name) > 25:
                name = name[:25] + "..."
            products.append(name)
        
        quantities = [item['total_terjual'] for item in analysis_data['top_products'][:8]]
        
        # Buat horizontal bar chart
        y_pos = range(len(products))
        colors = ['#9b59b6', '#3498db', '#2ecc71', '#f1c40f', '#e74c3c', '#1abc9c', '#34495e', '#95a5a6']
        bars = ax1.barh(y_pos, quantities, color=colors[:len(products)], height=0.6)
        
        ax1.set_title('PRODUK TERLARIS', fontsize=12, fontweight='bold', pad=10, color='white')
        ax1.set_xlabel('Jumlah Terjual', fontsize=9, color='white')
        ax1.set_ylabel('Produk', fontsize=9, color='white')
        ax1.set_yticks(y_pos)
        ax1.set_yticklabels(products, fontsize=8, color='white')
        ax1.tick_params(axis='x', colors='white')
        ax1.tick_params(axis='y', colors='white')
        ax1.grid(True, alpha=0.3, axis='x', color='#555555')
        
        # Tambah nilai di bar
        for bar, value in zip(bars, quantities):
            ax1.text(bar.get_width() + max(quantities)*0.02, bar.get_y() + bar.get_height()/2, 
                    f'{value}', ha='left', va='center', fontsize=8, fontweight='bold', color='white')
        
        # Set border color
        ax1.spines['bottom'].set_color('white')
        ax1.spines['top'].set_color('white')
        ax1.spines['right'].set_color('white')
        ax1.spines['left'].set_color('white')
        
        fig1.tight_layout(rect=[0, 0, 1, 0.96])
        
        # ========== DIAGRAM 2: PIE CHART PENDAPATAN ==========
        fig2 = plt.Figure(figsize=(6, 4), dpi=80, facecolor='#2d2d44')
        ax2 = fig2.add_subplot(111, facecolor='#2d2d44')
        
        # Siapkan data untuk pie chart (maksimal 6 item)
        product_names = []
        revenues = []
        total_items = min(6, len(analysis_data['top_products']))
        
        for i in range(total_items):
            item = analysis_data['top_products'][i]
            name = item['nama_barang']
            if len(name) > 20:
                name = name[:20] + "..."
            product_names.append(name)
            revenues.append(item['total_pendapatan'])
        
        # Warna untuk pie chart
        colors = ['#9b59b6', '#3498db', '#2ecc71', '#f1c40f', '#e74c3c', '#1abc9c']
        
        # Buat pie chart
        wedges, texts, autotexts = ax2.pie(
            revenues, 
            labels=product_names, 
            autopct=lambda p: f'{p:.1f}%' if p > 5 else '',
            startangle=90, 
            colors=colors[:total_items],
            textprops={'fontsize': 8, 'color': 'white'}
        )
        
        # Style persentase
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(8)
        
        ax2.set_title('DISTRIBUSI PENDAPATAN', fontsize=12, fontweight='bold', pad=10, color='white')
        
        # Tambah total pendapatan
        total_revenue = sum(revenues)
        ax2.text(0, 0, f'Total:\nRp {total_revenue:,.0f}', 
                ha='center', va='center', fontsize=9, fontweight='bold', style='italic', color='white')
        
        fig2.tight_layout(rect=[0, 0, 1, 0.96])
        
        # ========== DIAGRAM 3: TREND PENJUALAN HARIAN ==========
        fig3 = plt.Figure(figsize=(6, 4), dpi=80, facecolor='#2d2d44')
        ax3 = fig3.add_subplot(111, facecolor='#2d2d44')
        
        if analysis_data['daily_sales']:
            dates = [datetime.datetime.strptime(item['tanggal'], '%Y-%m-%d').strftime('%d/%m') 
                    for item in analysis_data['daily_sales'][-10:]]
            daily_totals = [item['total_harian'] for item in analysis_data['daily_sales'][-10:]]
            
            # Buat line chart
            ax3.plot(dates, daily_totals, marker='o', linewidth=2, color='#e74c3c', markersize=6)
            ax3.fill_between(dates, daily_totals, alpha=0.2, color='#e74c3c')
            ax3.set_title('TREND PENJUALAN HARIAN', fontsize=12, fontweight='bold', pad=10, color='white')
            ax3.set_xlabel('Tanggal', fontsize=9, color='white')
            ax3.set_ylabel('Pendapatan (Rp)', fontsize=9, color='white')
            ax3.tick_params(axis='x', rotation=45, labelsize=7, colors='white')
            ax3.tick_params(axis='y', labelsize=7, colors='white')
            ax3.grid(True, alpha=0.3, color='#555555')
            
            # Format y-axis
            ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Rp {x:,.0f}'))
            
            # Set border color
            ax3.spines['bottom'].set_color('white')
            ax3.spines['top'].set_color('white')
            ax3.spines['right'].set_color('white')
            ax3.spines['left'].set_color('white')
            
            # Highlight titik tertinggi
            if daily_totals:
                max_idx = daily_totals.index(max(daily_totals))
                ax3.annotate(f'Puncak\nRp {daily_totals[max_idx]:,}', 
                            xy=(dates[max_idx], daily_totals[max_idx]),
                            xytext=(10, 10), textcoords='offset points',
                            fontsize=7, color='white',
                            bbox=dict(boxstyle='round,pad=0.3', facecolor='#9b59b6', alpha=0.8),
                            arrowprops=dict(arrowstyle='->', color='white', lw=1))
        
        else:
            ax3.text(0.5, 0.5, 'Tidak ada data\ntrend harian', 
                    ha='center', va='center', transform=ax3.transAxes, fontsize=10, color='white')
            ax3.set_title('TREND PENJUALAN HARIAN', fontsize=12, fontweight='bold', pad=10, color='white')
        
        fig3.tight_layout(rect=[0, 0, 1, 0.96])
        
        # ========== DIAGRAM 4: PENJUALAN PER KASIR ==========
        fig4 = plt.Figure(figsize=(6, 4), dpi=80, facecolor='#2d2d44')
        ax4 = fig4.add_subplot(111, facecolor='#2d2d44')
        
        if analysis_data['sales_by_cashier']:
            cashiers = [item['nama_pegawai'] for item in analysis_data['sales_by_cashier']]
            cashier_sales = [item['total_penjualan'] for item in analysis_data['sales_by_cashier']]
            
            # Buat bar chart
            x_pos = range(len(cashiers))
            bars = ax4.bar(x_pos, cashier_sales, color='#3498db', width=0.6)
            
            ax4.set_title('PENJUALAN PER KASIR', fontsize=12, fontweight='bold', pad=10, color='white')
            ax4.set_ylabel('Total Penjualan (Rp)', fontsize=9, color='white')
            ax4.set_xticks(x_pos)
            ax4.set_xticklabels(cashiers, fontsize=8, rotation=45, ha='right', color='white')
            ax4.tick_params(axis='y', colors='white')
            ax4.grid(True, alpha=0.3, axis='y', color='#555555')
            
            # Format y-axis
            ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'Rp {x:,.0f}'))
            
            # Set border color
            ax4.spines['bottom'].set_color('white')
            ax4.spines['top'].set_color('white')
            ax4.spines['right'].set_color('white')
            ax4.spines['left'].set_color('white')
            
            # Tambah nilai di atas bar
            for bar, value in zip(bars, cashier_sales):
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + max(cashier_sales)*0.01,
                        f'Rp {value:,.0f}', ha='center', va='bottom', 
                        fontsize=7, fontweight='bold', rotation=0, color='white')
        
        else:
            ax4.text(0.5, 0.5, 'Tidak ada data\npenjualan kasir', 
                    ha='center', va='center', transform=ax4.transAxes, fontsize=10, color='white')
            ax4.set_title('PENJUALAN PER KASIR', fontsize=12, fontweight='bold', pad=10, color='white')
        
        fig4.tight_layout(rect=[0, 0, 1, 0.96])
        
        # ========== TEMPATKAN DIAGRAM DI LAYOUT ==========
        # Baris 1: Produk Terlaris dan Pie Chart
        canvas1 = FigureCanvasTkAgg(fig1, row1_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5)
        
        canvas2 = FigureCanvasTkAgg(fig2, row1_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="right", fill="both", expand=True, padx=5)
        
        # Baris 2: Trend Harian dan Penjualan Kasir
        canvas3 = FigureCanvasTkAgg(fig3, row2_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side="left", fill="both", expand=True, padx=5)
        
        canvas4 = FigureCanvasTkAgg(fig4, row2_frame)
        canvas4.draw()
        canvas4.get_tk_widget().pack(side="right", fill="both", expand=True, padx=5)
        
        # ========== TIMESTAMP ==========
        timestamp_frame = tk.Frame(self.chart_frame, bg="#2d2d44")
        timestamp_frame.pack(side="bottom", fill="x", pady=5)
        
        timestamp = datetime.datetime.now().strftime("🕐 Terakhir update: %d/%m/%Y %H:%M:%S")
        timestamp_label = tk.Label(timestamp_frame, text=timestamp, 
                                 font=("Arial", 9), bg="#2d2d44", fg="#b19cd9")
        timestamp_label.pack()
        
        # Simpan referensi canvas
        self.canvas = canvas1
        self.current_figure = fig1
    
    def toggle_auto_refresh(self):
        """Toggle auto refresh setiap 10 detik"""
        self.auto_refresh_var.set(not self.auto_refresh_var.get())
        
        if self.auto_refresh_var.get():
            self.auto_refresh_label.config(text="Auto Refresh: ON", fg="#27ae60")
            self.start_auto_refresh()
        else:
            self.auto_refresh_label.config(text="Auto Refresh: OFF", fg="#e74c3c")
    
    def start_auto_refresh(self):
        """Mulai auto refresh"""
        if self.auto_refresh_var.get():
            self.update_all_charts()
            # Schedule refresh berikutnya dalam 10 detik
            self.window.after(10000, self.start_auto_refresh)

def open_laporan_penjualan():
    try:
        win = tk.Toplevel()
        app = LaporanPenjualan(win)
        return win
    except Exception as e:
        messagebox.showerror("Error", f"Gagal membuka laporan: {str(e)}")
        return None

# Untuk testing
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    open_laporan_penjualan()
    root.mainloop()