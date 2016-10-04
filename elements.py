class _Elements:
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


class Project(_Elements):
    def __init__(self, title="", analyst_name="", date="", summary_report=""):
        exp = "PROJECT, %s, %s, %s, %s" % (str(title), str(analyst_name), str(date), str(summary_report))
        super().__init__(exp)


class Replicate(_Elements):
    def __init__(self, num_replications="", begin_time="", replication_len="", init_system="", init_stats="", warmup_period=""):
        exp = "REPLICATE, %s, %s, %s, %s, %s, %s" % (
            str(num_replications), str(begin_time), str(replication_len),
            str(init_system), str(init_stats), str(warmup_period)
        )
        super().__init__(exp)


class Discrete(_Elements):
    def __init__(self, max_entities="", max_attr="", max_queue_num="", max_station_num="", animation_attr=""):
        exp = 'DISCRETE, {}, {}, {}, {}, {}'.format(max_entities, max_attr, max_queue_num, max_station_num, animation_attr)
        super().__init__(exp)


class Trace(_Elements):
    def __init__(self, begin_time="", end_time="", condition="", expression=""):
        exp = 'TRACE, {}, {}, {}, {}'.format(begin_time, end_time, condition, expression)
        super().__init__(exp)


class _Begin(_Elements):
    def __init__(self, listing="", run_controller=""):
        exp = "BEGIN, %s, %s" % (str(listing), str(run_controller))
        super().__init__(exp)


class _End(_Elements):
    def __init__(self):
        exp = "END"
        super().__init__(exp)


class _Queues(_Elements):
    def __init__(self):
        exp = "QUEUES"
        super().__init__(exp)


class _Resources(_Elements):
    def __init__(self):
        exp = "RESOURCES"
        super().__init__(exp)


class _Counters(_Elements):
    def __init__(self):
        exp = "COUNTERS"
        super().__init__(exp)


class _Attributes(_Elements):
    def __init__(self):
        exp = "ATTRIBUTES"
        super().__init__(exp)


class _Variables(_Elements):
    def __init__(self):
        exp = "VARIABLES"
        super().__init__(exp)


class _Dstats(_Elements):
    def __init__(self):
        exp = "DSTATS"
        super().__init__(exp)


class _Tallies(_Elements):
    def __init__(self):
        exp = "TALLIES"
        super().__init__(exp)


class _Storages(_Elements):
    def __init__(self):
        exp = "STORAGES"
        super().__init__(exp)


class _Seeds(_Elements):
    def __init__(self):
        exp = "SEEDS"
        super().__init__(exp)


class _Outputs(_Elements):
    def __init__(self):
        exp = "Outputs"
        super().__init__(exp)


# SIMAN does not define Entities as Elements. But, programatically very similar.
class _Entities(_Elements):
    def __init__(self):
        exp = "ENTITIES"
        super().__init__(exp)


"""ELEMENT STORAGE CLASSES"""
# todo: should these classes just be a dict or list?
class _Element:
    """Base Element storage class"""

    def __init__(self, name, attributes):
        self.name = name
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
        self.ranking_criterion = ranking_criterion

        attributes = [number, name, ranking_criterion]
        super().__init__(name, attributes)


class Resource(_Element):
    """Resource storage class"""
    def __init__(self, number="", name="", capacity=""):
        self.number = number
        self.capacity = capacity

        attributes = [number, name, capacity]
        super().__init__(name, attributes)


class Counter(_Element):
    """Counter storage class"""
    def __init__(self, number="", name="", limit="", init_option="", output_file="", report_id=""):
        self.number = number
        self.limit = limit
        self.init_option = init_option
        self.output_file = output_file
        self.report_id = report_id

        attributes = [number, name, limit, init_option, output_file, report_id]
        super().__init__(name, attributes)


class Attribute(_Elements):
    def __init__(self, number="", name="", init_values=""):
        self.number = number
        self.init_values = init_values

        attributes = (number, name, init_values)
        super().__init__(name, attributes)


class Variable(_Elements):
    def __init__(self, number="", name="", init_values=""):
        self.number = number
        self.init_values = init_values

        attributes = (number, name, init_values)
        super().__init__(name, attributes)


class Dstat(_Element):
    def __init__(self, number="", name="", expression="", output_file="", report_id=""):
        self.number = number
        self.expression = expression
        self.output_file = output_file
        self.report_id = report_id

        attributes = (number, name, expression, output_file, report_id)
        super().__init__(name, attributes)


class Tally(_Element):
    def __init__(self, number="", name="", output_file="", report_id=""):
        self.number = number
        self.output_file = output_file
        self.report_id = report_id

        attributes = (number, name, output_file, report_id)
        super().__init__(name, attributes)


class Storage(_Element):
    def __init__(self, number="", name=""):
        self.number = number

        attributes = (number, name)
        super().__init__(name, attributes)

class Output(_Element):
    def __init__(self, number="", name="", expression="", output_file="", report_id=""):
        self.number = number
        self.expression = expression
        self.output_file = output_file
        self.report_id = report_id

        attributes = (number, name, expression, output_file, report_id)
        super().__init__(name, attributes)


# todo: determine how seeds should work. Does not fit number/name scheme
class Seed(_Element):
    def __init__(self, name="", seed_value="", init_option=""):
        self.seed_value = seed_value
        self.init_option = init_option

        attributes = (name, seed_value, init_option)
        super().__init__(name, attributes)



# todo: include other attributes
class Entity(_Element):
    """Entity storage class"""
    def __init__(self, name=""):
        attributes = [name]
        super().__init__(name, attributes)