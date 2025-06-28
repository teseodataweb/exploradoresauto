from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import json


class PDF(FPDF):

    def add_property_details(self, image_path, property_data):
        # Configurar márgenes FIJOS
        margin = 20
        self.set_left_margin(margin)
        self.set_right_margin(margin)
        self.set_top_margin(20)
        self.set_auto_page_break(auto=True, margin=20)
                
        available_width = self.w - (2 * margin) # ancho disponible respetando márgenes
        
        # Proporción de columnas (60% - 40%)
        left_column_width = available_width * 0.60  
        right_column_width = available_width * 0.40 
            
        initial_y = 85 # Posición Y inicial
        
        # Imagen de la propiedad (columna izquierda) - RESPETANDO MÁRGENES
        image_height = 100
        self.image(image_path, x=margin, y=initial_y, w=left_column_width - 7, h=image_height)
        
        # línea divisoria - POSICIÓN CORRECTA
        self.set_draw_color(100,149,237)  
        line_x = margin + left_column_width
        self.line(line_x, initial_y, line_x, initial_y + image_height)
        
        # Detalles de la propiedad (columna derecha) - RESPETANDO MÁRGENES
        x_second_column = margin + left_column_width + 7        
        
        # Ubicación
        self.set_xy(x_second_column, initial_y)
        self.set_font('Arial', 'B', 14)
        self.cell(right_column_width - 10, 10, "Ubicación de la propiedad", 0, 1)        
        self.set_xy(x_second_column, initial_y + 10)
        self.set_font('Arial', '', 12)
        # Usar ancho limitado para multi_cell
        self.multi_cell(right_column_width - 10, 5, property_data['ubicacion'], 0, 'L')
        
        # Valor
        self.set_xy(x_second_column, initial_y + 35)
        self.set_font('Arial', 'B', 14)
        self.cell(right_column_width - 10, 10, "Valor de la Propiedad", 0, 1)        
        self.set_xy(x_second_column, initial_y + 45)
        self.set_font('Arial', '', 12)
        self.cell(right_column_width - 10, 10, f"${property_data['Precio']:,}", 0, 1)        
        
        # Fecha
        self.set_xy(x_second_column, initial_y + 60)
        self.set_font('Arial', 'B', 14)
        self.cell(right_column_width - 10, 10, "Fecha", 0, 1)        
        self.set_xy(x_second_column, initial_y + 70)
        self.set_font('Arial', '', 12)
        self.cell(right_column_width - 10, 10, property_data['fecha'], 0, 1)
        
    def header(self):        
        page_width = self.w
        page_height = self.h
        
        # Header para página 1 (portada)
        if self.page_no() == 1:
            image_width = 120
            image_height = 20
            y_logo = 25
            x_logo = (page_width - image_width) / 2
            self.image('tools/DatLogo.png', x_logo, y_logo, image_width)

            self.set_font('Arial', 'B', 25)
            text = "EXPLORADOR DE PROPIEDADES"
            text_width = self.get_string_width(text)
            x_text = (page_width - text_width) / 2
            y_text = y_logo + image_height + 15
            self.text(x_text, y_text, text)

            self.set_font('Arial', 'I', 19)
            text = "Análisis de precios"
            text_width = self.get_string_width(text)
            x_text = (page_width - text_width) / 2
            y_text = y_logo + image_height + 25
            self.text(x_text, y_text, text)
        
        # Header para página 2 y siguientes
        else:
            # El logo tiene ancho=52 y largo=11 (alto=11)
            # Logo en esquina izquierda
            self.image('tools/DatLogo.png', 15, 10, 52, 11)
            
            # Fecha en esquina derecha
            self.set_font('Arial', '', 10)
            fecha_text = "Fecha"
            #fecha_numeros = "26/06/2024"
            fecha_numeros = property_data['fecha']
            fecha_width = self.get_string_width(fecha_text)
            self.text(page_width - fecha_width - 20, 15, fecha_text)
            self.set_font('Arial', 'B', 10)
            self.text(page_width - fecha_width - 20, 20, fecha_numeros)

    def footer(self):
        # Solo agregar footer si NO es la página 1 (portada)
        if self.page_no() != 1:
            # Posición del footer
            self.set_y(-17)
            
            # Línea horizontal
            self.set_draw_color(0, 0, 0)  # Color negro para la línea
            margin = 14
            self.line(margin, self.get_y(), self.w - margin, self.get_y())
            
            # Mover un poco hacia abajo después de la línea
            self.set_y(-14)
            
            # Configurar fuente para el footer
            self.set_font('Arial', '', 9)
            self.set_text_color(0, 0, 0)
            
            # Fecha de pedido (izquierda)
            #fecha_pedido = "Fecha de pedido: 19.06.2024"
            #self.set_x(margin)
            #self.cell(0, 10, fecha_pedido, 0, 0, 'L')
            
            # Texto central
            texto_central = "Explorador de propiedades impulsado por"
            text_width = self.get_string_width(texto_central)
            #x_center = (self.w - text_width) / 2
            self.set_x(margin) #x_center
            self.cell(text_width, 10, texto_central, 0, 0, 'C')

            # Logo pequeño después de "por"
            # Ajustar posición X para que el logo quede justo después del texto central
            logo_width = 22  # alargar el logo horizontalmente
            logo_height = 5  # mantener el alto pequeño para el logo
            x_logo = margin + text_width + 1  # pequeño espacio después del texto # x_center
            y_logo = self.get_y() + 2  # centrar verticalmente con el texto
            self.image('tools/DatLogo.png', x=x_logo, y=y_logo, w=logo_width, h=logo_height)
            # Número de página (derecha)
            page_text = f"Pág. {self.page_no()}"
            page_width = self.get_string_width(page_text)
            self.set_x(self.w - margin - page_width)
            self.cell(page_width, 10, page_text, 0, 0, 'R')
    
    def create_price_chart(self, property_value):
        """Crear gráfica de rangos de precios con slider horizontal y precio dinámico"""
        # Datos para el rango de precios
        bajo = 2268500      # Valor mínimo
        medio = property_value  # Valor de la propiedad (dinámico)
        alto = 3800000      # Valor máximo
        
        # Crear la figura
        fig, ax = plt.subplots(figsize=(6, 1.5))
        
        # Posición vertical centrada
        y_pos = 0.5
        
        # Calcular posición relativa del valor medio (ajustada al rango)
        # Aseguramos que 'medio' esté dentro del rango [bajo, alto]
        medio_clipped = max(bajo, min(medio, alto))
        total_range = alto - bajo
        medio_pos = (medio_clipped - bajo) / total_range  # Posición normalizada (0 a 1)
        
        # Dibujar la línea base (track del slider, gris claro)
        line_width = 4
        ax.plot([0, 1], [y_pos, y_pos], color='#E8F4FD', linewidth=line_width, solid_capstyle='round')
        
        # Dibujar la línea activa (azul, hasta el valor medio)
        ax.plot([0, medio_pos], [y_pos, y_pos], color='#4A90E2', linewidth=line_width, solid_capstyle='round')
        
        # Marcador circular en la posición del valor
        ax.scatter(medio_pos, y_pos, color='#4A90E2', s=80, zorder=5, edgecolors='white', linewidth=2)
        
        # Etiquetas fijas en los extremos
        ax.text(0, y_pos - 0.15, 'Bajo', ha='center', va='top', fontsize=9, color='#666666')
        ax.text(1, y_pos - 0.15, 'Alto', ha='center', va='top', fontsize=9, color='#666666')
        
        # Valores fijos en los extremos (Bajo y Alto)
        ax.text(0, y_pos - 0.25, f'${bajo:,.0f}', ha='center', va='top', fontsize=8, color='#888888')
        ax.text(1, y_pos - 0.25, f'${alto:,.0f}', ha='center', va='top', fontsize=8, color='#888888')
        
        # Precio dinámico (se mueve con el marcador)
        ax.text(medio_pos, y_pos + 0.15, f'${medio:,.2f}', ha='center', va='bottom', 
                fontsize=10, color='#4A90E2', weight='bold')
        
        # Configurar límites y aspecto
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        plt.tight_layout()
        
        # Guardar la gráfica
        chart_path = 'price_slider_chart.png'
        plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        return chart_path
    def create_price_chart(self, precio_datalpine, precio_propiedad):
        import matplotlib.pyplot as plt
        import numpy as np

        # Definir el rango
        bajo = 3268500
        alto = 3500000
        total_range = alto - bajo

        # Normalizar los valores
        datalpine_pos = (max(bajo, min(precio_datalpine, alto)) - bajo) / total_range
        propiedad_pos = (max(bajo, min(precio_propiedad, alto)) - bajo) / total_range

        # Crear figura
        fig, ax = plt.subplots(figsize=(6, 1.8))
        y_pos = 0.5

        # Gradiente de color en la barra
        x_vals = np.linspace(0, 1, 500)
        cmap = plt.get_cmap('PuBu')
        for i in range(len(x_vals) - 1):
            ax.plot([x_vals[i], x_vals[i+1]], [y_pos, y_pos],
                    color=cmap(x_vals[i]), linewidth=6, solid_capstyle='butt')

        # Remates extremos
        ax.plot([0, 0], [y_pos - 0.1, y_pos + 0.1], color=cmap(0.2), linewidth=8)
        ax.plot([1, 1], [y_pos - 0.1, y_pos + 0.1], color=cmap(0.9), linewidth=8)

        # Marcadores de los valores
        ax.plot([datalpine_pos], [y_pos], marker='|', markersize=25,
                color='#A020F0', linewidth=2, zorder=5)  # morado
        ax.plot([propiedad_pos], [y_pos], marker='|', markersize=25,
                color='black', linewidth=2, zorder=5)

        # Texto de cada valor: Datalpine ARRIBA del marcador, Propiedad ABAJO del marcador, ambos más cerca de la línea
        ax.text(datalpine_pos, y_pos + 0.13, f"${precio_datalpine:,.2f}",
                ha='center', va='bottom', fontsize=10, color='#A020F0', fontweight='bold')

        ax.text(propiedad_pos, y_pos - 0.13, f"${precio_propiedad:,.2f}",
                ha='center', va='top', fontsize=10, color='black', fontweight='bold')

        # Etiquetas de extremos (con decimales)
        ax.text(0, y_pos - 0.45, f"${bajo:,.2f}", ha='center', va='top', fontsize=9, color='gray')
        ax.text(1, y_pos - 0.45, f"${alto:,.2f}", ha='center', va='top', fontsize=9, color='gray')

        # Texto 'Bajo' y 'Alto'
        ax.text(0, y_pos + 0.12, "Bajo", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#333333')
        ax.text(1, y_pos + 0.12, "Alto", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#333333')

        # Estética
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')

        plt.tight_layout()
        chart_path = 'price_slider_doble_valor.png'
        plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()

        return chart_path


    def add_second_page(self, property_data):
        """Agregar la segunda página con el análisis detallado"""
        # Forzar una nueva página
        self.add_page()
        
        # CONFIGURAR MÁRGENES FIJOS PARA SEGUNDA PÁGINA
        margin = 20
        self.set_left_margin(margin)
        self.set_right_margin(margin)
        self.set_auto_page_break(auto=True, margin=20)
        
        # Dirección como título - RESPETANDO MÁRGENES
        self.set_y(26)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 0, 0)
        
        # Centrar la dirección DENTRO de los márgenes
        direccion = property_data['ubicacion']
        max_width = self.w - (2 * margin)  # Ancho disponible respetando márgenes
        
        # Usar multi_cell para mantener márgenes
        self.set_x(margin)
        self.multi_cell(max_width, 8, direccion, border=0, align='C')
        
        current_y = self.get_y() + 4  # Obtener posición Y después del título
        
        # Sección de precio y gráfica (dos columnas) - RESPETANDO MÁRGENES
        available_width = self.w - (2 * margin)
        left_col_width = available_width * 0.5
        right_col_width = available_width * 0.5
        
        # Columna izquierda - Valor de la propiedad
        self.set_xy(margin, current_y)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(160, 32, 240)  # Color púrpura (#A020F0)
        self.cell(left_col_width, 10, "Precio DatAlpine:", 0, 1)
        
        self.set_xy(margin, current_y + 5)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 0, 0)
        precio_datalpine = f"$ {property_data['precio_datalpine']:,}"
        self.cell(left_col_width, 15, precio_datalpine, 0, 1)
        
        self.set_xy(margin, current_y + 16.5)
        self.set_font('Arial', '', 12)
        self.set_text_color(128, 128, 128)
        self.cell(left_col_width, 10, "Valor de la Propiedad:", 0, 1)
        
        self.set_xy(margin, current_y + 22)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 0, 0)
        precio_text = f"$ {property_data['Precio']:,}"
        self.cell(left_col_width, 10, precio_text, 0, 1)
        
        # Columna derecha - Gráfica - RESPETANDO MÁRGENES
        try:
            #chart_path = self.create_price_chart(property_data['precio_datalpine'])
            chart_path = self.create_price_chart(property_data['precio_datalpine'], property_data['Precio'])
            chart_x = margin + left_col_width + 10
            # Asegurar que la gráfica no se salga de los márgenes
            chart_width = right_col_width - 8
            if chart_x + chart_width > self.w - margin:
                chart_width = self.w - margin - chart_x
            # Subir la gráfica un poco (por ejemplo, 10 unidades arriba)
            self.image(chart_path, chart_x, current_y - 5, chart_width, 30)
        except Exception as e:
            print(f"Error creando gráfica: {e}")
            # Si falla la gráfica, agregar texto alternativo
            self.set_xy(chart_x, current_y + 10)
            self.set_font('Arial', '', 10)
            self.cell(right_col_width - 10, 10, "Gráfica de precios", 1, 1, 'C')

        # Tabla de descripción de la propiedad - RESPETANDO MÁRGENES
        table_y = current_y + 36

        # --- CONFIGURACIÓN GENERAL ---
        self.set_font('Arial', '', 10)
        line_height = 8
        col_width = available_width / 4
        gray_fill = (240, 240, 240)
        gray_line = (200, 200, 200)
        text_color = (60, 60, 60)  # Color de texto para los encabezados

        # --- TÍTULO DE SECCIÓN ---
        self.set_xy(margin, table_y)
        self.set_font('Arial', 'B', 14)
        self.cell(available_width / 2, 8, "Descripción de la propiedad", 0, 0, 'L')
        self.set_font('Arial', 'B', 10)
        self.cell(available_width / 2, 8, f"C.P. {fila.get('cp', '')}", 0, 1, 'R')

        # Datos de la tabla de descripción de la propiedad
        table_data = [
            ("Tipo de propiedad", property_data['tipo_propiedad'].capitalize(), "Tamaño de Construcción", f"{property_data['mConstruccion']} M²"),
            ("Recámaras", str(property_data['Recamaras']), "Tamaño de lote", f"{property_data['mTerreno']} M²"),
            ("Baños Completos", str(property_data['Banos_completos']), "Medio Baños", property_data['mediobano']),
            ("Estacionamientos", str(property_data['Estacionamiento']), "Baños", property_data['Banos'])
        ]

        # Dibujar la tabla de descripción RESPETANDO MÁRGENES
        y_pos = table_y + 10

        # Definir anchos: primera y tercera columna más anchas
        ancho_col1 = available_width * 0.28
        ancho_col2 = available_width * 0.22
        ancho_col3 = available_width * 0.28
        ancho_col4 = available_width * 0.22

        for row in table_data:
            self.set_xy(margin, y_pos)

            # Primera columna (header con fondo, más ancha)
            self.set_fill_color(*gray_fill)
            self.set_text_color(*text_color)
            self.set_font('Arial', 'B', 9)
            self.cell(ancho_col1, line_height, f"  {row[0]}", 0, 0, 'L', fill=True)

            # Segunda columna (valor)
            self.set_font('Arial', '', 9)
            self.set_text_color(0, 0, 0)
            self.cell(ancho_col2, line_height, f"{row[1]}", 0, 0, 'C')

            # Tercera columna (header con fondo, más ancha)
            self.set_fill_color(*gray_fill)
            self.set_text_color(*text_color)
            self.set_font('Arial', 'B', 9)
            self.cell(ancho_col3, line_height, f"  {row[2]}", 0, 0, 'L', fill=True)

            # Cuarta columna (valor)
            self.set_font('Arial', '', 9)
            self.set_text_color(0, 0, 0)
            self.cell(ancho_col4, line_height, f"{row[3]}", 0, 0, 'C')

            # Dibujar línea horizontal
            self.set_draw_color(*gray_line)
            self.line(margin, y_pos + line_height, margin + available_width, y_pos + line_height)

            y_pos += line_height

        # Tabla de historial de la propiedad - RESPETANDO MÁRGENES
        # Esta tabla es independiente y NO debe reutilizar variables de la tabla anterior
        y_pos_histo = y_pos + 12  # Separación suficiente debajo de la tabla anterior
        # --- TÍTULO DE SECCIÓN ---
        self.set_xy(margin, y_pos + 4)
        self.set_font('Arial', 'B', 14)
        self.cell(available_width / 2, 8, "Histórico", 0, 0, 'L')

        # Definir los encabezados y los valores para la tabla de historial
        encabezados_histo = [
            "Fecha",
            "Evento",
            "Tipo",
            "Precio",
            "Apreciación",
            "Oferta",
            "Fuente"
        ]
        valores_histo = [
            property_data.get('fecha', ''),
            property_data.get('evento', '').capitalize(),
            property_data.get('tipo_propiedad', '').capitalize(),
            f"{precio_text}",
            "- -",
            "- -",
            "Formulario"
        ]

        num_columnas_histo = len(encabezados_histo)
        ancho_col_histo = available_width / num_columnas_histo

        # Primera fila: encabezados con fondo gris
        self.set_xy(margin, y_pos_histo)
        self.set_font('Arial', 'B', 9)
        self.set_fill_color(*gray_fill)
        self.set_text_color(*text_color)
        for i in range(num_columnas_histo):
            self.cell(ancho_col_histo, line_height, encabezados_histo[i], 0, 0, 'C', fill=True)
        self.ln(line_height)

        # Segunda fila: valores
        y_pos_histo += line_height
        self.set_xy(margin, y_pos_histo)
        self.set_font('Arial', '', 9)
        self.set_text_color(0, 0, 0)
        for i in range(num_columnas_histo):
            self.cell(ancho_col_histo, line_height, valores_histo[i], 0, 0, 'C')
        self.ln(line_height)

        # Dibujar línea horizontal debajo de la tabla de historial
        self.set_draw_color(*gray_line)
        self.line(margin, y_pos_histo + line_height, margin + available_width, y_pos_histo + line_height)


        # Título de sección de Comparabilidad con el Mercado (centrado y en una sola línea)
        y_pos_compar = y_pos_histo + 12
        # Definir los textos del título compuesto
        textGraf1 = "Comparabilidad con el Mercado - "
        textGraf2 = f"{property_data['tipo_propiedad'].capitalize()}s"
        textGraf3 = f" en {property_data['municipio']}"
        textGraf4 = " entre "
        textGraf5 = "$0,000,000 y $0,000,000"
        # Concatenar todos los textos en una sola línea
        titulo_completo = f"{textGraf1}{textGraf2}{textGraf3}{textGraf4}{textGraf5}"
        # Seleccionar fuente y color para todo el título
        self.set_font('Arial', 'B', 13)
        self.set_text_color(0, 0, 0)
        # Calcular el ancho total del título para centrarlo
        ancho_titulo = self.get_string_width(titulo_completo)
        x_inicio = (self.w - ancho_titulo) / 2
        # Posicionar y escribir el título centrado en y_pos_compar
        self.set_xy(x_inicio, y_pos_compar)
        self.cell(ancho_titulo, 10, titulo_completo, 0, 1, 'C')









        print(f"Segunda página agregada correctamente")

    def add_third_page(self, property_data):
        """Agregar la tercera página con el mapa y análisis de activos comparables"""
        # Forzar una nueva página
        self.add_page()
        
        # CONFIGURAR MÁRGENES FIJOS PARA TERCERA PÁGINA
        margin = 20
        self.set_left_margin(margin)
        self.set_right_margin(margin)
        self.set_auto_page_break(auto=True, margin=20)
        
        # Calcular ancho disponible
        available_width = self.w - (2 * margin)
        
        # Agregar el mapa - RESPETANDO MÁRGENES
        map_y = 30
        map_height = 90  # Altura del mapa
        
        try:
            self.image('tools/mapa_ejemplo.png', x=margin, y=map_y, w=available_width, h=map_height)
        except Exception as e:
            print(f"Error cargando mapa: {e}")
            # Si falla el mapa, agregar texto alternativo
            self.set_xy(margin, map_y)
            self.set_font('Arial', '', 12)
            self.cell(available_width, map_height, "Mapa no disponible", 1, 1, 'C')
        
        # Posición Y después del mapa
        current_y = map_y + map_height + 10
        
        # Título "Activos comparables sugeridos (1-3)"
        self.set_xy(margin, current_y)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.cell(available_width, 10, "Activos comparables sugeridos (1-3)", 0, 1, 'L')
        
        # Espacio después del título
        current_y += 10
        
        # Sección "Similitud" con círculos de colores
        self.set_xy(margin, current_y)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, "Similitud", 0, 1, 'L')
        
        # Crear los círculos de similitud con colores
        legend_y = current_y + 15
        circle_radius = 3
        
        # Configurar posiciones para los círculos y texto
        items = [
            ("Alta", (76, 175, 80)),      # Verde
            ("Moderada", (255, 193, 7)),  # Amarillo/Naranja
            ("Baja", (244, 67, 54)),      # Rojo/Naranja
            ("Propiedad", (33, 150, 243)) # Azul
        ]
        
        x_start = margin
        for i, (label, color) in enumerate(items):
            # Posición X para cada elemento
            x_pos = x_start + (i * 45)
            
            # Dibujar círculo de color
            self.set_fill_color(color[0], color[1], color[2])
            self.circle(x_pos, legend_y, circle_radius, 'F')
            
            # Agregar texto junto al círculo
            self.set_xy(x_pos + 6, legend_y - 2)
            self.set_font('Arial', '', 10)
            self.set_text_color(0, 0, 0)
            self.cell(35, 5, label, 0, 0, 'L')
        
        # Tabla de propiedades comparables
        table_y = legend_y + 20
        
        # Headers de la tabla
        headers = ["Propiedad", "Precio de Venta", "Precio por M²", "Recámaras", "Baños", "Tamaño"]
        col_widths = [40, 30, 25, 20, 20, 25]  # Anchos proporcionales
        
        # Ajustar anchos de columna al ancho disponible
        total_width_ratio = sum(col_widths)
        col_widths = [w * available_width / total_width_ratio for w in col_widths]
        
        # Dibujar headers
        self.set_xy(margin, table_y)
        self.set_font('Arial', 'B', 9)
        self.set_fill_color(240, 240, 240)  # Gris claro para headers
        
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, 'C', True)
        
        table_y += 8
        
        # Datos de ejemplo para las propiedades comparables
        properties_data = [
            ("Circuito El Cerrito 142", "$3,500,000", "$23,333/M²", "3", "2.5", "150 M²"),
            ("Circuito El Cerrito 138", "$3,200,000", "$21,333/M²", "3", "2", "150 M²"),
            ("Circuito El Cerrito 144", "$3,800,000", "$25,333/M²", "4", "3", "150 M²")
        ]
        
        # Dibujar filas de datos
        self.set_font('Arial', '', 8)
        self.set_fill_color(255, 255, 255)  # Fondo blanco
        
        for row_data in properties_data:
            self.set_xy(margin, table_y)
            for i, cell_data in enumerate(row_data):
                self.cell(col_widths[i], 8, cell_data, 1, 0, 'C', True)
            table_y += 8
        
        print(f"Tercera página agregada correctamente con mapa y tabla de comparables")

    def circle(self, x, y, r, style=''):
        """Método auxiliar para dibujar círculos"""
        if style == 'F':
            self.ellipse(x-r, y-r, 2*r, 2*r, 'F')
        else:
            self.ellipse(x-r, y-r, 2*r, 2*r, 'D')

    def add_six_page(self, property_data):
        """Agregar la quinta página con el análisis detallado"""
        # Forzar una nueva página
        self.add_page()
        
        # CONFIGURAR MÁRGENES FIJOS PARA LA QUINTA PÁGINA
        margin = 20
        self.set_left_margin(margin)
        self.set_right_margin(margin)
        self.set_auto_page_break(auto=True, margin=20)
        
        # Título principal centrado
        self.set_y(30)
        self.set_font('Arial', 'B', 13)
        self.set_text_color(0, 0, 0)
        texto1 = "Mercado de Riesgo en oferta -"
        self.set_font('Arial', '', 10)
        self.set_text_color(80, 80, 80)
        texto2 = property_data['ubicacion_zona']
        
        # Calcular el ancho de ambos textos para centrarlos
        self.set_font('Arial', 'B', 13)
        ancho1 = self.get_string_width(texto1)
        self.set_font('Arial', '', 10)
        ancho2 = self.get_string_width(texto2)
        espacio = 5
        total_ancho = ancho1 + espacio + ancho2
        x_inicio = (self.w - total_ancho) / 2
        
        # Escribir el título
        self.set_xy(x_inicio, 30)
        self.set_font('Arial', 'B', 13)
        self.set_text_color(0, 0, 0)
        self.cell(ancho1, 10, texto1, 0, 0, 'L')
        self.set_font('Arial', '', 10)
        self.set_text_color(80, 80, 80)
        self.cell(espacio, 10, "", 0, 0)
        self.cell(ancho2, 10, texto2, 0, 1, 'L')
        
        # Línea horizontal debajo del título
        y_linea = self.get_y() + 2
        self.set_draw_color(180, 180, 180)
        self.set_line_width(0.5)
        self.line(margin, y_linea, self.w - margin, y_linea)
        
        # PRIMERA SECCIÓN: Dos columnas con valores centradas en cada columna
        self.set_y(y_linea + 6)
        ancho_pagina = self.w - 2 * margin
        ancho_columna = ancho_pagina / 2

        # Columna izquierda - Riesgo de depreciación (centrado en su columna)
        x_col_izq = margin
        self.set_xy(x_col_izq, y_linea + 6)
        self.set_font('Arial', 'B', 9)
        self.set_text_color(0, 0, 0)
        self.cell(ancho_columna, 5, "Riesgo de depreciación", 0, 2, 'C')
        self.set_x(x_col_izq)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(255, 0, 0)  # Rojo
        self.cell(ancho_columna, 8, "5.04%", 0, 2, 'C')
        y_primera_columna = self.get_y()

        # Columna derecha - Nivel de riesgo (centrado en su columna)
        x_col_der = margin + ancho_columna
        self.set_xy(x_col_der, y_linea + 6)
        self.set_font('Arial', 'B', 9)
        self.set_text_color(0, 0, 0)
        self.cell(ancho_columna, 5, "Nivel de riesgo", 0, 2, 'C')
        self.set_x(x_col_der)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(255, 0, 0)  # Rojo
        self.cell(ancho_columna, 8, "Medio Bajo", 0, 2, 'C')
        # PÁRRAFO EXPLICATIVO
        self.set_y(max(y_primera_columna, self.get_y()) + 5)
        self.set_font('Arial', '', 8)
        self.set_text_color(60, 60, 60)
        
        parrafo_explicativo = ("El riesgo de depreciación se refiere a la posibilidad de que el valor de una propiedad disminuya con el tiempo debido a las principales tendencias en el mercado inmobiliario en una región específica. La variación Riesgo de Depreciación se calcula con base en estudios estadísticos del historial de ventas inmobiliarias en la zona y aproximadamente el 5.04% de cada 10 casas ha estado en oferta durante más de 1 año. Este nivel de riesgo se considera Medio Bajo en comparación con el mercado inmobiliario general de Pachuca de Soto. Considerar estos factores pueden ayudar a entender el mercado en el que participa una propiedad.")
        
        self.multi_cell(self.w - 2 * margin, 4, parrafo_explicativo, 0, 'J')
        
        # SUBTÍTULO "Comercialización"
        self.ln(5)
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, "Comercialización", 0, 1, 'L')
        
        # Línea horizontal debajo del subtítulo
        y_subtitulo = self.get_y() + 2
        self.set_draw_color(180, 180, 180)
        self.set_line_width(0.5)
        self.line(margin, y_subtitulo, self.w - margin, y_subtitulo)
        
        # SEGUNDA SECCIÓN: Dos columnas con gráficos y texto
        y_inicio_graficos = y_subtitulo + 5
        
        # Definir ancho de columnas para gráficos
        col_width = (self.w - 2 * margin - 10) / 2  # 10 es el espacio entre columnas
        x_col_izq = margin
        x_col_der = margin + col_width + 10
        
        # **COLUMNA IZQUIERDA COMPLETA**
        self.set_xy(x_col_izq, y_inicio_graficos)
        self.set_font('Arial', 'B', 9)
        self.set_text_color(0, 0, 0)
        municipio_estado = fila.get('municipio', '') + ', ' + fila.get('estado', '')
        self.cell(col_width, 5, f"Meses de oferta - {municipio_estado}", 0, 1, 'L')
        # Espacio reservado para el gráfico (reducido de 65 a 40)
        y_grafico_izq = self.get_y() + 2
        # Aquí iría el código para insertar el gráfico de líneas
        # self.image('ruta_del_grafico_lineas.png', x_col_izq, y_grafico_izq, col_width, 40)
        
        # Texto debajo del gráfico izquierdo
        y_texto_izq = y_grafico_izq + 45  # Espacio del gráfico + margen
        self.set_xy(x_col_izq, y_texto_izq)
        self.set_font('Arial', '', 7)
        self.set_text_color(60, 60, 60)
        
        texto_grafico_izq = ("Los meses de oferta es una métrica que refleja cuántos meses pasarían antes de que todas las propiedades disponibles se agotaran si las mismas se compraran con los créditos demandados (es decir, si se usaran todos los créditos disponibles de dicho mes)\n\n"
                             "Este gráfico te permite visualizar cómo es la relación entre la oferta de propiedades y la demanda de créditos. Un promedio de meses alto indica que se tiene un mercado más competitivo, puesto que hay más propiedades 'peleando' contra los créditos otorgados para dicho mercado inmobiliario. Un promedio de meses bajo indica una reducción en el número de propiedades listadas o un aumento en la demanda de créditos y, por lo tanto, un mercado menos competitivo. En septiembre de 2023, la cifra arrojó una puntuación de 4.82 meses, esta cifra ha aumentado consistentemente al paso de los meses. En marzo de 2024 se registró la cifra más alta de 6.34, a partir de ese mes se registra una caída a 4.63 y para mayo el cociente disminuyó a 4.40, esto podría indicar una disminución en el número de propiedades listadas en los últimos meses y, por lo tanto, un mercado más competitivo en comparación a los meses finales de 2023.")

        self.multi_cell(col_width, 3.5, texto_grafico_izq, 0, 'J')
        
        # **COLUMNA DERECHA COMPLETA**
        # Empezar desde la misma altura que la columna izquierda
        self.set_xy(x_col_der, y_inicio_graficos)
        self.set_font('Arial', 'B', 9)
        self.set_text_color(0, 0, 0)
        self.cell(col_width, 5, "Propiedades ofertadas en el mercado", 0, 1, 'L')
        self.set_x(x_col_der)
        self.cell(col_width, 5, f"Colonia {fila.get('colonia', '')}", 0, 1, 'L')
        
        # Espacio reservado para el gráfico (mismo tamaño que el izquierdo)
        y_grafico_der = self.get_y() + 2
        # Aquí iría el código para insertar el gráfico de barras
        # self.image('ruta_del_grafico_barras.png', x_col_der, y_grafico_der, col_width, 40)
        
        # Texto debajo del gráfico derecho
        y_texto_der = y_grafico_der + 45  # Mismo espacio que la columna izquierda
        self.set_xy(x_col_der, y_texto_der)
        self.set_font('Arial', '', 7)
        self.set_text_color(60, 60, 60)
        
        texto_grafico_der = ("Las propiedades en el mercado muestran la tendencia en la cantidad de propiedades ofertadas para la colonia La Herradura desde septiembre de 2023 a mayo de 2024 en el municipio de Pachuca de Soto, Hidalgo, México.\n\n"
                             "Esto puede ayudar a los inversores, compradores y vendedores a entender cómo está cambiando el mercado inmobiliario en esta área específica. En septiembre de 2024, había 59 propiedades ofertadas disponibles. Esta cantidad ha cambiado con el paso de los meses, pues, en diciembre la cantidad ofertada disminuyó a 57, para los meses consecutivos volvió a disminuir, en febrero eran 55 las propiedades ofertadas y en marzo fueron 47. Sin embargo, para abril y mayo aumentaron estas propiedades con 54 y 57, respectivamente.")
        self.multi_cell(col_width, 3.5, texto_grafico_der, 0, 'J')
        
        # Establecer la posición Y final para que ambas columnas terminen a la misma altura
        final_y = max(y_texto_izq + len(texto_grafico_izq.split('\n')) * 3.5 * 4, 
                     y_texto_der + len(texto_grafico_der.split('\n')) * 3.5 * 4)
        self.set_y(final_y)
        
        print(f"Quinta página agregada correctamente")

    def add_seven_page(self, property_data):
        """Agregar la sexta página con el análisis detallado"""
        # Forzar una nueva página
        self.add_page()
        
        # CONFIGURAR MÁRGENES FIJOS PARA LA SEXTA PÁGINA
        margin = 20
        self.set_left_margin(margin)
        self.set_right_margin(margin)
        self.set_auto_page_break(auto=True, margin=20)
        
        # Título "Disclaimer" centrado
        self.set_y(30)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, "Disclaimer", 0, 1, 'C')
        
        # Línea horizontal debajo del título
        y_linea = self.get_y() + 2
        self.set_draw_color(180, 180, 180)
        self.set_line_width(0.5)
        self.line(margin, y_linea, self.w - margin, y_linea)
        
        # Texto justificado de disclaimer, cada párrafo separado y letra más pequeña
        # Tomar la fecha formateada desde property_data['fecha']
        # Convertir la fecha de property_data['fecha'] (formato DD/MM/AAAA) a "mes de AAAA"
        import calendar
        fecha_str = property_data.get('fecha', '')
        if fecha_str and len(fecha_str) == 10 and fecha_str[2] == '/' and fecha_str[5] == '/':
            try:
                mes = int(fecha_str[3:5])
                anio = fecha_str[6:]
                meses_es = [
                    "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
                    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
                ]
                mes_texto = meses_es[mes] if 1 <= mes <= 12 else ""
                fecha_actualizada = f"{mes_texto} de {anio}" if mes_texto else fecha_str
            except Exception:
                fecha_actualizada = fecha_str
        else:
            fecha_actualizada = "NO MENCIONADA"
        disclaimer_parrafos = [
            f"Para concluir este análisis de precios, es crucial destacar que los datos se encuentran actualizados hasta {fecha_actualizada}. No obstante, el mercado inmobiliario es altamente dinámico y evoluciona constantemente. Por lo tanto, es fundamental reconocer que este reporte representa una instantánea a corto plazo, lo que enfatiza la necesidad de mantenerlo actualizado. La adaptación a las nuevas tendencias y condiciones del mercado se vuelve esencial para mantener una ventaja competitiva y lograr una comprensión precisa de la industria. Estos conocimientos ofrecen no solo una perspectiva valiosa a corto plazo, sino que también funcionan como una guía esencial para los inversionistas, desarrolladores y profesionales del sector puesto que les capacita para tomar decisiones informadas y estratégicas en este entorno en constante evolución y siempre cambiante.",
            "Este explorador de propiedades se proporciona únicamente con fines de información comercial general. No se crea ninguna relación de asesoramiento  o  de  otro  tipo  mediante  la  aceptación  o  el  uso  de  su  explorador  de  propiedades.  La  inclusión  de  este  explorador  de propiedades  con  cualquier  otro  material  no  constituye  un  respaldo  por  parte  de  DatAlpine  y  de  ningún  tercero  ni  de  sus  productos  o servicios. El mercado proyectado, la valoración y la información financiera, las conclusiones y otra información contenida en este explorador de propiedades se basan en metodologías para garantizar su precisión. Sin embargo, dicha información y conclusiones no son previsiones, valoraciones ni opiniones de valoraciones definitivas. Dicha información y conclusiones se expresan en términos de probabilidad basada en factores de mercado e información enviada a DatAlpine, y dicha información y conclusiones no están garantizadas por DatAlpine y no deben interpretarse como una valoración certificada, ni como asesoramiento de inversión para la toma de decisiones críticas. DatAlpine utiliza o ha utilizado datos y suposiciones públicos y/o confidenciales proporcionados a  DatAlpine  por terceros, y  DatAlpine no ha verificado de forma independiente los datos y suposiciones utilizados en estos análisis o conjuntos de datos. Los atributos de las propiedades pueden ser inexactos porque los datos del tasador no siempre incluyen adiciones y/o modificaciones que afectan el precio final de la propiedad. Los cambios en los datos subyacentes o los supuestos operativos, o cualquier pérdida de acceso a una o más fuentes afectarán claramente los análisis, la información y las conclusiones establecidas en este informe del explorador de propiedades.",
            "En nombre de DatAlpine agradecemos la confianza depositada en nuestro análisis y estamos disponibles para cualquier consulta adicional o  colaboración  futura.  Estamos  comprometidos  a  seguir  brindando  soluciones  y  conocimientos  de  vanguardia  para  la  industria  de  la construcción inmobiliaria. ¡Gracias por su atención y su interés en nuestros servicios! "
        ]
        self.set_y(y_linea + 10)
        self.set_font('Arial', '', 7)  # Letra más pequeña
        self.set_text_color(60, 60, 60)
        # Reducir la sangría de cada párrafo
        sangria = 3  # Menor sangría (en puntos)
        max_width = self.w - 2 * margin - sangria
        for parrafo in disclaimer_parrafos:
            self.set_x(margin + sangria)
            self.multi_cell(max_width, 6, parrafo, 0, 'J')
            self.ln(2)
        print(f"Sexta página agregada correctamente")
    


# EXTRA

    def multi_cell_in_bounds(self, x, y, w, h, text):
        """Método auxiliar para dibujar texto en una celda con límites específicos"""
        # Guardar posición actual
        current_x = self.get_x()
        current_y = self.get_y()
        
        # Establecer posición y límites
        self.set_xy(x + 1, y + 1)  # Pequeño margen interno
        
        # Calcular el ancho máximo para el texto
        max_width = w - 2
        
        # Usar multi_cell con límites
        try:
            self.multi_cell(max_width, 4, text, border=0, align='C')
        except:
            # Si falla, usar cell simple
            self.set_xy(x, y)
            self.cell(w, h, text[:20], 1, 0, 'C')
        
        # Dibujar el borde de la celda
        self.rect(x, y, w, h)
        
        # Restaurar posición
        self.set_xy(current_x, current_y)

    def load_csv_data(csv_path="editable/agosto_2024_1.csv"):
        """Cargar y procesar datos del CSV"""
        try:
            csv_data = pd.read_csv(csv_path)
            # Convertir a lista de diccionarios para facilitar el acceso
            return csv_data.to_dict('records')
        except Exception as e:
            print(f"Error al cargar CSV: {e}")
            return []

    def add_comparison_page_1(self, property_data, csv_path="editable/agosto_2024_1.csv",load_csv_data=load_csv_data):
        """Agregar página de comparación con las primeras 3 propiedades del CSV"""
        # Cargar datos del CSV
        csv_data = load_csv_data(csv_path)
        
        if not csv_data:
            print("No se pudieron cargar datos del CSV")
            return
        
        # Forzar una nueva página
        self.add_page()
        
        # CONFIGURAR MÁRGENES FIJOS
        margin = 20
        self.set_left_margin(margin)
        self.set_right_margin(margin)
        self.set_auto_page_break(auto=True, margin=20)
        
        # Título principal
        self.set_y(30)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, "Activos comparables sugeridos (1-3)", 0, 1, 'L')
        
        # Calcular dimensiones de la tabla
        available_width = self.w - (2 * margin)
        col_width = available_width / 4  # 4 columnas: header + propiedad original + 2 del CSV
        
        # Altura de las imágenes
        image_height = 25
        
        # Posición inicial de la tabla
        table_y = 45
        current_y = table_y
        
        # FILA DE IMÁGENES
        self.set_xy(margin, current_y)
        
        # Primera columna (header vacío para imágenes)
        self.cell(col_width, image_height, "", 1, 0, 'C')
        
        # Imagen de la propiedad original
        try:
            nombre_carpeta_propiedad = property_data.get('nombre_carpeta', 'Irving_Alvarez_Bautista')
            self.image(f'propiedades/{nombre_carpeta_propiedad}/Propiedad.jpg', margin + col_width + 2, current_y + 2, 
            #self.image('tools/Propiedad.jpg', margin + col_width + 2, current_y + 2, 
                    col_width - 4, image_height - 4)
        except:
            pass
        self.set_xy(margin + col_width, current_y)
        self.cell(col_width, image_height, "", 1, 0, 'C')
        
        # Imágenes de las primeras 2 propiedades del CSV
        for i in range(min(2, len(csv_data))):
            try:
                image_path = f'tools/propiedades/prop_{i+1}.jpg'
                self.image(image_path, margin + col_width * (i+2) + 2, current_y + 2, 
                        col_width - 4, image_height - 4)
            except:
                pass
            self.set_xy(margin + col_width * (i+2), current_y)
            self.cell(col_width, image_height, "", 1, 0, 'C')
        
        current_y += image_height
        
        # FILA DE DIRECCIONES
        self.set_xy(margin, current_y)
        self.set_font('Arial', 'B', 8)
        self.cell(col_width, 15, "Direccion", 1, 0, 'C')
        
        # Dirección de la propiedad original
        direccion_original = self.truncate_text(property_data.get('ubicacion', 'N/A'), 30)
        self.set_font('Arial', '', 7)
        self.multi_cell_in_bounds(margin + col_width, current_y, col_width, 15, direccion_original)
        
        # Direcciones del CSV (primeras 2)
        for i in range(min(2, len(csv_data))):
            ubicacion = self.truncate_text(csv_data[i].get('ubicacion', 'N/A'), 25)
            self.multi_cell_in_bounds(margin + col_width * (i+2), current_y, col_width, 15, ubicacion)
        
        current_y += 15
        
        # FILAS DE DATOS DINÁMICAS
        data_rows = self.build_comparison_rows(property_data, csv_data, 0, 2)
        
        # Dibujar filas de datos
        self.draw_data_rows(data_rows, margin, current_y, col_width)
        
        print("Primera página de comparación agregada correctamente")

    def add_comparison_page_2(self, property_data, csv_path="editable/agosto_2024_1.csv",load_csv_data=load_csv_data):
        """Agregar página de comparación con las siguientes 2 propiedades del CSV"""
        # Cargar datos del CSV
        csv_data = load_csv_data(csv_path)
        
        if not csv_data or len(csv_data) <= 2:
            print("No hay suficientes datos para la segunda página")
            return
        
        # Forzar una nueva página
        self.add_page()
        
        # CONFIGURAR MÁRGENES FIJOS
        margin = 20
        self.set_left_margin(margin)
        self.set_right_margin(margin)
        self.set_auto_page_break(auto=True, margin=20)
        
        # Título principal
        self.set_y(30)
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, "Activos comparables sugeridos (3-4)", 0, 1, 'L')
        
        # Calcular dimensiones de la tabla
        available_width = self.w - (2 * margin)
        col_width = available_width / 4  # 4 columnas
        
        # Altura de las imágenes
        image_height = 25
        
        # Posición inicial de la tabla
        table_y = 45
        current_y = table_y
        
        # FILA DE IMÁGENES
        self.set_xy(margin, current_y)
        
        # Primera columna (header vacío)
        self.cell(col_width, image_height, "", 1, 0, 'C')
        
        # Imagen de la propiedad original
        try:
            self.image('tools/Propiedad.jpg', margin + col_width + 2, current_y + 2, 
                    col_width - 4, image_height - 4)
        except:
            pass
        self.set_xy(margin + col_width, current_y)
        self.cell(col_width, image_height, "", 1, 0, 'C')
        
        # Imágenes de las propiedades 3 y 4 del CSV
        for i in range(2, min(4, len(csv_data))):
            try:
                image_path = f'tools/propiedades/prop_{i+1}.jpg'
                self.image(image_path, margin + col_width * (i) + 2, current_y + 2, 
                        col_width - 4, image_height - 4)
            except:
                pass
            self.set_xy(margin + col_width * (i), current_y)
            self.cell(col_width, image_height, "", 1, 0, 'C')
        
        current_y += image_height
        
        # FILA DE DIRECCIONES
        self.set_xy(margin, current_y)
        self.set_font('Arial', 'B', 8)
        self.cell(col_width, 15, "Direccion", 1, 0, 'C')
        
        # Dirección de la propiedad original
        direccion_original = self.truncate_text(property_data.get('ubicacion', 'N/A'), 30)
        self.set_font('Arial', '', 7)
        self.multi_cell_in_bounds(margin + col_width, current_y, col_width, 15, direccion_original)
        
        # Direcciones del CSV (propiedades 3 y 4)
        for i in range(2, min(4, len(csv_data))):
            ubicacion = self.truncate_text(csv_data[i].get('ubicacion', 'N/A'), 25)
            self.multi_cell_in_bounds(margin + col_width * (i), current_y, col_width, 15, ubicacion)
        
        current_y += 15
        
        # FILAS DE DATOS DINÁMICAS
        data_rows = self.build_comparison_rows(property_data, csv_data, 2, 2)
        
        # Dibujar filas de datos
        self.draw_data_rows(data_rows, margin, current_y, col_width)
        
        print("Segunda página de comparación agregada correctamente")

    def build_comparison_rows(self, property_data, csv_data, start_idx, count):
            """Construir filas de comparación dinámicamente desde los datos del CSV"""
            
            # Calcular similitudes y distancias dinámicamente (ejemplo)
            similarities = ["--"] + [f"0.{90-i*2}" for i in range(start_idx, min(start_idx + count, len(csv_data)))]
            distances = ["--"] + [f"{300 + i*100} m" for i in range(start_idx, min(start_idx + count, len(csv_data)))]
            
            data_rows = [
                ("Similitud", similarities),
                ("Distancia", distances),
                ("Fecha / Años", self.get_row_data(property_data, csv_data, start_idx, count, 'año_construccion', '2024')),
                ("Precio de venta", self.get_price_row(property_data, csv_data, start_idx, count, 'precio_mxn')),
                ("Precio M² Terreno", self.get_price_m2_row(property_data, csv_data, start_idx, count, 'precio_m2_terreno')),
                ("Precio M² Construcción", self.get_price_m2_row(property_data, csv_data, start_idx, count, 'precio_m2_construido')),
                ("Recámaras", self.get_row_data(property_data, csv_data, start_idx, count, 'Recamaras')),
                ("Baños", self.get_row_data(property_data, csv_data, start_idx, count, 'bano_total', 'Banos_completos')),
                ("Tamaño de Lote", self.get_size_row(property_data, csv_data, start_idx, count, 'metros_total', 'mTerreno')),
                ("M² Construidos", self.get_size_row(property_data, csv_data, start_idx, count, 'metros_construido', 'mConstruccion')),
                ("Tipo de propiedad", self.get_row_data(property_data, csv_data, start_idx, count, 'tipo', 'tipo_propiedad')),
                ("Año de construcción", self.get_row_data(property_data, csv_data, start_idx, count, 'año_construccion', '2024')),
                ("Estado de la publicación", self.get_row_data(property_data, csv_data, start_idx, count, 'Status', 'condicion')),
                ("Fraccionamiento", self.get_row_data(property_data, csv_data, start_idx, count, 'Colonia', 'fraccionamiento')),
                ("Colonia", self.get_row_data(property_data, csv_data, start_idx, count, 'colonia')),
                ("Días en el mercado", self.get_row_data(property_data, csv_data, start_idx, count, 'dias_transcurridos', '--')),
                ("Piscina", self.get_row_data(property_data, csv_data, start_idx, count, 'piscina', 'No')),
                ("Estacionamientos", self.get_row_data(property_data, csv_data, start_idx, count, 'Estacionamiento')),
                ("Sótano", self.get_row_data(property_data, csv_data, start_idx, count, 'sotano', 'No')),
                ("Precio promedio por fraccionamiento", ["--"] * (count + 1))
            ]
            
            return data_rows

    def get_row_data(self, property_data, csv_data, start_idx, count, csv_key, property_key=None):
            """Obtener datos de una fila específica"""
            if property_key is None:
                property_key = csv_key
            
            # Valor de la propiedad original
            original_value = str(property_data.get(property_key, 'N/A'))
            
            # Valores del CSV
            csv_values = []
            for i in range(start_idx, min(start_idx + count, len(csv_data))):
                value = csv_data[i].get(csv_key, 'N/A')
                csv_values.append(str(value))
            
            return [original_value] + csv_values

    def get_price_row(self, property_data, csv_data, start_idx, count, csv_key):
            """Obtener fila de precios formateada"""
            original_price = f"${property_data.get('Precio', 0):,}"
            
            csv_values = []
            for i in range(start_idx, min(start_idx + count, len(csv_data))):
                price = csv_data[i].get(csv_key, 0)
                try:
                    price_formatted = f"${float(price):,.0f}" if price != 'N/A' else "N/A"
                except:
                    price_formatted = "N/A"
                csv_values.append(price_formatted)
            
            return [original_price] + csv_values

    def get_price_m2_row(self, property_data, csv_data, start_idx, count, csv_key):
            """Obtener fila de precios por m² formateada"""
            # Calcular precio m² original (ejemplo)
            original_value = property_data.get('Precio', 0)
            divisor = 128 if 'terreno' in csv_key else 150
            # Convertir a entero antes de usar operaciones de división entera
            original_value_int = int(original_value)
            original_m2 = f"${original_value_int//divisor:,}.{original_value_int%divisor:02d}"
            
            csv_values = []
            for i in range(start_idx, min(start_idx + count, len(csv_data))):
                price_m2 = csv_data[i].get(csv_key, 0)
                try:
                    price_formatted = f"${float(price_m2):,.2f}" if price_m2 != 'N/A' else "N/A"
                except:
                    price_formatted = "N/A"
                csv_values.append(price_formatted)
            
            return [original_m2] + csv_values

    def get_size_row(self, property_data, csv_data, start_idx, count, csv_key, property_key):
            """Obtener fila de tamaños formateada"""
            original_size = property_data.get(property_key, 'N/A')
            
            csv_values = []
            for i in range(start_idx, min(start_idx + count, len(csv_data))):
                size = csv_data[i].get(csv_key, 'N/A')
                size_formatted = f"{size} m²" if size != 'N/A' else "N/A"
                csv_values.append(size_formatted)
            
            return [original_size] + csv_values

    def draw_data_rows(self, data_rows, margin, start_y, col_width):
            """Dibujar las filas de datos en la tabla"""
            current_y = start_y
            row_height = 8
            
            for row_data in data_rows:
                self.set_xy(margin, current_y)
                
                # Primera columna (header)
                self.set_font('Arial', 'B', 7)
                self.cell(col_width, row_height, row_data[0], 1, 0, 'L')
                
                # Columnas de datos
                self.set_font('Arial', '', 7)
                for i, value in enumerate(row_data[1]):
                    if i < 3:  # Máximo 3 columnas de datos
                        display_value = self.truncate_text(str(value), 15)
                        self.cell(col_width, row_height, display_value, 1, 0, 'C')
                
                current_y += row_height

    def truncate_text(self, text, max_length):
            """Truncar texto si es muy largo"""
            if len(text) > max_length:
                return text[:max_length-3] + "..."
            return text








# Definir el nombre del usuario (esto puede venir de una selección del usuario)
nombre_usuario = "Irving_Alvarez_Bautista"
# Construir la ruta a la carpeta del usuario
carpeta_usuario = f"propiedades/{nombre_usuario}"
# Buscar el único archivo .json en la carpeta seleccionada
archivos_json = [f for f in os.listdir(carpeta_usuario) if f.endswith('.json')]
if len(archivos_json) == 1:
    nombre_archivo = archivos_json[0]
    ruta_json = os.path.join(carpeta_usuario, nombre_archivo)
    # Leer el archivo JSON como un diccionario
    with open(ruta_json, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Convertir el diccionario a un DataFrame de una sola fila
    df_form = pd.DataFrame([data])
    df_form['nombre_archivo'] = nombre_archivo
    # Extraer la fecha del nombre del archivo
    partes = nombre_archivo.replace('.json', '').split('_')
    if len(partes) >= 3:
        fecha_str = partes[-2]  # Tomar el segundo elemento de derecha a izquierda
        if len(fecha_str) == 8 and fecha_str.isdigit():
            try:
                # Convertir a formato deseado DD/MM/AAAA
                fecha_formateada = f"{fecha_str[6:8]}/{fecha_str[4:6]}/{fecha_str[0:4]}"
                df_form['fecha'] = fecha_formateada
            except Exception as e:
                print(f"Error al convertir la fecha: {e}")
                df_form['fecha'] = ""
        else:
            df_form['fecha'] = ""
    else:
        df_form['fecha'] = ""
else:
    print("No se encontró un único archivo JSON en la carpeta seleccionada.")
df_form['ubicacion'] = df_form['calle'] + ', ' + df_form['colonia'] + ', ' + df_form['cp'] + ', ' + df_form['municipio']+ ', ' + df_form['estado']
df_form['ubicacion_zona'] = df_form['colonia'] + ', Municipio de ' + df_form['municipio']+ ', ' + df_form['estado']
df_form['Banos_completos'] = (df_form['Banos'].astype(float) + df_form['mediobano'].astype(float)).astype(int)
df_form['precio_datalpine'] =3368091.60
df_form['municipio_estado'] = df_form['municipio']+ ', ' + df_form['estado']


# Datos de la propiedad
# property_data = {
#     'ubicacion': 'Circuito El Cerrito 140, Privadas de La Herradura, CP 42082, Pachuca de Soto, Hidalgo, México',
#     'ubicacion_zona':'La Herradura , Municipio de Pachuca de Soto , Hidalgo', 
#     'Precio': 19444444,
#     'precio_datalpine': 3368091.60,
#     'fecha': '26/06/2024',
#     'tipo_propiedad': 'Casa',
#     'Recamaras': '3',
#     'Banos_completos': '2',
#     'Banos':'1',
#     'mediobano':'2',
#     'Estacionamiento': '2',
#     'mConstruccion': '150 M²',
#     'mTerreno': '128 M²',
#     'condicion': 'Excelente'
# }
# Obtener la primera fila como diccionario
#property_data = df_form
fila = df_form.iloc[0]
property_data = {
    'ubicacion': fila['ubicacion'],
    'ubicacion_zona': fila['ubicacion_zona'],
    'municipio': fila['municipio'],
    'nombre_carpeta': nombre_usuario,
    'Precio': float(fila.get('Precio', 0)) if fila.get('Precio', '') != '' else 0,
    'precio_datalpine': 3368091.60,
    'fecha': fila.get('fecha', ''),
    'tipo_propiedad': fila.get('tipo_propiedad', ''),
    'Recamaras': str(fila.get('Recamaras', '')),
    'Banos_completos': str(fila.get('Banos_completos', '')),
    'Banos': str(fila.get('Banos', '')),
    'mediobano': str(fila.get('mediobano', '')),
    'Estacionamiento': str(fila.get('Estacionamiento', '')),
    'mConstruccion': str(fila.get('mConstruccion', '')),
    'mTerreno': str(fila.get('mTerreno', '')),
    'condicion': fila.get('Condicion', ''),
    'evento': fila.get('EstadoCasa','')
}


# Instancia de PDF
pdf = PDF(format='Letter')
pdf.alias_nb_pages()
# Primera página
pdf.add_page()
#pdf.add_property_details('tools/Propiedad.jpg', property_data)
pdf.add_property_details(os.path.join(carpeta_usuario, 'Propiedad.jpg'), property_data)

# Segunda página
pdf.add_second_page(property_data)
# Tercera página (usando el método correcto)
pdf.add_third_page(property_data)
# Agregar las páginas de comparación (4-5)
pdf.add_comparison_page_1(property_data)
pdf.add_comparison_page_2(property_data)
# Agregar la seta página
pdf.add_six_page(property_data)
pdf.add_seven_page(property_data)

pdf.output('editable/Explorador_output.pdf')