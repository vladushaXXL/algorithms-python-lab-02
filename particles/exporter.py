import openpyxl
from openpyxl.styles import Font

def save_results_to_excel(particle_name: str, specific_charge: float, compton_wl: float, filename="report.xlsx"):
    """Сохраняет результаты расчетов в файл Excel."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Результаты расчетов"

    # Заголовки
    headers = ["Параметр", "Значение"]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    # Данные
    ws.append(["Частица", particle_name])
    ws.append(["Удельный заряд (Кл/кг)", specific_charge])
    ws.append(["Комптоновская длина волны (м)", compton_wl])

    # Автоширина столбцов
    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 25

    wb.save(filename)
    return filename