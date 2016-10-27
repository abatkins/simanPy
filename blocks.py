from elements import Queue, Variable, Attribute
# TODO: Add param class that simply returns discrete list of params for a given block/elem. Example: param.branchtype.if
# TODO: Better handling for modifiers like NEXT() and MARK(). Either set both independently or "add modifier" to pass both.


class Block:
    def __init__(self, mod, element=None):
        self._mod = mod
        self.type = 'mod'
        self.element = element
        self._modifiers = None

    def __str__(self):
        if self._modifiers:
            mod_string = ': '.join(self._modifiers)
            return self._mod + ': {};'.format(mod_string)
        else:
            return self._mod + ";"

    # Add modifiers to block tail. EX: NEXT() / MARKS()
    def set_modifiers(self, modifiers):
        assert isinstance(modifiers, (list, tuple))
        self._modifiers = modifiers

    # For Repeats
    # todo: better formatting for repeats. Dynamic padding.
    def add(self, add_list):
        self._mod += ':\n\t\t{}'.format((', '.join(add_list)))


# todo: determine if element_ids should be passed to block as string or an object
class CreateBlock(Block):
    def __init__(self, entity, batch_size="", offset_time="", interval="", maximum_batches=""):
        mod = 'CREATE, {}, {}, {}: {}, {}'.format(batch_size, offset_time, entity.name, interval, maximum_batches)
        super().__init__(mod, entity)


class QueueBlock(Block):
    def __init__(self, queue, capacity="", balk_label=""):
        assert isinstance(queue, Queue)
        mod = 'QUEUE, {}, {}, {}'.format(queue.name, capacity, balk_label)
        super().__init__(mod, queue)


class TallyBlock(Block):
    def __init__(self, tally, value, num_obs=""):
        mod = 'TALLY: {}, {}, {}'.format(tally.name, value, num_obs)
        super().__init__(mod, tally)


class SeizeBlock(Block):
    def __init__(self, resource, priority="", num_units=1):
        mod = 'SEIZE, {}: {}, {}'.format(priority, resource.name, num_units)
        super().__init__(mod, resource)

    # For Repeats
    def add(self, resource_id="", num_units=""):
        add_list = [resource_id, num_units]
        super().add(add_list)


class DelayBlock(Block):
    def __init__(self, duration="", storage_id=""):
        mod = 'DELAY: {}, {}'.format(duration, storage_id)
        super().__init__(mod)


class ReleaseBlock(Block):
    def __init__(self, resource, quantity_to_release=1):
        mod = 'RELEASE: {}, {}'.format(resource.name, quantity_to_release)
        super().__init__(mod, resource)

    # For Repeats
    def add(self, resource_id="", quantity_to_release=""):
        add_list = [resource_id, quantity_to_release]
        super().add(add_list)


class CountBlock(Block):
    def __init__(self, counter, counter_increment=""):
        mod = 'COUNT: {}, {}'.format(counter.name, counter_increment)
        super().__init__(mod, counter)


class BranchBlock(Block):
    def __init__(self, branch_type, destination_label, max_branches="", rand_num_stream="", condition=""):
        if branch_type.lower() in ["else", "always"]:
            mod = 'Branch, {}, {}: {}, {}'.format(max_branches, rand_num_stream, branch_type, destination_label)
        else:
            mod = 'Branch, {}, {}: {}, {}, {}'.format(max_branches, rand_num_stream, branch_type, condition,
                                                      destination_label)
        super().__init__(mod)

    # For Repeats
    def add(self, branch_type, destination_label, condition=""):
        if branch_type.lower() in ["else", "always"]:
            add_list = [branch_type, destination_label]
        else:
            add_list = [branch_type, condition, destination_label]
        super().add(add_list)


# todo: determine how this affects the .exp. Does another var/attr need to be added?
# todo: Should name string be passed or the element object?
class AssignBlock(Block):
    """Name can be a SIMAN variable or attribute.
    Used for modifying an existing variable or attribute element"""
    def __init__(self, var_or_attr, value):
        assert isinstance(var_or_attr, (Attribute, Variable))
        mod = 'ASSIGN: {} = {}'.format(var_or_attr.name, value)
        super().__init__(mod, var_or_attr)

    # For Repeats
    def add(self, name, value):
        add_list = [name, value]
        super().add(add_list)


class StationBlock(Block):
    def __init__(self, begin_station_id, end_station_id):
        mod = 'STATION, {}, {}'.format(begin_station_id, end_station_id)
        super().__init__(mod)


class RouteBlock(Block):
    def __init__(self, duration, destination):
        mod = 'ROUTE: {}, {}'.format(duration, destination)
        super().__init__(mod)


class RequestBlock(Block):
    def __init__(self, priority, storage_id, alt_path, transporter_unit, velocity, entity_location):
        mod = 'REQUEST, {}, {}, {}: {}, {}, {}'.format(priority, storage_id, alt_path, transporter_unit, velocity, entity_location)
        super().__init__(mod)


class TransportBlock(Block):
    def __init__(self, alt_path, transporter_unit, destination, velocity, guided_trans_dest):
        mod = 'TRANSPORT, {}, {}: {}, {}, {}, {}'.format(alt_path, transporter_unit, destination, velocity, guided_trans_dest)
        super().__init__(mod)


class FreeBlock(Block):
    def __init__(self, transporter_unit):
        mod = 'FREE: {}'.format(transporter_unit)
        super().__init__(mod)


class AllocateBlock(Block):
    def __init__(self, priority, alt_path, transport_unit, entity_location):
        mod = 'ALLOCATE: {}, {}: {}, {}'.format(priority, alt_path, transport_unit, entity_location)
        super().__init__(mod)


class MoveBlock(Block):
    def __init__(self, storage_id, alt_path, transport_unit, destination, velocity):
        mod = 'MOVE, {}, {}: {}, {}, {}'.format(storage_id, alt_path, transport_unit, destination, velocity)
        super().__init__(mod)


class HalthBlock(Block):
    def __init__(self, transport_unit):
        mod = 'HALT: {}'.format(transport_unit)
        super().__init__(mod)


class DisposeBlock(Block):
    def __init__(self):
        mod = "DISPOSE"
        super().__init__(mod)


class SuperBlock:
    """Create group of sequential blocks with reference id"""
    def __init__(self, name, blocks):
        if not isinstance(blocks, (list, tuple)):
            raise TypeError('argument must be list or tuple')
        if len(blocks) == 0:
            raise ValueError("empty list")

        self.name = name
        self.type = "mod"
        self.blocks = blocks

    def __str__(self):
        string1 = str(self.name) + '\t' + str(self.blocks[0])
        str_blocks = [string1] + [" "*len(self.name) + '\t' + str(b) for b in self.blocks[1:]]
        return '\n'.join(str_blocks) + '\n'