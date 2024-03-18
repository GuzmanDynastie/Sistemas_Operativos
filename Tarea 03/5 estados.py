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
        self.master.title("Administrador de Tareas 💻")
        self.master.geometry("600x400")
        
        self.procesos_agregados = 0
        
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
        
        self.agregar_button = tk.Button(button_frame, text='Agregar Proceso', command=self.agregar_proceso, bg='#9f56a5', fg='white', relief='raised', font=('Arial', 10, 'bold'))
        self.agregar_button.pack(side='left', padx=5)
        
        self.agregar_button = tk.Button(button_frame, text='Bloquear', command=self.bloquear_proceso, bg='#4e74b8', fg='white', relief='raised', font=('Arial', 10, 'bold'))
        self.agregar_button.pack(side='left', padx=5)
        
        self.agregar_button = tk.Button(button_frame, text='Activar', command=self.activar_proceso, bg='#2e856e', fg='white', relief='raised', font=('Arial', 10, 'bold'))
        self.agregar_button.pack(side='left', padx=5)
        
        self.agregar_button = tk.Button(button_frame, text='Finalizar', command=self.finalizar_proceso, bg='#ff0000', fg='white', relief='raised', font=('Arial', 10, 'bold'))
        self.agregar_button.pack(side='left', padx=5)
        
        self.agregar_button = tk.Button(button_frame, text='Actualizar Procesos', command=self.actualizar_procesos, bg='#4B4B4B', fg='white', relief='raised', font=('Arial', 10, 'bold'))
        self.agregar_button.pack(side='left', padx=5)
        
        self.cambiar_estados()
        self.agregar_proceso()
        
    def agregar_proceso(self):
        procesos_reales = obtener_procesos()
        
        if len(procesos_reales) > self.procesos_agregados:
            pid, nombre = procesos_reales[self.procesos_agregados]
            proceso = Proceso(pid, nombre, 'Nuevo')
            self.tree.insert('', 'end', values=(proceso.pid, proceso.nombre, proceso.estado))
            self.procesos_agregados += 1
            self.master.after(random.randint(5000, 10000), self.agregar_proceso)
            
    def bloquear_proceso(self):
        self.seleccion('Bloqueado', '')
                
    def activar_proceso(self):
        self.seleccion('Activo', '')
        
    def finalizar_proceso(self):
        self.seleccion('Terminado', 'eliminar')
        
        
    def cambiar_estados(self):
        for item_id in self.tree.get_children():
            estado_actual = self.tree.item(item_id, 'values')[2]
            nuevo_estado = random.choice(['Nuevo', 'Preparado', 'Activo', 'Bloqueado', 'Terminado'])
            while nuevo_estado == estado_actual:
                nuevo_estado = random.choice(['Nuevo', 'Preparado', 'Activo', 'Bloqueado', 'Terminado'])
            self.tree.item(item_id, values=(self.tree.item(item_id, 'values')[0], self.tree.item(item_id, 'values')[1], nuevo_estado))
        self.master.after(random.randint(15000, 20000), self.cambiar_estados)
        
    def actualizar_procesos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        procesos_reales = obtener_procesos()
        
        for pid, nombre in procesos_reales:
            self.tree.insert('', 'end', values=(pid, nombre, 'Nuevo'))
            self.procesos_agregados = 20
        
    def seleccion(self, estado, eliminar):
        seleccion = self.tree.selection()
        if seleccion:
            for item in seleccion:
                self.tree.item(item, values=(self.tree.item(item, 'values')[0], self.tree.item(item, 'values')[1], f'{estado}'))
                if f'{eliminar}' == 'eliminar':
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