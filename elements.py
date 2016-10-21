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
        exp = "PROJECT, {}, {}, {}, {}".format(title, analyst_name, date, summary_report)
        super().__init__(exp)


# todo: find out what 3 missing params are
class Replicate(_Elements):
    def __init__(self, num_replications="", begin_time="", replication_len="", init_system="", init_stats="",
                 warmup_period="", hours_per_day=24, base_time_unit=""):
        exp = "REPLICATE, {}, {}, {}, {}, {}, {},,,{}, {}".format(num_replications, begin_time, replication_len,
                                                                  init_system, init_stats, warmup_period, hours_per_day,
                                                                  base_time_unit)
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
        exp = "OUTPUTS"
        super().__init__(exp)


class _Stations(_Elements):
    def __init__(self):
        exp = "STATIONS"
        super().__init__(exp)


class _Sequences(_Elements):
    def __init__(self):
        exp = "SEQUENCES"
        super().__init__(exp)


class _Transporters(_Elements):
    def __init__(self):
        exp = "TRANSPORTERS"
        super().__init__(exp)


#class _Distances(_Elements):
#    def __init__(self):
#        exp = "DISTANCES"
#        super().__init__(exp)


class Sets(_Elements):
    def __init__(self):
        exp = "SETS"
        super().__init__(exp)


# SIMAN does not define Entities as Elements. But, programatically very similar.
class _Entities(_Elements):
    def __init__(self):
        exp = "ENTITIES"
        super().__init__(exp)


"""ELEMENT STORAGE CLASSES"""
class _Element:
    """Base Element storage class"""

    def __init__(self, name, attributes, number=None):
        self.name = name
        self.number = number
        self.attributes = attributes
        self.type = "element"

    def __str__(self):
        num = str(self.number) + ', ' if self.number else ''
        return ': ' + num + ', '.join(str(x) for x in self.attributes)

    def __eq__(self, other):
        if self.number:
            return self.name == other.name and self.number == other.number
        else:
            return self.name == other.name

    def __ne__(self, other):
        if self.number:
            return self.name != other.name or self.number != other.number
        else:
            return self.name != other.name

    def __hash__(self):
        if self.number:
            return hash(('number', self.number, 'name', self.name))
        else:
            return hash(('name', self.name))


class Queue(_Element):
    """Queue storage class"""
    def __init__(self, number="", name="", ranking_criterion=""):
        self.ranking_criterion = ranking_criterion

        attributes = [name, ranking_criterion]
        super().__init__(name, attributes, number)


class Resource(_Element):
    """Resource storage class"""
    def __init__(self, number="", name="", capacity=""):
        self.capacity = capacity

        attributes = [name, capacity]
        super().__init__(name, attributes, number)


class Counter(_Element):
    """Counter storage class"""
    def __init__(self, number="", name="", limit="", init_option="", output_file="", report_id=""):
        self.limit = limit
        self.init_option = init_option
        self.output_file = output_file
        self.report_id = report_id

        attributes = [name, limit, init_option, output_file, report_id]
        super().__init__(name, attributes, number)


class Attribute(_Element):
    def __init__(self, number="", name="", init_values=""):
        self.init_values = init_values

        attributes = (name, init_values)
        super().__init__(name, attributes, number)


class Variable(_Element):
    def __init__(self, number="", name="", init_values=""):
        self.init_values = init_values

        attributes = (name, init_values)
        super().__init__(name, attributes, number)


class Dstat(_Element):
    def __init__(self, number="", name="", expression="", output_file="", report_id=""):
        self.expression = expression
        self.output_file = output_file
        self.report_id = report_id

        attributes = (expression, name, output_file, report_id)
        super().__init__(name, attributes, number)


class Tally(_Element):
    def __init__(self, number="", name="", output_file="", report_id=""):
        self.output_file = output_file
        self.report_id = report_id

        attributes = (name, output_file, report_id)
        super().__init__(name, attributes, number)


class Storage(_Element):
    def __init__(self, number="", name=""):
        attributes = (name)
        super().__init__(name, attributes, number)


class Output(_Element):
    def __init__(self, number="", name="", expression="", output_file="", report_id=""):
        self.number = number
        self.expression = expression
        self.output_file = output_file
        self.report_id = report_id

        attributes = (number, name, expression, output_file, report_id)
        super().__init__(name, attributes)


class Station(_Element):
    def __init__(self, number="", name="", intersection_id="", recipe_id=""):
        self.number = number
        self.intersection_id = intersection_id
        self.recipe_id = recipe_id

        attributes = (number, name, intersection_id, recipe_id)
        super().__init__(name, attributes)


class Sequence(_Element):
    def __init__(self, number="", name="", station_id="", variable=None, value=None):
        self.number = number
        self.steps = [[station_id, variable, value]]

        attributes = [number, name, self.to_string(station_id, variable, value)]
        super().__init__(name, attributes)

    def add(self, station_id="", variable="", value=""):
        self.steps.append([station_id, variable, value])
        self.attributes[2] += ' & ' + self.to_string(station_id, variable, value)

    def to_string(self, station_id, variable, value):
        if variable and value:
            return '{}, {} = {}'.format(station_id, variable, value)
        else:
            return str(station_id)


class Transporter(_Element):
    def __init__(self, number="", name="", num_units="", system_map_type="", velocity=""):
        self.number = number
        self.num_units = num_units
        self.system_map_type = system_map_type
        self.velocity = velocity

        attributes = (number, name, num_units, system_map_type, velocity)
        super().__init__(name, attributes)


#class Distance(_Element):
#    def __init__(self, name, start_station_id, end_station_id, distance):

class Set(_Element):
    def __init__(self, number="", name="", members=[]):
        assert isinstance(members, (tuple, list))

        self.number = number
        self.members = members

        attributes = (number, name, ', '.join(members))
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