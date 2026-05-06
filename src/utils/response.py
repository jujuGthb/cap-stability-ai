from sdks.novavision.src.helper.package import PackageHelper
from capsules.StabilityAI.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    OutputImage,
    TextToImage,
    TextToImageResponse,
    TextToImageOutputs,
    ImageToImage,
    ImageToImageResponse,
    ImageToImageOutputs,
    Inpainting,
    InpaintingResponse,
    InpaintingOutputs,
    Outpainting,
    OutpaintingResponse,
    OutpaintingOutputs,
)


def build_response_text_to_image(context):
    output = OutputImage(value=context.image)
    outputs = TextToImageOutputs(outputImage=output)
    response = TextToImageResponse(outputs=outputs)
    executor = TextToImage(value=response)
    configExecutor = ConfigExecutor(value=executor)
    packageConfigs = PackageConfigs(executor=configExecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    return package.build_model(context)


def build_response_image_to_image(context):
    output = OutputImage(value=context.image)
    outputs = ImageToImageOutputs(outputImage=output)
    response = ImageToImageResponse(outputs=outputs)
    executor = ImageToImage(value=response)
    configExecutor = ConfigExecutor(value=executor)
    packageConfigs = PackageConfigs(executor=configExecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    return package.build_model(context)


def build_response_inpainting(context):
    output = OutputImage(value=context.image)
    outputs = InpaintingOutputs(outputImage=output)
    response = InpaintingResponse(outputs=outputs)
    executor = Inpainting(value=response)
    configExecutor = ConfigExecutor(value=executor)
    packageConfigs = PackageConfigs(executor=configExecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    return package.build_model(context)


def build_response_outpainting(context):
    output = OutputImage(value=context.image)
    outputs = OutpaintingOutputs(outputImage=output)
    response = OutpaintingResponse(outputs=outputs)
    executor = Outpainting(value=response)
    configExecutor = ConfigExecutor(value=executor)
    packageConfigs = PackageConfigs(executor=configExecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    return package.build_model(context)