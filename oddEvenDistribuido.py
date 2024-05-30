from mpi4py import MPI
import numpy as np

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def compare_split(a, rank, partner, comm):
    send_data = np.copy(a)
    recv_data = np.empty_like(a)
    
    comm.Send(send_data, dest=partner)
    comm.Recv(recv_data, source=partner)
    
    if rank < partner:
        combined = np.concatenate((a, recv_data))
        combined.sort()
        a[:] = combined[:len(a)]
    else:
        combined = np.concatenate((recv_data, a))
        combined.sort()
        a[:] = combined[-len(a):]

def even_odd_sort(L):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    n = len(L) if rank == 0 else 0
    n = comm.bcast(n, root=0)
    m = n // size

    local_a = np.empty(m, dtype=int)
    comm.Scatter(L, local_a, root=0)

    merge_sort(local_a)

    for k in range(size):
        if (k + rank) % 2 == 0:
            if rank < size - 1:
                compare_split(local_a, rank, rank + 1, comm)
        else:
            if rank > 0:
                compare_split(local_a, rank, rank - 1, comm)

    comm.Gather(local_a, L, root=0)

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        L = np.random.randint(0, 100, size=16)
        print("Unsorted array:", L)
    else:
        L = None

    even_odd_sort(L)

    if rank == 0:
        print("Sorted array:", L)

if __name__ == "__main__":
    main()
