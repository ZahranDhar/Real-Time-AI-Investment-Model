import threading
import time
from StocksProcessor import stocksprocessor


# Create two instances of stocksprocessor class
process1 = stocksprocessor()
process2 = stocksprocessor()

# Create two threads targeting the run method of each object
thread1 = threading.Thread(target=process1.run)
thread2 = threading.Thread(target=process2.run)

# Start the threads
thread1.start()
time.sleep(5)
thread2.start()

# Wait for both threads to complete
thread1.join()
thread2.join()

