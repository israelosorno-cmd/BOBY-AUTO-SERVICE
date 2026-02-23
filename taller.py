from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", 'B', 16)
pdf.cell(200, 10, "Israel de Jesus Osorno Moreno", ln=True, align='C')
pdf.set_font("Arial", size=10)
pdf.cell(200, 10, "Farmington, UT | (713) 401-8085 | israelosorno@gmail.com", ln=True, align='C')
pdf.ln(10)

pdf.set_font("Arial", 'B', 12)
pdf.cell(200, 10, "PROFESSIONAL SUMMARY", ln=True)
pdf.set_font("Arial", size=10)
pdf.multi_cell(0, 5, "Highly skilled Automotive Technician and Systems Analyst with over 15 years of experience...")

pdf.output("Resume_Israel_Osorno.pdf")
print("¡PDF creado con éxito!")
