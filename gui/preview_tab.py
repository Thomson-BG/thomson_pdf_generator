import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from core.pdf_handler import PDFHandler
import fitz  # PyMuPDF

class PreviewTab:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.pdf_handler = PDFHandler()
        self.current_pdf_path = None
        self.current_page = 0
        self.zoom_factor = 1.0

        self._setup_ui()

    def _setup_ui(self):
        self.main_frame = ctk.CTkFrame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Toolbar
        self.toolbar = ctk.CTkFrame(self.main_frame)
        self.toolbar.pack(fill=tk.X, pady=5, padx=5)

        self.prev_button = ctk.CTkButton(self.toolbar, text="< Prev", command=self.prev_page, state="disabled")
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.page_label = ctk.CTkLabel(self.toolbar, text="Page 0/0")
        self.page_label.pack(side=tk.LEFT, padx=5)

        self.next_button = ctk.CTkButton(self.toolbar, text="Next >", command=self.next_page, state="disabled")
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.zoom_in_button = ctk.CTkButton(self.toolbar, text="+", command=self.zoom_in, state="disabled")
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = ctk.CTkButton(self.toolbar, text="-", command=self.zoom_out, state="disabled")
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        # Canvas for PDF rendering
        self.canvas = tk.Canvas(self.main_frame, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def load_pdf(self, file_path):
        self.current_pdf_path = file_path
        if self.pdf_handler.open_pdf(self.current_pdf_path):
            self.current_page = 0
            self.update_preview()
            self.update_toolbar()

    def update_preview(self):
        if not self.pdf_handler.current_pdf:
            return

        page = self.pdf_handler.current_pdf.load_page(self.current_page)
        mat = fitz.Matrix(self.zoom_factor, self.zoom_factor)
        pix = page.get_pixmap(matrix=mat)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        self.photo_image = ImageTk.PhotoImage(image=img)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def update_toolbar(self):
        if self.pdf_handler.current_pdf:
            num_pages = self.pdf_handler.get_page_count()
            self.page_label.configure(text=f"Page {self.current_page + 1}/{num_pages}")

            self.prev_button.configure(state="normal" if self.current_page > 0 else "disabled")
            self.next_button.configure(state="normal" if self.current_page < num_pages - 1 else "disabled")
            self.zoom_in_button.configure(state="normal")
            self.zoom_out_button.configure(state="normal")
        else:
            self.page_label.configure(text="Page 0/0")
            self.prev_button.configure(state="disabled")
            self.next_button.configure(state="disabled")
            self.zoom_in_button.configure(state="disabled")
            self.zoom_out_button.configure(state="disabled")

    def next_page(self):
        if self.pdf_handler.current_pdf and self.current_page < self.pdf_handler.get_page_count() - 1:
            self.current_page += 1
            self.update_preview()
            self.update_toolbar()

    def prev_page(self):
        if self.pdf_handler.current_pdf and self.current_page > 0:
            self.current_page -= 1
            self.update_preview()
            self.update_toolbar()

    def zoom_in(self):
        self.zoom_factor *= 1.2
        self.update_preview()

    def zoom_out(self):
        self.zoom_factor /= 1.2
        self.update_preview()

    def get_preview_panel(self):
        return self.main_frame
