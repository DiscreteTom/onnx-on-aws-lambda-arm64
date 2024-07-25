# ONNX on AWS Lambda ARM64

This is a demo to show how to run [ONNX Runtime](https://onnxruntime.ai/docs/get-started/with-python.html) on AWS Lambda for arm64 runtimes.

## How This Works

ONNX Runtime works fine on x86 lambda, but on arm64 lambda you will get the following error:

```
Error in cpuinfo: failed to parse the list of possible processors in /sys/devices/system/cpu/possible
Error in cpuinfo: failed to parse the list of present processors in /sys/devices/system/cpu/present
Error in cpuinfo: failed to parse both lists of possible and present processors
terminate called after throwing an instance of 'onnxruntime::OnnxRuntimeException'
```

That's because AWS Lambda remove these files for the simplicity of runtimes.

In Zip mode, you can't modify files in `/sys`, but in Container mode you can. This demo will copy [`patch.txt`](./hello_world/patch.txt) to `/sys/devices/system/cpu/possible` and `/sys/devices/system/cpu/present` to fix the issue.

> [!IMPORTANT]
> You should modify the content of [`patch.txt`](./hello_world/patch.txt) corresponding to your Lambda function's memory configuration. The content should be `0-X` where `X` is the cpu count of the Lambda function ***minus 1***. You can use `os.cpu_count()` in python to checkout how many vCPU is allocated for your memory configuration. E.g. when memory is 128MB there is 2 vCPU and the content should be `0-1`; when memory is 10240MB there is 6 vCPU and the content should be `0-5`.

> Why can't you generate `/sys/devices/system/cpu/possible` and `/sys/devices/system/cpu/present` during the runtime to write the correct vCPU? That's because in Lambda only `/tmp` is writable. Thus you have to finish the patch process before the Lambda is invoked.

This demo uses [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) as the development framework.

## Build

Docker is required.

```bash
sam build -u
```

## Deploy

```bash
sam deploy -g
```

## Remote Test

```bash
sam remote invoke HelloWorldFunction --region us-east-1
```

You can also test your function in the AWS management console.

## Clean

```bash
sam delete --stack-name python-onnx
```