from perx.config import settings

queue = []
processed = [None for _ in range(settings.workers_num)]
results = []
