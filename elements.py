class Elements:
    """Base Elements class"""
    def __init__(self, exp):
        self._exp = exp
        self.elements = []
        self.ext = "exp"

    def __str__(self):
        return self._exp + ";"

    def add(self, element):
        self._exp += str(element)
        self.elements.append(element)


class Project(Elements):
    def __init__(self, title="", analyst_name="", date="", summary_report=""):
        exp = "PROJECT, %s, %s, %s, %s" % (str(title), str(analyst_name), str(date), str(summary_report))
        super().__init__(exp)


class Replicate(Elements):
    def __init__(self, num_replications, begin_time, replication_len, init_system, init_stats, warmup_period):
        exp = "REPLICATE, %s, %s, %s, %s, %s, %s" % (
            str(num_replications), str(begin_time), str(replication_len),
            str(init_system), str(init_stats), str(warmup_period)
        )
        super().__init__(exp)


class Discrete(Elements):
    def __init__(self, max_entities):
        exp = "DISCRETE, %s" % str(max_entities)
        super().__init__(exp)


class Begin(Elements):
    def __init__(self, listing="", run_controller=""):
        exp = "BEGIN, %s, %s" % (str(listing), str(run_controller))
        super().__init__(exp)


class End(Elements):
    def __init__(self):
        exp = "END"
        super().__init__(exp)


class Queues(Elements):

    def __init__(self):
        exp = "QUEUES"
        super().__init__(exp)

    def add(self, number="", name="", ranking_criterion=""):
        e = _Queue(number, name, ranking_criterion)
        super().add(e)


class Resources(Elements):
    def __init__(self):
        exp = "RESOURCES"
        super().__init__(exp)

    def add(self, number="", name="", capacity=""):
        e = _Resource(number, name, capacity)
        super().add(e)


class Counters(Elements):
    def __init__(self):
        exp = "COUNTERS"
        super().__init__(exp)

    def add(self, number, name, limit, init_option, output_file, report_id):
        e = _Counter(number, name, limit, init_option, output_file, report_id)
        super().add(e)


# SIMAN does not define Entities as Elements. But, programatically very similar.
class Entities(Elements):
    def __init__(self):
        exp = "ENTITIES"
        super().__init__(exp)

    def add(self, name):
        e = _Entity(name)
        super().add(e)

"""ELEMENT STORAGE CLASSES"""
# todo: should these classes just be a dict or list?
class _Element:
    """Base Element storage class"""

    def __str__(self):
        return ': ' + ', '.join(str(x) for x in self.__dict__.values())


class _Queue(_Element):
    """Queue storage class"""
    def __init__(self, number="", name="", ranking_criterion=""):
        self.number = number
        self.name = name
        self.ranking_criterion = ranking_criterion
        super().__init__()


class _Resource(_Element):
    """Resource storage class"""
    def __init__(self, number="", name="", capacity=""):
        self.number = number
        self.name = name
        self.capacity = capacity
        super().__init__()


class _Counter(_Element):
    """Counter storage class"""
    def __init__(self, number, name, limit, init_option, output_file, report_id):
        self.number = number
        self.name = name
        self.limit = limit
        self.init_option = init_option
        self.output_file = output_file
        self.report_id = report_id
        super().__init__()

# todo: include other attributes
class _Entity(_Element):
    """Entity storage class"""
    def __init__(self, name):
        self.name = name
        super().__init__()

q = Queues()
q.add(1)
print(q)