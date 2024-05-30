import subprocess
import time

def run_command(n = 4, program = '', params = []):
    command = ['mpiexec', '-n', str(n), 'py', '-m', 'mpi4py', program] + params
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Output:\n")
        print(result.stdout)
        print("Errors:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        print(f"Salida del comando: {e.output}")

if __name__ == '__main__':
    while True:
        print("-------------------------")
        print("Paso de mensajes con MPI en Python\n")
        print("1. one for all from 0")
        print("2. one for all from any")
        print("3. reduce all for one")
        print("4. odd even distribution")
        print("5. matrix multiplication")
        print("6. exit")
        print("-------------------------")

        option = input("Elige el programa a ejecutar: ")
        print("\n")

        if option == "1":
            source = input("Ingresa el mensaje: ")
            run_command(program='oneforallcero.py', params=[source])
        elif option == "2":
            run_command(program='oneforall.py', params=[])
        elif option == "3":
            run_command(program='reduceallforone.py', params=[])
        elif option == "4":
            run_command(program='oddeven.py', params=[])
        elif option == "5":
            run_command(program='MultiplicacionMatricesDistribuido.py', params=[])
        elif option == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida")
            continue

        time.sleep(3)
