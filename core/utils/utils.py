

def batch_generator(iterable, batch_size=1000):
    """ Разложить итерируемый объект на части """
    batch = []
    for item in iterable:
        if len(batch) == batch_size:
            yield batch
            batch = []
        batch.append(item)
    if len(batch):
        yield batch

