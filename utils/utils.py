class AverageQueue:
    def __init__(self, length: int = 25):
        self.maxlen = length
        self.queue = []

    def add(self, item: float):
        if len(self.queue) >= self.maxlen:
            self.queue.pop(0)
        self.queue.append(item)

    def avg(self) -> float:
        total = sum(self.queue)
        return total / len(self.queue)
