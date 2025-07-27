from calendar import monthrange
from datetime import datetime
from fpdf import FPDF


# Imposta il mese e l'anno desiderati
today = datetime.today()
year = today.year
month = today.month

# Definizione annaffiature regolari
watering_schedule = {
    "Monday": ["Origano", "Timo", "Salvia"],
    "Thursday": ["Origano", "Timo", "Salvia"],
    "Saturday": ["Rosmarino*"],
}
daily = ["Basilico", "Menta spicata"]

# Giorni e numero di giorni nel mese
days = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
days_in_month = monthrange(year, month)[1]
start_date = datetime(year, month, 1)

# Dimensioni celle
cell_w = 40
cell_h = 30

# Crea PDF
pdf = FPDF(orientation="L", format="A4")
pdf.add_page()
pdf.set_font("Arial", "B", 16)
pdf.cell(0, 10, f"Calendario di Annaffiatura - Luglio {year}", ln=True, align="C")

# Intestazione giorni della settimana
pdf.set_font("Arial", "B", 12)
for day in days:
    pdf.cell(cell_w, 10, day, border=1, align="C")
pdf.ln()

# Posizionamento celle
pdf.set_font("Arial", "", 10)
week_day_index = start_date.weekday()  # giorno della settimana del 1° giorno del mese

# Celle vuote prima del primo giorno
for i in range(week_day_index):
    pdf.cell(cell_w, cell_h, "", border=1)

day_of_week = week_day_index

# Riempimento celle giorno per giorno
line_height = 4  # altezza riga testo
cell_h_min = 30  # altezza minima cella

for day in range(1, days_in_month + 1):
    current_date = datetime(year, month, day)
    weekday = current_date.strftime("%A")

    # Piante da annaffiare oggi (uniche e ordinate)
    plants_today = watering_schedule.get(weekday, []) + daily
    unique_plants = sorted(set(plants_today))

    # Calcola altezza cella in base al numero di righe (1 per giorno + righe piante)
    # n_lines = 1 + len(unique_plants)
    # cell_h = max(cell_h_min, n_lines * line_height + 4)  # +4 per padding verticale

    # Posizione corrente
    x = pdf.get_x()
    y = pdf.get_y()

    # Disegna il bordo della cella
    pdf.rect(x, y, cell_w, cell_h)

    # Scrivi il numero del giorno in alto a sinistra (grassetto)
    pdf.set_xy(x + 2, y + 2)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(cell_w - 4, line_height, str(day), ln=0)

    # Scrivi le piante da annaffiare un po' più in basso
    pdf.set_xy(x + 2, y + 4 + line_height)
    pdf.set_font("Arial", "", 8)
    for plant in unique_plants:
        pdf.cell(cell_w - 4, line_height, plant, ln=0)  # ln=0 = resta sulla stessa riga
        pdf.set_xy(x + 2, pdf.get_y() + line_height)

    # Passa alla cella successiva sulla stessa riga
    pdf.set_xy(x + cell_w, y)

    day_of_week += 1
    if day_of_week > 6:
        day_of_week = 0
        pdf.ln(cell_h)

# Salva PDF
pdf_path = "Calendario_Annaffiature.pdf"
pdf.output(pdf_path)
pdf_path
