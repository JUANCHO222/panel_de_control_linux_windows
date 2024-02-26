import socket
import threading
import subprocess
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from tkinter import *
from tkinter import messagebox
import os


# TODO: ___________________________________________________Metodos___________________________________________________________________

# ! Escanear puertos logicos abiertos
def escanear_puertos(ip_destino, puerto_inicial, puerto_final, tiempo_espera=2):
    # Crear el documento PDF
    pdf = canvas.Canvas('resultados.pdf')
    pdf.setTitle('Resultados del escaneo de puertos')

    # Agregar información adicional al PDF
    pdf.drawString(50, 800, f'Escaneo de puertos para el host: {ip_destino}')
    pdf.drawString(50, 780, f'Rango de puertos escaneados: {puerto_inicial} - {puerto_final}')
    pdf.drawString(50, 760, f'Tiempo de espera: {tiempo_espera} segundo(s)')

    # Lista para almacenar los puertos abiertos
    puertos_abiertos = []

    def escanear(puerto):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(tiempo_espera)  # Establecer tiempo de espera
        resultado = sock.connect_ex((ip_destino, puerto))
        if resultado == 0:
            print(f'Puerto {puerto} abierto')
            puertos_abiertos.append(puerto)  # Agregar puerto a la lista de puertos abiertos
            pdf.drawString(100, 700 - (puerto * 20), f'Puerto {puerto} abierto')
        sock.close()

    # Crear hilos para el escaneo de puertos
    hilos = []
    for puerto in range(puerto_inicial, puerto_final + 1):
        hilo = threading.Thread(target=escanear, args=(puerto,))
        hilo.start()
        hilos.append(hilo)

    # Esperar a que todos los hilos hayan terminado
    for hilo in hilos:
        hilo.join()

    # Agregar los puertos abiertos al PDF
    pdf.drawString(50, 740, "Puertos abiertos:")
    y = 720
    for puerto in puertos_abiertos:
        pdf.drawString(100, y, f"Puerto {puerto}")
        y -= 20

    # Guardar el PDF
    pdf.save()

    # Ventana que avisa cuando termina eso
    messagebox.showinfo("Escaneo de puertos finalizado", "El escaneo de puertos ha finalizado. Los resultados se han guardado en resultados.pdf")

# ! Funciones para permitir/denegar ping en Windows
def permitir_ping_windows():
    """ if ip:
        comando = f"netsh advfirewall firewall add rule name='Allow ICMPv4-In' protocol=icmpv4:any,any remoteip={ip} action=allow"
        subprocess.run(comando, shell=True)
        messagebox.showinfo("Ping aceptado", f"Se permitió el ping para la dirección IP: {ip}")
    else:
        messagebox.showerror("Error", "Debe ingresar una dirección IP") """
    subprocess.run(["netsh","advfirewall","firewall","delete","rule","name=BlockICMP"])


def denegar_ping_windows():
    """ if ip:
        comando = f"netsh advfirewall firewall add rule name='Block ICMPv4-In' protocol=icmpv4:any,any remoteip={ip} action=block"
        subprocess.run(comando, shell=True)
        messagebox.showinfo("Ping denegado", f"Se denegó el ping para la dirección IP: {ip}")
    else:
        messagebox.showerror("Error", "Debe ingresar una dirección IP") """
    subprocess.run(["netsh","advfirewall","firewall","add","rule","name=BlockICMP","dir=in","action=block","enable=yes","protocol=ICMPv4","any"])

# ! Permitir acceso al puerto 22
def permitir_acceso_puerto_22():
    comando = 'netsh advfirewall firewall add rule name="Allow Port 22" dir=in action=allow protocol=TCP localport=22'
    subprocess.run(comando, shell=True)
    messagebox.showinfo("Puerto desbloquedo", "El puerto 22 ha sido desbloqueado")

def denegar_acceso_puerto_22():
    comando = 'netsh advfirewall firewall delete rule name="Allow Port 22"'
    subprocess.run(comando, shell=True)
    messagebox.showinfo("Puerto bloqueado", "El puerto 22 ha sido bloqueado")

def salir():
    resultado = messagebox.askquestion("Salir", "¿Estas seguro de salir?")
    if resultado == "yes":
        ventana.destroy()

# TODO: ___________________________________________________Interfaz_______________________________________________________________

ventana = Tk()
ventana.title("Hacker")
ventana.resizable(True, True)

# * ----------------------Etiquetas----------------------

instruccion1 = Label(ventana, text="Analizar los puertos")
instruccion1.grid(row=1, column=0, sticky="w", padx=5, pady=5)

instruccion2 = Label(ventana, text="Permitir y denegar PING")
instruccion2.grid(row=2, column=0, sticky="w", padx=5, pady=5)

instruccion4 = Label(ventana, text="Permitir acceso al puerto 22")
instruccion4.grid(row=6, column=0, sticky="w", padx=5, pady=5)

# * ------------------------Texto------------------------
txtIp = Entry(ventana)
txtIp.grid(row=3, column=0, sticky="w", padx=5, pady=5)

# * -----------------------Botones-----------------------

btn1 = Button(ventana, text="Escanear puertos", command=lambda: escanear_puertos('192.168.46.222', 1, 4000))
btn1.grid(row=1, column=1, sticky="w", padx=5, pady=5)

btn2 = Button(ventana, text="Permitir ping", command=lambda: permitir_ping_windows())
btn2.grid(row=3, column=1,  sticky="w", padx=5, pady=5)
btn3 = Button(ventana, text="Denegar ping", command=lambda: denegar_ping_windows())
btn3.grid(row=3, column=2,  sticky="w",padx=5, pady=5)

btn6 = Button(ventana, text="Permitir acceso", command=lambda: permitir_acceso_puerto_22() )
btn6.grid(row=6, column=1,  sticky="w", padx=5, pady=5)

btn7 = Button(ventana, text="Denegar acceso", command=lambda: denegar_acceso_puerto_22() )
btn7.grid(row=6, column=2,  sticky="w",padx=5, pady=5)

btn_salir = Button(ventana, text="Salir", command=salir)
btn_salir.grid(row=6, column=3,  sticky="s",padx=5, pady=5)

ventana.mainloop()
