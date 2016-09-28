class Elements:
    def __init__(self, exp):
        self._exp = exp
        self.elements = []

    def __str__(self):
        return self._exp + ";"

    def update(self, element):
        self._exp += str(element)
        self.elements.append(element)


class Project(Elements):
    def __init__(self, title="", analyst_name="", date="", summary_report=""):
        exp = "PROJECT, %s, %s, %s, %s;" % (str(title), str(analyst_name), str(date), str(summary_report))
        super().__init__(exp)


# class Discrete(Element):

# todo: each class contains all the elements. Need a way to store all elements. Perhaps a subclass.
class Queues(Elements):

    def __init__(self):
        exp = "QUEUES"
        super().__init__(exp)

    def add(self, number="", name="", ranking_criterion=""):
        q = _Queue(number, name, ranking_criterion)
        self.update(q)


class Resources(Elements):
    def __init__(self):
        exp = "RESOURCES"
        super().__init__(exp)

    def add(self, number="", name="", capacity=""):
        r = _Resource(number, name, capacity)
        self.update(r)


class _Queue:
    def __init__(self, number="", name="", ranking_criterion=""):
        self.number = number
        self.name = name
        self.ranking_criterion = ranking_criterion

    def __str__(self):
        return ": %s, %s, %s" % (str(self.number), str(self.name), str(self.ranking_criterion))


class _Resource:
    def __init__(self, number="", name="", capacity=""):
        self.number = number
        self.name = name
        self.capacity = capacity

    def __str__(self):
        return ": %s, %s, %s" % (str(self.number), str(self.name), str(self.capacity))

q = Queues()
q.add(1)
print(q)