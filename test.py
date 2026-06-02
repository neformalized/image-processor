from logic import Logic

processor = Logic()

result, usage = processor.work("https://play-lh.googleusercontent.com/EQf5FLgn72S85Z9bxYUuKNj4T59x_Nlhnniwzvc8-3mRD-iek1BSXX7MFi5U7bqMZe9B=w526-h296-rw")

print(result)

_usage = {}
for u in usage:
    
    if u[0] not in _usage.keys(): _usage[u[0]] = {"input": 0, "output": 0}
    
    _usage[u[0]]["input"] += int(u[1])
    _usage[u[0]]["output"] += int(u[2])
#

print(_usage)