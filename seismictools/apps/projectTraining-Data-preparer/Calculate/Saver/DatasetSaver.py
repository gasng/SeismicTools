import numpy as np
import json

def save_dataset(traces, output_path):
    dataset = [trace.to_dict() for trace in traces]
    np.save(output_path, np.array(dataset, dtype=object))
    print(f"Выборка сохранена: {output_path}")

def load_dataset(filepath):
    loaded = np.load(filepath, allow_pickle=True)
    traces = []
    for item in loaded:
        traces.append(TraceData.from_dict(item))
    return traces