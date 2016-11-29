def select(setExpr, resource_rule="CYC", attribute_id=""):
    return 'SELECT({}, {}, {})'.format(setExpr, resource_rule, attribute_id)


def int(attribute):
    return 'INT({})'.format(attribute)


def disc(values, cumsum=None):
    if not cumsum:
        p = 1/len(values)
        cumsum = [p*c for c in range(1, len(values)+1)]
    strings = ['{}, {}'.format(cumsum[i], val) for i, val in enumerate(values)]
    return 'DISC({})'.format(', '.join(strings))


def cont(values, cumsum=None):
    if not cumsum:
        p = 1/len(values)
        cumsum = [p*c for c in range(1, len(values)+1)]
    strings = ['{}, {}'.format(cumsum[i], val) for i, val in enumerate(values)]
    return 'CONT({})'.format(', '.join(strings))


def nq(queue_id):
    """
    Returns number of items currently in the queue
    """
    return 'NQ({})'.format(queue_id)

def nr(resource_id):
    """
    Returns number of resources currently being used
    """
    return 'NR({})'.format(resource_id)


def resUtil(resource_id):
    """
    Return resource utilization time
    """
    return 'ResUtil({})'.format(resource_id)

# set functions
def numMem(set_name):
    """
    returns the number of members in SetName
    """
    return 'NumMem({})'.format(set_name)


def member(set_name, index):
    """
    returns the element number of the member in SetName at position Index
    """
    return 'Member({}, {})'.format(set_name, index)


def memIdx(set_name, member_name):
    """
    returns the index of MemberName located in SetName
    """
    return 'MemIdx({}, {})'.format(set_name, member_name)


class SelectionRule:
    """
    Can be used with SELECT, PICKQ, QPICK
    """
    def __init__(self):
        self.cyc = "CYC"  # CYClic priority
        self.ran = "RAN"  # RANdom priority
        self.por = "POR"  # Preferred Order Rule
        self.lnb = "LNB"  # Largest Number Busy
        self.snb = "SNB"  # Smallest Number Busy
        self.lrc = "LRC"  # Largest Remaining Capacity
        self.src = "SRC"  # Smallest Remaining capacity


class ReleaseRule:
    """
    Used with RELEASE block and SETS
    """
    def __init__(self):
        self.last = "LAST"  # Last Member Seized
        self.first = "FIRST"  # First Member Seized
