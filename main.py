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

def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

def main():
    while True:
        print("-------------------------")
        print("Paso de mensajes con MPI en Python\n")
        x = input("Ingresa el numero de procesos a usar: ")

        if x == "exit":
            print("Saliendo del programa...")
            break

        if is_power_of_two(int(x)) == False or int(x) < 2:
            print("El número de procesos debe ser mayor a 1")
            print("El numero de procesos debe ser una potencia de 2\n")
            continue
    
        print("\nProgramas disponibles:\n")
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
            run_command(n=x, program='oneforallcero.py', params=[source])

        elif option == "2":

            source = input("Ingresa el mensaje: ")

            node = input("Ingresa el nodo origen: ")

            while int(node) >= int(x) or int(node) < 0:
                print("El nodo origen no puede ser mayor o igual al número de procesos")
                node = input("Ingresa el nodo origen: ")

            run_command(n=x, program='oneforall.py', params=[source, node])

        elif option == "3":

            m = input("Ingresa el tamaño del vector: ")

            if not is_power_of_two(int(m)):
                print("El tamaño del vector debe ser una potencia de 2")
                print("Se usará un tamaño de 10\n")
                m = 10

            source = input("Ingresa el vector a reducir (random, my_id, ones): ")

            while not (source in ["random", "my_id", "ones"]):
                print("random: Vector aleatorio")
                print("my_id: Vector con el id del procesador")
                print("ones: Vector de unos")
                source = input("Ingresa el vector a reducir (random, my_id, ones): ")

            run_command(program='reduceAllToOne.py', params=[m, source])

        elif option == "4":

            print("Se ejecutará el programa con 16 procesos siempre\n")

            vector = input("Ingresa el vector a ordenar (random, reverse, reverse_from): ")

            while not (vector in ["random", "reverse", "reverse_from"]):
                print("random: Vector aleatorio")
                print("reverse: Vector ordenado de forma descendente")
                print("reverse_from: Vector ordenado de forma descendente desde un número dado")
                vector = input("Ingresa el vector a ordenar (random, reverse, reverse_from): ")

            if vector == "reverse_from":
                x = input("Ingresa el número desde el cual se ordenará de forma descendente: ")
                if int(x) < 16:
                    print("El número debe ser mayor o igual a 16")
                    print("Se usará el número 16\n")
                    x = 16

                command = "--reverse_from"
                run_command(n=16, program='oddEvenDistribuido.py', params=[command, x])

            if vector == "reverse":
                command = "--vector"
                run_command(n=16, program='oddEvenDistribuido.py', params=[command, vector])

            if vector == "random":
                command = "--vector"
                run_command(n=16, program='oddEvenDistribuido.py', params=[command, vector])


        elif option == "5":
            run_command(n=4, program='MultiplicacionMatricesDistribuido.py', params=[])
        elif option == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida")
            continue

        time.sleep(3)

if __name__ == '__main__':
    main()