
def lambda_handler(event, _):
    import onnxruntime as ort
    import numpy as np

    session = ort.InferenceSession('coat_tiny_Opset18.onnx')
    print(session.get_providers())
