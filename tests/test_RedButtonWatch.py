import time
from context import atruck
from atruck.RedButtonWatch import RedButtonWatch
from atruck.TruckStatus import TruckStatus

if __name__ == "__main__":
    status = TruckStatus()
    rbw = RedButtonWatch(status)
    rbw.start()

    for _ in range(100):
        print(status.over)
        time.sleep(0.2)

        rbw.join()
