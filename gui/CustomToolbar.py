from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os
from fpdf import FPDF

class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas, parent, var_nombre_tentativo):
        # var_nombre_tentativo -> cambiar nombre a futuro dependiendo del uso 
        self.var_nombre_tentativo = var_nombre_tentativo.replace("/", " - ")
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to  previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
            (None, None, None, None),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
            ('Save', 'Export to PDF', 'filesave', 'my_icon_callback'),
        )
        NavigationToolbar2Tk.__init__(self, canvas, parent)

    def my_icon_callback(self):
        # Write your custom functionality here
        #print("My custom icon was clicked!")
        
        #self.canvas.figure.axes[1]
        extent = self.canvas.figure.axes[1].get_window_extent().transformed(self.canvas.figure.dpi_scale_trans.inverted())
        #fig.savefig('ax2_figure.png', bbox_inches=extent)
        #
        ## Pad the saved area by 10% in the x-direction and 20% in the y-direction
        self.canvas.figure.savefig('ax2_figure_expanded.png', bbox_inches=extent.expanded(1.1, 1.2))

        # Guardar el gráfico en un archivo png
        self.canvas.figure.savefig("signal.png")
        #fig.savefig("signal.png")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        #fpdf.cell(w, h = 0, txt = '', border = 0, ln = 0, align = '', fill = False, link = '')
        #pdf.cell(40, 10, 'Área 2 - Máquina 4 - Zona 8 - Punto 9.', 0, 20)
        pdf.cell(40, 10, self.var_nombre_tentativo, 0, 20)
        #pdf.cell(40, 10, 'Área 2 - Máquina 4 - Zona 8 - Punto 9.', 0, 1, 'C')
        pdf.image('ax2_figure_expanded.png', x = None, y = None, w = 200, h = 0, type = 'png', link = '')
        pdf.ln(h = '')

        # Cabecera de la tabla
        pdf.cell(40,7,'Unidad',1,0,'C')
        pdf.cell(40,7,'Horizontal',1,0,'C')
        pdf.cell(40,7,'Vertical',1,0,'C')
        pdf.cell(40,7,'Axial',1,0,'C')
        pdf.ln(h = '')

        # Datos de la tabla
        pdf.cell(40,7,'G',1,0,'C')
        pdf.cell(40,7,'0,12',1,0,'C')
        pdf.cell(40,7,'0,09',1,0,'C')
        pdf.cell(40,7,'0,05',1,0,'C')
        pdf.ln(h = '')
        pdf.cell(40,7,'GE',1,0,'C')
        pdf.cell(40,7,'0,07',1,0,'C')
        pdf.cell(40,7,'0,06',1,0,'C')
        pdf.cell(40,7,'0,04',1,0,'C')
        pdf.ln(h = '')
        pdf.cell(40,7,'in',1,0,'C')
        pdf.cell(40,7,'0,09',1,0,'C')
        pdf.cell(40,7,'0,12',1,0,'C')
        pdf.cell(40,7,'0,06',1,0,'C')
        pdf.ln(h = '')
        pdf.cell(40,7,'Fahrenheit',1,0,'C')
        pdf.cell(120,7,'78,40',1,0,'C')
        pdf.ln(h = '')
        pdf.ln(h = '')

        # Cabecera de la tabla
        pdf.cell(54,7,'Severidad',1,0,'C')
        pdf.cell(54,7,'Ubicación del daño',1,0,'C')
        pdf.cell(54,7,'Naturaleza del daño',1,0,'C')
        pdf.ln(h = '')

        # Datos de la tabla
        pdf.cell(54,7,'Amarillo',1,0,'C')
        pdf.cell(54,7,'Anillo interno',1,0,'C')
        pdf.cell(54,7,'Desgaste',1,0,'C')
        pdf.ln(h = '')

        pdf.output('tuto1.pdf', 'F')
        os.system('tuto1.pdf')

