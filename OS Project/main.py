import time
import random
import threading


#Producer consumer code start

class Semaphore():
    def __init__(self, initial=0):
        self.lock = threading.Condition(threading.Lock())
        self.value = initial

    def up(self):
        with self.lock:
            self.value += 1
            self.lock.notify()

    def down(self):
        with self.lock:
            while self.value == 0:
                self.lock.wait()
            self.value -= 1


class Memory():
    def __init__(self):
        self.buffer_mutex = Semaphore(1)
        self.fill_count = Semaphore(0)
        self.empty_count = Semaphore(100)
        self.memory_buffer = []


class Consumer(threading.Thread):
    def __init__(self, memory, producer=None):
        super().__init__()
        self.memory = memory
        self.producer = producer
        self.sleep()

    def wake(self):
        self.awake = True
        self.asleep = False

    def sleep(self):
        self.awake = False
        self.asleep = True

    def run(self):
        while True:
            self.consume()

    def consume(self):
        self.memory.fill_count.down()
        self.memory.buffer_mutex.down()
        item = self.memory.memory_buffer.pop()
        print("Consumer consumes the item {}".format(item))
        self.memory.buffer_mutex.up()
        self.memory.empty_count.up()


class Producer(threading.Thread):
    def __init__(self, memory, consumer=None):
        super().__init__()
        self.memory = memory
        self.consumer = consumer
        self.wake()

    def wake(self):
        self.awake = True
        self.asleep = False

    def sleep(self):
        self.awake = False
        self.asleep = True

    def run(self):
        while True:
            self.produce()

    def produce(self):
        it = random.randint(1, 10)
        print("Producer produces {}".format(it))
        self.memory.empty_count.down()
        self.memory.buffer_mutex.down()
        self.memory.memory_buffer.append(it)
        print("Producer put {} in buffer memory".format(it))
        self.memory.buffer_mutex.up()
        self.memory.fill_count.up()




def mainPC():
    memory = Memory()
    consumer = Consumer(memory)
    producer = Producer(memory)
    consumer.producer = producer
    producer.consumer = consumer
    consumer.daemon = True
    producer.daemon = True
    consumer.start()
    producer.start()

    while True:
        if consumer.asleep and producer.asleep:
            print("Deadlock ocurred")
            break
#Producer Consumer Code End

#Petersons code start
class MemoryPet():
    def __init__(self, processes):
        self.quantity = processes
        self.flag = [False] * processes
        self.turn = 0

    def calculate_next_process(self, process):
        return (process + 1) % self.quantity

    def enter_region(self, thread):
        other = self.calculate_next_process(thread)
        self.flag[thread] = True
        turn = thread
        while self.turn == thread and self.flag[other]:
            time.sleep(random.randint(1, 3))

    def leave_region(self, thread):
        self.flag[thread] = False


class ProcessPet(threading.Thread):
    def __init__(self, id, memory):
        super().__init__()
        self.id = id
        self.memory = memory
        self.incriticarea = False

    def run(self):
        while True:
            while self.memory.turn != self.id:
                time.sleep(random.randint(1, 3))

            self.memory.enter_region(self.id)
            self.incriticarea = True
            print("Process {} is in the critic area".format(self.id))
            time.sleep(random.randint(1, 5))

            self.memory.leave_region(self.id)
            self.incriticarea = False
            print("Process {} left the critic area".format(self.id))

            self.memory.turn = self.memory.calculate_next_process(self.id)
            time.sleep(1)


def mainPet():
    n = int(input("Type the quantity of processes: "))
    memory = MemoryPet(n)
    processes = []
    for i in range(n):
        p = ProcessPet(i, memory)
        p.daemon = True
        print("Create Process {}".format(i))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

#Peterson code end

#Dinner code start
spoon = [False] * 5
philosofers = ["A", "B", "C", "D", "E"]


class Philosofer(threading.Thread):
    def __init__(self, id):

        super().__init__()
        self.id = philosofers[id]
        self.left = id
        self.right = (id + 1) % len(spoon)
        self.n_spoon = 0
        self.waiting = False
        self.eating = False
        self.thinking = True

    def run(self):

        while True:
            self.think()
            self.eat()

    def think(self):

        self.thinking = True
        print("Philosofer {} is thinking...".format(self.id))
        time.sleep(random.randint(1, 5))

    def eat(self):

        self.take_spon(self.left)
        self.take_spon(self.right)
        self.thinking = False
        self.eating = True
        print("Philosofer {} is eating...".format(self.id))
        time.sleep(random.randint(1, 10))
        self.eating = False
        self.return_spon(self.left)
        self.return_spon(self.right)
        print("Philosofer {} over your meal".format(self.id))

    def take_spon(self, i):

        if self.n_spoon >= 0 or self.n_spoon < 2:
            self.waiting = True
            while spoon[i]:
                print("Philosofer {} waiting the chop stick {}".format(self.id, i))
                time.sleep(random.randint(1, 5))
            self.waiting = False
            self.n_spoon += 1
            spoon[i] = True
            print("Philosofer {} took the chop stick {}".format(self.id, i))

    def return_spon(self, i):

        spoon[i] = False
        self.n_spoon -= 1
        print("Philosofer {} returned the chop stick {}".format(self.id, i))


def mainDinner():
    print("Philosofer's dinner is starting")
    filosofos = []
    for i in range(5):
        print("Philosofer {} arrive".format(philosofers[i]))
        a = Philosofer(i)
        a.start()
        filosofos.append(a)

    while True:
        # If all spoon are taken by the philosofers and all the philosofers are waiting other spon
        if all(spoon) and all(i.waiting for i in filosofos):
            print("Deadlock ocurred")
            break
    print("Dining Philosophers  is over")

#Dinners code end

def menu():
    print("Process Synchronization\n")

    # using the while loop to print menu list


while True:
    print("==================Process Synchronization=================")
    print("1. Producer Consumer Algorithm ")
    print("2. Peterson Algorithm")
    print("3. Dining Philosophers")
    print("4. Exit")
    users_choice = int(input("\nEnter your Choice: "))


    if users_choice == 1:
        print("\n=============Producer Consumer Algorithm=============\n")
        mainPC()

    elif users_choice == 2:
        print("\n=============Peterson Algorithm=============\n")
        mainPet()

    elif users_choice == 3:
        print("\n=============Dining Philosophers =============\n")
        mainDinner()
    elif users_choice == 4:
        raise SystemExit

if __name__ == "__main__":
   menu()