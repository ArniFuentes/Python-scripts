import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory


def main():
    try:
        root = Tk()
        root.withdraw()
        excel_file_path = askdirectory(title='Seleccionar una carpeta con los datos')

        if not excel_file_path:
            print("No se seleccionó una carpeta.")
            return

        file_list = os.listdir(excel_file_path)

        for file in file_list:
            process_excel_file(excel_file_path, file)

    except Exception as e:
        print(f"Error: {e}")


def process_excel_file(folder, file):
    print(f"Procesando archivo: {file}")
    date = file[-13:-5]
    year = date[:4]
    month = date[-4:-2]
    day = date[-2:]

    if file.endswith(".xlsx"):
        df = pd.read_excel(os.path.join(folder, file))
        df = df.drop_duplicates()
        print('duplicados borrados.')
        df['Fecha y hora actualizacion Paris'] = df['Fecha y hora actualizacion Paris'].dt.date
        target_date = pd.to_datetime(f'{year}-{month}-{day}').date()
        df = df[df['Fecha y hora actualizacion Paris'] == target_date]
        df = df.rename(columns={
            'Precio normal': 'Precio Normal Paris',
            'Precio oferta todo medio de pago': 'Precio oferta todo medio de pago Paris',
            'Precio Tarjeta': 'Precio tarjeta Paris',
            'SKU': 'Sku Paris',
            'URL': 'URL Paris',
            'Posee stock': 'Stock Paris'
        })

        df_columns = list(df.columns)
        df_list = []
        stores = [string[4:] for string in df_columns if 'Sku' in string]

        for store in stores:
            df_store = pd.DataFrame()
            df_store['SKU Paris'] = df['Sku Paris']
            df_store['SKU'] = df[f'Sku {store}']
            df_store['Categoría'] = df['Categoria (nivel 1)']
            df_store['Marca'] = df['Marca']
            df_store['Nombre'] = df['Nombre']
            df_store['Precio Normal'] = df[f'Precio Normal {store}']
            df_store['Precio oferta todo medio de pago'] = df[f'Precio oferta todo medio de pago {store}']
            df_store['Precio tarjeta'] = df[f'Precio tarjeta {store}']
            df_store['Stock'] = df[f'Stock {store}']
            df_store['Tienda'] = store
            df_store['Fecha'] = df['Fecha y hora actualizacion Paris']

            df_list.append(df_store)

        df = pd.concat(df_list, ignore_index=True)
        df = df[df['SKU'] != 0]
        df = df[df['Stock'] == 'con_stock']

        # Lista de reemplazo de categorías
        replacement_category = {
            'niÃ±os': 'niños',
            'ninos': 'niños',
            'linea blanca': 'línea blanca',
            'zapatos': 'zapatos y zapatillas',
            'tecno': 'tecnología'
        }

        df['Categoría'] = df['Categoría'].replace(replacement_category)
        df = df.drop_duplicates()
        output_file_name = f'{os.path.splitext(file)[0]}-transformado.xlsx'
        df.to_excel(os.path.join(folder, output_file_name), index=False)
        print(f'Archivo transformado y guardado como {output_file_name}')
    
    else:
        print('El no tienen extensión .xlsx')


if __name__ == "__main__":
    main()
