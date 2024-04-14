import tkinter as tk
from tkinter import ttk
import random
import string
import psutil

class Proceso:
    def __init__(self, pid, nombre, estado):
        self.pid = pid
        self.nombre = nombre
        self.estado = estado
        
class InterfazApp:
    def __init__(self, master):
        self.master = master
        self.master.title("FCFS")
        self.master.geometry("600x400")
        
        self.procesos_agregados = 0
        self.indice_elemento = 0
        self.prioridad_proceso = 0
        self.colaProcesos = []
        self.valoresTabla = []
        
        # Estilo de la tabla
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', background='#f0f0f0', foreground='black', rowheight=25, fieldbackground='#f0f0f0')
        style.configure('Treeview.Heading', font=('Arial', 11, 'bold'))
        style.map('Treeview', background=[('selected', '#347083')])
        
        # Crear tabla
        self.tree = ttk.Treeview(master, columns=('PID', 'Nombre', 'Estado'), show='headings')
        self.tree.heading('PID', text='PID')
        self.tree.heading('Nombre', text='Nombre')
        self.tree.heading('Estado', text='Estado')
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Botones
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)
        
        self.bloquear_button = tk.Button(button_frame, text='Bloquear', command=self.bloquear_proceso, bg='#4e74b8', fg='white', relief='raised', font=('Arial', 10, 'bold'))
        self.bloquear_button.pack(side='left', padx=5)
        
        self.continuar_button = tk.Button(button_frame, text='Continuar', command=self.continuar_proceso, bg='#2e856e', fg='white', relief='raised', font=('Arial', 10, 'bold'))
        self.continuar_button.pack(side='left', padx=5)
        
        self.terminar_button = tk.Button(button_frame, text='Terminar', command=self.terminar_proceso, bg='#ff0000', fg='white', relief='raised', font=('Arial', 10, 'bold'))
        self.terminar_button.pack(side='left', padx=5)

        self.cambiar_estados()
        self.agregar_proceso()
        
        
    def agregar_proceso(self):
        procesos_reales = obtener_procesos()
        if len(procesos_reales) > self.procesos_agregados:
            pid, nombre = procesos_reales[self.procesos_agregados]
            proceso = Proceso(pid, nombre, 'Nuevo')
            self.tree.insert('', 'end', values=(proceso.pid, proceso.nombre, proceso.estado))
            self.procesos_agregados += 1
            self.master.after(random.randint(5000, 8000), self.agregar_proceso)
            
    def bloquear_proceso(self):
        self.seleccion('Bloqueado', '')
                
    def continuar_proceso(self):
        self.seleccion('Listo', '')
        
    def terminar_proceso(self):
        self.seleccion('Terminado', 'eliminar') 
        
    def cambiar_estados(self):
        children = self.tree.get_children()
        if self.indice_elemento < len(children):
            item_id = random.choice(children)
            while item_id in ['Bloqueado', 'Ejecucion']:
                item_id = random.choice(children)
            estado_actual = self.tree.item(item_id, 'values')[2]
            if estado_actual != 'Listo':
                self.tree.item(item_id, values=(self.tree.item(item_id, 'values')[0], self.tree.item(item_id, 'values')[1], 'Listo'))
                verificar_proceso = self.tree.item(item_id, 'values')[0]
                if verificar_proceso not in self.colaProcesos:
                    self.colaProcesos.append(verificar_proceso)
            self.proceso_ejecucion()
            self.indice_elemento += 1
        self.master.after(random.randint(8500, 9000), self.cambiar_estados)
    
    def proceso_ejecucion(self):
        children = self.tree.get_children()
        nuevos_valores = set()
        for item_id in children:
            valor_item = self.tree.item(item_id, 'values')[0]
            if valor_item not in self.valoresTabla:
                nuevos_valores.add(valor_item)
        self.valoresTabla.extend(nuevos_valores)
        
        print(f'esto es el contenedor de las prioridades {self.colaProcesos}')
        print(f'este es el contenedor de arboles de la tabla {self.valoresTabla}')
        
        for item_id in children:
            valor_item = self.tree.item(item_id, 'values')[0]
            estatus = self.tree.item(item_id, 'values')[2]
            if valor_item == self.colaProcesos[self.prioridad_proceso] and estatus == 'Listo':
                print(valor_item)
                if valor_item not in self.colaProcesos:
                    self.colaProcesos.append(valor_item)
                self.tree.item(item_id, values=(valor_item, self.tree.item(item_id, 'values')[1], 'Ejecución'))
                self.master.after(random.randint(10000, 15000), lambda item=item_id: self.eliminar_item_si_existe(item_id))
                break
         
    def eliminar_item_si_existe(self, item_id):
        if self.tree.exists(item_id):
            valor_item = self.tree.item(item_id, 'values')[0]
            if valor_item in self.colaProcesos:
                self.colaProcesos.remove(valor_item)
            self.tree.delete(item_id)
  
    def seleccion(self, estado, eliminar):
        seleccion = self.tree.selection()
        if seleccion:
            indices_eliminar = []
            for item in seleccion:
                estado_actual = self.tree.item(item, 'values')[2]
                if estado_actual == 'Bloqueado':
                    self.tree.item(item, values=(self.tree.item(item, 'values')[0], self.tree.item(item, 'values')[1], 'Listo'))
                    valor_item = self.tree.item(item, 'values')[0]
                    self.colaProcesos.append(valor_item)
                if estado_actual != 'Bloqueado':
                    if estado == 'Bloqueado':
                        self.tree.item(item, values=(self.tree.item(item, 'values')[0], self.tree.item(item, 'values')[1], f'{estado}'))
                        valor_item = self.tree.item(item, 'values')[0]
                        if valor_item in self.colaProcesos:
                            self.colaProcesos.remove(valor_item)
                    else:
                        self.tree.item(item, values=(self.tree.item(item, 'values')[0], self.tree.item(item, 'values')[1], f'{estado}'))
                        valor_item = self.tree.item(item, 'values')[0]
                        self.colaProcesos.append(valor_item)
                    if eliminar == 'eliminar':
                        indices_eliminar.append(self.tree.index(item))
                        valor_item = self.tree.item(item, 'values')[0]
                        print(f'eliminaste el item: {valor_item}')
            for index in indices_eliminar:
                item = self.tree.get_children()[index]
                valor_item = self.tree.item(item, 'values')[0]
                self.colaProcesos.remove(valor_item)
                self.tree.delete(item)
                self.procesos_agregados -= 1

def obtener_procesos():
    procesos = []
    for i, proceso in enumerate(psutil.process_iter(['pid', 'name'])):
        procesos.append((proceso.info['pid'], proceso.info['name']))
        if i >= 19:
            break
    return procesos
            
def main():
    root = tk.Tk()
    app = InterfazApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()