from elements import Queue
# todo: fix add for seize and release to handle repeats
# TODO: Add param class that simply returns discrete list of params for a given block/elem. Example: param.branchtype.if


class Block:
    def __init__(self, mod, element=None):
        self._mod = mod
        self.type = 'mod'
        self.element = element
        self._next = None

    def __str__(self):
        if self._next:
            return self._mod + ": %s;" % self._next.name
        else:
            return self._mod + ";"

    # Directly link successor block
    def set_next(self, obj):
        self._next = obj

    # For Repeats
    # todo: better formatting for repeats. Dynamic padding.
    def add(self, add_list):
        self._mod += ":\n\t\t%s, %s, %s" % tuple(str(x) for x in add_list)


# todo: determine if element_ids should be passed to block as string or an object
class CreateBlock(Block):
    def __init__(self, entity, batch_size="", offset_time="", interval="", maximum_batches=""):
        mod = "CREATE, %s, %s, %s: %s, %s" % (str(batch_size), str(offset_time), str(entity.name), str(interval), str(maximum_batches))
        super().__init__(mod, entity)


class QueueBlock(Block):
    def __init__(self, queue, capacity="", balk_label=""):
        assert isinstance(queue, Queue)
        mod = "QUEUE, %s, %s, %s" % (str(queue.name), str(capacity), str(balk_label))
        super().__init__(mod, queue)


class SeizeBlock(Block):
    def __init__(self, resource, priority="", num_units=""):
        mod = "SEIZE, %s: %s, %s" % (str(priority), str(resource.name), str(num_units))
        super().__init__(mod, resource)

    # For Repeats
    def add(self, resource_id="", num_units=""):
        add_list = [resource_id, num_units]
        super().add(add_list)


class DelayBlock(Block):
    def __init__(self, duration="", storage_id=""):
        mod = "DELAY: %s, %s" % (str(duration), str(storage_id))
        super().__init__(mod)


class ReleaseBlock(Block):
    def __init__(self, resource, quantity_to_release=""):
        mod = "RELEASE: %s, %s" % (str(resource.name), str(quantity_to_release))
        super().__init__(mod, resource)

    # For Repeats
    def add(self, resource_id="", quantity_to_release=""):
        add_list = [resource_id, quantity_to_release]
        super().add(add_list)


class CountBlock(Block):
    def __init__(self, counter, counter_increment=""):
        mod = "COUNT: %s, %s" % (str(counter.name), str(counter_increment))
        super().__init__(mod, counter)


class BranchBlock(Block):
    def __init__(self, branch_type, destination_label, max_branches="", rand_num_stream="", condition=""):
        mod = "Branch, %s, %s: %s, %s, %s" % (str(max_branches), str(rand_num_stream), str(branch_type), str(condition), str(destination_label))
        super().__init__(mod)

    # For Repeats
    def add(self, branch_type, destination_label, condition=""):
        add_list = [branch_type, condition, destination_label]
        super().add(add_list)


# todo: determine how this affects the .exp. Does another var/attr need to be added?
# todo: Should name string be passed or the element object?
class Assign(Block):
    """Name can be a SIMAN variable or attribute.
    Used for modifying an existing variable or attribute element"""
    def __init__(self, name, value):
        attributes = (name, value)
        mod = 'ASSIGN: {} = {}'.format(attributes)
        super().__init__(mod)

    # For Repeats
    def add(self, name, value):
        add_list = [name, value]
        super().add(add_list)


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