from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Spacer
)

class PDFReport:
    def __init__(self, output_path):
        self.output_path = output_path
        self.elements = []
        self.styles = getSampleStyleSheet()

    def add_title(self, text):
        self.elements.append(Paragraph(f"<b>{text}</b>", self.styles["Title"]))
        self.elements.append(Spacer(1, 12))

    def add_paragraph(self, text):
        self.elements.append(Paragraph(text, self.styles["Normal"]))
        self.elements.append(Spacer(1, 10))

    def add_section(self, title):
        self.elements.append(Paragraph(f"<b>{title}</b>", self.styles["Heading2"]))
        self.elements.append(Spacer(1, 10))

    def add_table(self, headers, rows):
        if not rows:
            self.add_paragraph("No se encontraron datos.")
            return

        num_cols = len(headers)

        # Ancho usable de página
        page_width, _ = A4
        usable_width = page_width - 80  # márgenes

        # Detectar columnas largas por nombre
        wide_columns = {"mensaje", "message", "descripcion", "reason"}

        # Peso por columna
        weights = []
        for h in headers:
            if h.lower() in wide_columns:
                weights.append(3)   # columnas largas
            else:
                weights.append(1)   # columnas normales

        total_weight = sum(weights)

        # Calcular anchos finales
        col_widths = [
            usable_width * (w / total_weight)
            for w in weights
        ]

        # Construir tabla con Paragraph (wrap automático)
        table_data = []

        table_data.append([
            Paragraph(f"<b>{h}</b>", self.styles["Normal"])
            for h in headers
        ])

        for row in rows:
            table_data.append([
                Paragraph(str(cell), self.styles["Normal"])
                for cell in row
            ])

        table = Table(
            table_data,
            colWidths=col_widths,
            repeatRows=1
        )

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))

        self.elements.append(table)
        self.elements.append(Spacer(1, 14))

    def save(self):
        doc = SimpleDocTemplate(
            self.output_path,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )
        doc.build(self.elements)