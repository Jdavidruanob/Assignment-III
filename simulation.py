import sys
import random
import matplotlib.pyplot as plt

# --- Constantes de la Simulacion ---
MAX_CYLINDERS = 5000 # 0 a 4999
NUM_REQUESTS = 1000  #

def run_fcfs(start_pos, requests):
    """
    Simula el algoritmo FCFS (First-Come, First-Served).
    Atiende las solicitudes en el orden en que llegaron.
    """
    total_movement = 0
    current_pos = start_pos
    path = [current_pos] # Lista para guardar la ruta para el gráfico

    for req in requests:
        movement = abs(req - current_pos)
        total_movement += movement
        current_pos = req
        path.append(current_pos)
        
    return total_movement, path

def run_scan(start_pos, requests, direction="up"):
    """
    Simula el algoritmo SCAN (Elevador).
    La direccion ("up" o "down") determina el movimiento inicial.
    """
    total_movement = 0
    current_pos = start_pos
    path = [current_pos] # Lista para guardar la ruta
    
    # Copiamos y ordenamos las solicitudes
    requests_copy = sorted(requests)
    
    if direction == "up":
        # 1. Separar solicitudes "hacia arriba" y "hacia abajo"
        up_requests = sorted([r for r in requests_copy if r >= current_pos])
        down_requests = sorted([r for r in requests_copy if r < current_pos], reverse=True) # Descendente
        
        # 2. Moverse "hacia arriba" atendiendo solicitudes
        for req in up_requests:
            total_movement += abs(req - current_pos)
            current_pos = req
            path.append(current_pos)
            
        # 3. Moverse al final del disco (4999)
        if not up_requests or up_requests[-1] != (MAX_CYLINDERS - 1):
            total_movement += abs((MAX_CYLINDERS - 1) - current_pos)
            current_pos = MAX_CYLINDERS - 1
            path.append(current_pos)
            
        # 4. Moverse "hacia abajo" atendiendo el resto
        for req in down_requests:
            total_movement += abs(req - current_pos)
            current_pos = req
            path.append(current_pos)
            
    else: # direction == "down"
        # 1. Separar solicitudes "hacia abajo" y "hacia arriba"
        down_requests = sorted([r for r in requests_copy if r <= current_pos], reverse=True) # Descendente
        up_requests = sorted([r for r in requests_copy if r > current_pos]) # Ascendente
        
        # 2. Moverse "hacia abajo" atendiendo solicitudes
        for req in down_requests:
            total_movement += abs(req - current_pos)
            current_pos = req
            path.append(current_pos)
        
        # 3. Moverse al inicio del disco (0)
        if not down_requests or down_requests[-1] != 0:
            total_movement += abs(0 - current_pos)
            current_pos = 0
            path.append(current_pos)
            
        # 4. Moverse "hacia arriba" atendiendo el resto
        for req in up_requests:
            total_movement += abs(req - current_pos)
            current_pos = req
            path.append(current_pos)
        
    return total_movement, path

def run_cscan(start_pos, requests, direction="up"):
    """
    Simula el algoritmo C-SCAN (SCAN Circular).
    La direccion ("up" o "down") determina el movimiento inicial.
    """
    total_movement = 0
    current_pos = start_pos
    path = [current_pos] # Lista para guardar la ruta
    
    # Copiamos y ordenamos las solicitudes
    requests_copy = sorted(requests)
    
    if direction == "up":
        # 1. Separar solicitudes "hacia arriba" y "hacia abajo"
        up_requests = sorted([r for r in requests_copy if r >= current_pos])
        down_requests = sorted([r for r in requests_copy if r < current_pos]) # Ascendente
        
        # 2. Moverse "hacia arriba" atendiendo solicitudes
        for req in up_requests:
            total_movement += abs(req - current_pos)
            current_pos = req
            path.append(current_pos)
            
        # 3. Moverse al final del disco (4999)
        if not up_requests or up_requests[-1] != (MAX_CYLINDERS - 1):
            total_movement += abs((MAX_CYLINDERS - 1) - current_pos)
            current_pos = MAX_CYLINDERS - 1
            path.append(current_pos)
            
        # 4. Saltar al inicio del disco (0)
        total_movement += (MAX_CYLINDERS - 1) # Movimiento de 4999 a 0
        current_pos = 0
        path.append(current_pos) # Añadir el "salto" al gráfico
        
        # 5. Moverse "hacia arriba" desde 0
        for req in down_requests:
            total_movement += abs(req - current_pos)
            current_pos = req
            path.append(current_pos)
            
    else: # direction == "down"
        # 1. Separar solicitudes
        down_requests = sorted([r for r in requests_copy if r <= current_pos], reverse=True) # Descendente
        up_requests = sorted([r for r in requests_copy if r > current_pos], reverse=True) # Descendente
        
        # 2. Moverse "hacia abajo" atendiendo solicitudes
        for req in down_requests:
            total_movement += abs(req - current_pos)
            current_pos = req
            path.append(current_pos)
        
        # 3. Moverse al inicio del disco (0)
        if not down_requests or down_requests[-1] != 0:
            total_movement += abs(0 - current_pos)
            current_pos = 0
            path.append(current_pos)
            
        # 4. Saltar al final del disco (4999)
        total_movement += (MAX_CYLINDERS - 1) # Movimiento de 0 a 4999
        current_pos = MAX_CYLINDERS - 1
        path.append(current_pos)
        
        # 5. Moverse "hacia abajo" desde 4999
        for req in up_requests:
            total_movement += abs(req - current_pos)
            current_pos = req
            path.append(current_pos)
            
    return total_movement, path

def plot_head_movement(fcfs_path, scan_path, cscan_path, totals):
    """
    Crea los gráficos de movimiento del cabezal para cada algoritmo.
    """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))
    fig.suptitle('Visualizacion del Movimiento del Cabezal', fontsize=16)
    
    # Gráfico FCFS
    ax1.plot(fcfs_path, 'r.-', markersize=2, label=f"FCFS (Total: {totals['FCFS']})")
    ax1.set_title('FCFS')
    ax1.set_ylabel('Número de Cilindro')
    ax1.set_ylim(0, MAX_CYLINDERS)
    ax1.set_xlabel('Orden de Solicitud')
    ax1.legend(loc='upper right')
    
    # Gráfico SCAN
    # Usamos 'range' para el eje X para que la gráfica sea legible
    ax2.plot(scan_path, 'g.-', markersize=2, label=f"SCAN (Total: {totals['SCAN']})")
    ax2.set_title('SCAN')
    ax2.set_ylabel('Número de Cilindro')
    ax2.set_ylim(0, MAX_CYLINDERS)
    ax2.set_xlabel('Orden de Servicio')
    ax2.legend(loc='upper right')
    
    # Gráfico C-SCAN
    ax3.plot(cscan_path, 'b.-', markersize=2, label=f"C-SCAN (Total: {totals['C-SCAN']})")
    ax3.set_title('C-SCAN')
    ax3.set_ylabel('Número de Cilindro')
    ax3.set_ylim(0, MAX_CYLINDERS)
    ax3.set_xlabel('Orden de Servicio')
    ax3.legend(loc='upper right')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('head_movement_comparison.png')
    # plt.show() # Descomenta si quieres que se abra la ventana

def plot_performance_comparison(totals):
    """
    Crea el gráfico de barras comparando el rendimiento total.
    """
    algorithms = list(totals.keys())
    movements = list(totals.values())
    
    plt.figure(figsize=(8, 6))
    colors = ['red', 'green', 'blue']
    bars = plt.bar(algorithms, movements, color=colors)
    
    plt.title('Comparacion de Rendimiento de Algoritmos', fontsize=16)
    plt.ylabel('Movimiento Total del Cabezal (Cilindros)')
    plt.xlabel('Algoritmo')
    
    # Añadir etiquetas con el valor total encima de cada barra
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:,.0f}', va='bottom', ha='center') # 'va' vertical alignment
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png')
    # plt.show() # Descomenta si quieres que se abra la

def main():
    """
    Funcion principal para ejecutar la simulacion.
    """
    # 1. Obtener posicion inicial desde la línea de comandos
    try:
        if len(sys.argv) != 2:
            raise ValueError()
        start_position = int(sys.argv[1])
        if not (0 <= start_position < MAX_CYLINDERS):
            raise ValueError()
    except ValueError:
        print(f"Error: Debes proporcionar una posicion inicial válida (0 - {MAX_CYLINDERS - 1}).")
        print(f"Ejemplo: python {sys.argv[0]} 100")
        sys.exit(1)

    print(f"Simulacion de Planificacion de Disco")
    print(f"Disco de {MAX_CYLINDERS} cilindros (0-{MAX_CYLINDERS-1}).")
    print(f"{NUM_REQUESTS} solicitudes aleatorias.")
    print(f"Posicion inicial del cabezal: {start_position}\n")

    # 2. Generar solicitudes aleatorias
    # Usamos una copia para que FCFS reciba la lista en el orden original
    random_requests = [random.randint(0, MAX_CYLINDERS - 1) for _ in range(NUM_REQUESTS)]
    
    # 3. Ejecutar algoritmos
    fcfs_total, fcfs_path = run_fcfs(start_position, random_requests)
    scan_total, scan_path = run_scan(start_position, random_requests)
    cscan_total, cscan_path = run_cscan(start_position, random_requests)

    """  Para direccion "down" """
    #scan_total, scan_path = run_scan(start_position, random_requests, direction="down")
    #cscan_total, cscan_path = run_cscan(start_position, random_requests, direction="down")

    # 4. Reportar resultados
    print("--- Resultados de Movimiento Total ---")
    print(f"FCFS:   {fcfs_total:,.0f} cilindros")
    print(f"SCAN:   {scan_total:,.0f} cilindros")
    print(f"C-SCAN: {cscan_total:,.0f} cilindros\n")
    
    totals = {
        'FCFS': fcfs_total,
        'SCAN': scan_total,
        'C-SCAN': cscan_total
    }

    # 5. Generar Visualizaciones
    print("Generando gráficos de visualizacion...")
    try:
        plot_performance_comparison(totals)
        plot_head_movement(fcfs_path, scan_path, cscan_path, totals)
        print("Gráficos 'performance_comparison.png' y 'head_movement_comparison.png' guardados.")
    except Exception as e:
        print(f"Error al generar gráficos: {e}")
        print("Asegúrate de tener 'matplotlib' instalado (pip install matplotlib)")

if __name__ == "__main__":
    main()