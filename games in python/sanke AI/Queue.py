class MyNode:
    def __init__(self, x, y, next) -> None:
        self.x = x
        self.y = y
        self.next = next

    def __del__(self):
        pass


class Queue:

    def __init__(self) -> None:
        self.sz = 0
        self.a = None
        self.back = None

    def size(self) -> int:
        return self.sz

    def front(self):
        return self.a.x, self.a.y

    def back(self):
        return self.back.x, self.back.y

    def push(self, x, y):
        if self.size() == 0:
            self.a = MyNode(x, y, None)
            self.back = self.a
        else:
            back = MyNode(x, y, None)
            self.back.next = back
            self.back = back
        self.sz += 1

    def pop(self):
        b = self.a
        self.a = self.a.next
        self.sz -= 1
        b.__del__()
