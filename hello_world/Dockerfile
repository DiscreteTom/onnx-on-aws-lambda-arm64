FROM public.ecr.aws/lambda/python:3.12

COPY *.py requirements.txt ./
COPY *.onnx ./

RUN python3.12 -m pip install -r requirements.txt -t .

COPY patch.txt /sys/devices/system/cpu/possible
COPY patch.txt /sys/devices/system/cpu/present

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
