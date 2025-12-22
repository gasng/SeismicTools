import numpy as np

class TraceData:
    def __init__(self, trace_id, coordinates, data, class_label=None):
        self.trace_id = trace_id
        self.coordinates = coordinates  # (inline, xline)
        self.data = np.array(data)
        self.class_label = class_label

    def set_class(self, label):
        self.class_label = label

    def to_dict(self):
        return {
            'trace_id': self.trace_id,
            'coordinates': self.coordinates,
            'data': self.data.tolist(),
            'class_label': self.class_label
        }

    @staticmethod
    def from_dict(data_dict):
        trace = TraceData(
            trace_id=data_dict['trace_id'],
            coordinates=tuple(data_dict['coordinates']),
            data=data_dict['data'],
            class_label=data_dict['class_label']
        )
        return trace