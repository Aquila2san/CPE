# CPE 2026
# CPE 2000
from multiprocessing import Pipe
import array
if __name__ == "__main__" :
    a, b = Pipe(duplex=True)  # comme pour os.pipe()
    
    # Echange de simple liste
    a.send([1, 'hello', None])
    print("b.recv() envoyé par a", b.recv())
    # [1, 'hello', None]

    # Echange de bytes
    b.send_bytes(b'thank you')
    print("a.recv() envoyé par b", a.recv_bytes())
    # b'thank you'
    
    # Echange de tableau (array)
    arr1 = array.array('i', range(5))
    arr2 = array.array('i', [0] * 10)
    a.send_bytes(arr1)
    count = b.recv_bytes_into(arr2)
    print(f"{count=}")
    assert count == len(arr1) * arr1.itemsize
    print(arr2)
    # array('i', [0, 1, 2, 3, 4, 0, 0, 0, 0, 0])
