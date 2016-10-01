class Elements:
    """Base Elements class"""
    def __init__(self, exp):
        self._exp = exp
        self.elements = []
        self.type = "exp"

    def __str__(self):
        return self._exp + ";"

    # Add Element (unique) to container and add to .exp string
    # todo: better formatting for Elements string. Should be multiline
    def add(self, element):
        if element not in self.elements:
            self._exp += str(element)
            self.elements.append(element)


class Project(Elements):
    def __init__(self, title="", analyst_name="", date="", summary_report=""):
        exp = "PROJECT, %s, %s, %s, %s" % (str(title), str(analyst_name), str(date), str(summary_report))
        super().__init__(exp)


class Replicate(Elements):
    def __init__(self, num_replications="", begin_time="", replication_len="", init_system="", init_stats="", warmup_period=""):
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


class Resources(Elements):
    def __init__(self):
        exp = "RESOURCES"
        super().__init__(exp)


class Counters(Elements):
    def __init__(self):
        exp = "COUNTERS"
        super().__init__(exp)


# SIMAN does not define Entities as Elements. But, programatically very similar.
class Entities(Elements):
    def __init__(self):
        exp = "ENTITIES"
        super().__init__(exp)


"""ELEMENT STORAGE CLASSES"""
# todo: should these classes just be a dict or list?
class _Element:
    """Base Element storage class"""

    def __init__(self, attributes):
        self.attributes = attributes

    def __str__(self):
        return ': ' + ', '.join(str(x) for x in self.attributes)

    def __eq__(self, other):
        if hasattr(self, 'number'):
            return self.name == other.name and self.number == other.number
        else:
            return self.name == other.name

    def __ne__(self, other):
        if hasattr(self, 'number'):
            return self.name != other.name or self.number != other.number
        else:
            return self.name != other.name

    def __hash__(self):
        if hasattr(self, 'number'):
            return hash(('number', self.number, 'name', self.name))
        else:
            return hash(('name', self.name))


class Queue(_Element):
    """Queue storage class"""
    def __init__(self, number="", name="", ranking_criterion=""):
        self.number = number
        self.name = name
        self.ranking_criterion = ranking_criterion

        attributes = [number, name, ranking_criterion]
        super().__init__(attributes)


class Resource(_Element):
    """Resource storage class"""
    def __init__(self, number="", name="", capacity=""):
        self.number = number
        self.name = name
        self.capacity = capacity

        attributes = [number, name, capacity]
        super().__init__(attributes)


class Counter(_Element):
    """Counter storage class"""
    def __init__(self, number="", name="", limit="", init_option="", output_file="", report_id=""):
        self.number = number
        self.name = name
        self.limit = limit
        self.init_option = init_option
        self.output_file = output_file
        self.report_id = report_id

        attributes = [number, name, limit, init_option, output_file, report_id]
        super().__init__(attributes)


# todo: include other attributes
class Entity(_Element):
    """Entity storage class"""
    def __init__(self, name=""):
        self.name = name

        attributes = [name]
        super().__init__(attributes)