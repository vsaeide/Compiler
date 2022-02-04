class Stack:
    def __init__(self):
        self.stack = []
        self.size = 0

    def pop(self, num=1):
        if num > self.size:
            raise Exception('pop size bigger than stack size!, {}, {}'.format(self.size, num))
        self.stack = self.stack[:self.size-num]
        self.size -= num

    def push(self, key):
        self.stack.append(key)
        self.size += 1

    def empty(self):
        self.stack = []
        self.size = 0

    def top(self):
        return self.stack[self.size-1]

    def get_from_top(self, i):
        if i >= self.size:
            raise Exception("More than stack size!")
        return self.stack[self.size - i - 1]

    def get_index(self, key):
        for i in range(len(self.stack)):
            if self.stack[i] == key:
                return i
        return -1