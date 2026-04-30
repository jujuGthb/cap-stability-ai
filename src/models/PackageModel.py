from pydantic import validator, Field
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Outputs, Configs, Response, Request, Output, Input, Config
)


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Image"


class SegmentationMask(Input):
    name: Literal["segmentationMask"] = "segmentationMask"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Segmentation Mask"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Output Image"


class InputPrompt(Config):
    """
    Describe what you want to see in the generated image.
    Be as descriptive as possible for better results.
    """
    name: Literal["inputPrompt"] = "inputPrompt"
    value: str = ""
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Prompt"
        json_schema_extra = {"shortDescription": "What you want to see"}


class NegativePrompt(Config):
    """
    Describe what you do NOT want to see in the generated image.
    Example: 'blurry, low quality, distorted, watermark'
    Leave empty if not needed.
    """
    name: Literal["negativePrompt"] = "negativePrompt"
    value: str = ""
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Negative Prompt"
        json_schema_extra = {"shortDescription": "What you don't want to see"}


class InputApiKey(Config):
    """
    Enter your Stability AI API key.
    You can get one at https://platform.stability.ai/account/keys
    """
    name: Literal["inputApiKey"] = "inputApiKey"
    value: str = ""
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "API Key"
        json_schema_extra = {"shortDescription": "Stability AI API Key"}


class Seed(Config):
    """
    Optional seed for reproducible generation results.
    Must be between 0 and 4294967294. Leave at 0 to use a random seed.
    """
    name: Literal["seed"] = "seed"
    value: int
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Seed"
        json_schema_extra = {"shortDescription": "0 = random seed"}


class ModelCore(Config):
    """
    Balanced speed and quality. Recommended for most use cases.
    """
    name: Literal["core"] = "core"
    value: Literal["core"] = "core"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Core"


class ModelUltra(Config):
    """
    Highest quality output. Slower than Core.
    Best for final renders and high-resolution outputs.
    """
    name: Literal["ultra"] = "ultra"
    value: Literal["ultra"] = "ultra"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Ultra"


class ModelSD3(Config):
    """
    Stable Diffusion 3. More artistic and creative style.
    Best for illustrations and stylized outputs.
    """
    name: Literal["sd3"] = "sd3"
    value: Literal["sd3"] = "sd3"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "SD3"


class InputModel(Config):
    name: Literal["inputModel"] = "inputModel"
    value: Union[ModelCore, ModelUltra, ModelSD3]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Model"
        json_schema_extra = {"shortDescription": "Generation Model"}


class Strength(Config):
    """
    Controls how much the input image influences the generated output.
    Range: 0.0 to 1.0.
    - 0.0: output is nearly identical to the input image.
    - 1.0: input image is completely ignored, generation is from prompt only.
    """
    name: Literal["strength"] = "strength"
    value: float
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Strength"
        json_schema_extra = {"shortDescription": "Image Influence (0.0 - 1.0)"}


class Preset3dModel(Config):
    name: Literal["3d-model"] = "3d-model"
    value: Literal["3d-model"] = "3d-model"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "3D Model"


class PresetAnalogFilm(Config):
    name: Literal["analog-film"] = "analog-film"
    value: Literal["analog-film"] = "analog-film"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Analog Film"


class PresetAnime(Config):
    name: Literal["anime"] = "anime"
    value: Literal["anime"] = "anime"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Anime"


class PresetCinematic(Config):
    name: Literal["cinematic"] = "cinematic"
    value: Literal["cinematic"] = "cinematic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Cinematic"


class PresetComicBook(Config):
    name: Literal["comic-book"] = "comic-book"
    value: Literal["comic-book"] = "comic-book"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Comic Book"


class PresetDigitalArt(Config):
    name: Literal["digital-art"] = "digital-art"
    value: Literal["digital-art"] = "digital-art"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Digital Art"


class PresetEnhance(Config):
    name: Literal["enhance"] = "enhance"
    value: Literal["enhance"] = "enhance"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Enhance"


class PresetFantasyArt(Config):
    name: Literal["fantasy-art"] = "fantasy-art"
    value: Literal["fantasy-art"] = "fantasy-art"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Fantasy Art"


class PresetIsometric(Config):
    name: Literal["isometric"] = "isometric"
    value: Literal["isometric"] = "isometric"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Isometric"


class PresetLineArt(Config):
    name: Literal["line-art"] = "line-art"
    value: Literal["line-art"] = "line-art"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Line Art"


class PresetLowPoly(Config):
    name: Literal["low-poly"] = "low-poly"
    value: Literal["low-poly"] = "low-poly"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Low Poly"


class PresetModelingCompound(Config):
    name: Literal["modeling-compound"] = "modeling-compound"
    value: Literal["modeling-compound"] = "modeling-compound"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Modeling Compound"


class PresetNeonPunk(Config):
    name: Literal["neon-punk"] = "neon-punk"
    value: Literal["neon-punk"] = "neon-punk"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Neon Punk"


class PresetOrigami(Config):
    name: Literal["origami"] = "origami"
    value: Literal["origami"] = "origami"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Origami"


class PresetPhotographic(Config):
    name: Literal["photographic"] = "photographic"
    value: Literal["photographic"] = "photographic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Photographic"


class PresetPixelArt(Config):
    name: Literal["pixel-art"] = "pixel-art"
    value: Literal["pixel-art"] = "pixel-art"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Pixel Art"


class PresetTileTexture(Config):
    name: Literal["tile-texture"] = "tile-texture"
    value: Literal["tile-texture"] = "tile-texture"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Tile Texture"


class InputPresetDisabled(Config):
    name: Literal["disabled"] = "disabled"
    value: Literal["disabled"] = "disabled"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Disabled"


class InputPresetEnabled(Config):
    name: Literal["enabled"] = "enabled"
    value: Union[
        Preset3dModel, PresetAnalogFilm, PresetAnime, PresetCinematic,
        PresetComicBook, PresetDigitalArt, PresetEnhance, PresetFantasyArt,
        PresetIsometric, PresetLineArt, PresetLowPoly, PresetModelingCompound,
        PresetNeonPunk, PresetOrigami, PresetPhotographic, PresetPixelArt,
        PresetTileTexture
    ]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Enabled"


class InputPreset(Config):
    name: Literal["inputPreset"] = "inputPreset"
    value: Union[InputPresetDisabled, InputPresetEnabled]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Style Preset"
        json_schema_extra = {"shortDescription": "Optional style preset"}


class InvertMaskDisabled(Config):
    name: Literal["disabled"] = "disabled"
    value: Literal["disabled"] = "disabled"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Disabled"


class InvertMaskEnabled(Config):
    name: Literal["enabled"] = "enabled"
    value: Literal["enabled"] = "enabled"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Enabled"


class InvertMask(Config):
    """
    When enabled, inverts the segmentation mask so the background
    is inpainted instead of the detected foreground object.
    """
    name: Literal["invertSegmentationMask"] = "invertSegmentationMask"
    value: Union[InvertMaskDisabled, InvertMaskEnabled]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Invert Mask"
        json_schema_extra = {"shortDescription": "Inpaint background instead of foreground"}


class PromptDisabled(Config):
    name: Literal["disabled"] = "disabled"
    value: Literal["disabled"] = "disabled"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Disabled"


class PromptEnabled(Config):
    """
    Optional prompt to guide the outpainting generation.
    Describes what you want to see in the outpainted regions.
    """
    name: Literal["enabled"] = "enabled"
    value: str = ""
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Enabled"


class OutpaintingPrompt(Config):
    name: Literal["outpaintingPrompt"] = "outpaintingPrompt"
    value: Union[PromptDisabled, PromptEnabled]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Prompt"
        json_schema_extra = {"shortDescription": "Optional generation prompt"}


class Creativity(Config):
    """
    Controls how creative the outpainting is.
    Range: 0.0 to 1.0.
    - 0.0: conservative, stays close to the original image style.
    - 1.0: highly creative, generates more imaginative content.
    """
    name: Literal["creativity"] = "creativity"
    value: float
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Creativity"
        json_schema_extra = {"shortDescription": "Outpainting creativity (0.0 - 1.0)"}


class PaddingLeft(Config):
    """
    Number of pixels to outpaint on the left side of the image.
    Maximum value is 2000. Set to 0 to skip this direction.
    """
    name: Literal["paddingLeft"] = "paddingLeft"
    value: int
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Left"
        json_schema_extra = {"shortDescription": "Pixels to expand left (max 2000)"}


class PaddingRight(Config):
    """
    Number of pixels to outpaint on the right side of the image.
    Maximum value is 2000. Set to 0 to skip this direction.
    """
    name: Literal["paddingRight"] = "paddingRight"
    value: int
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Right"
        json_schema_extra = {"shortDescription": "Pixels to expand right (max 2000)"}


class PaddingUp(Config):
    """
    Number of pixels to outpaint on the top side of the image.
    Maximum value is 2000. Set to 0 to skip this direction.
    """
    name: Literal["paddingUp"] = "paddingUp"
    value: int
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Up"
        json_schema_extra = {"shortDescription": "Pixels to expand upward (max 2000)"}


class PaddingDown(Config):
    """
    Number of pixels to outpaint on the bottom side of the image.
    Maximum value is 2000. Set to 0 to skip this direction.
    """
    name: Literal["paddingDown"] = "paddingDown"
    value: int
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Down"
        json_schema_extra = {"shortDescription": "Pixels to expand downward (max 2000)"}


class TextToImageConfigs(Configs):
    inputPrompt: InputPrompt
    negativePrompt: NegativePrompt
    inputModel: InputModel
    inputApiKey: InputApiKey


class TextToImageOutputs(Outputs):
    outputImage: OutputImage


class TextToImageRequest(Request):
    configs: TextToImageConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class TextToImageResponse(Response):
    outputs: TextToImageOutputs


class TextToImageExecutor(Config):
    name: Literal["TextToImageExecutor"] = "TextToImageExecutor"
    value: Union[TextToImageRequest, TextToImageResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Text to Image"
        json_schema_extra = {"target": {"value": 0}}


class ImageToImageConfigs(Configs):
    inputPrompt: InputPrompt
    negativePrompt: NegativePrompt
    strength: Strength
    inputModel: InputModel
    inputApiKey: InputApiKey


class ImageToImageInputs(Inputs):
    inputImage: InputImage


class ImageToImageOutputs(Outputs):
    outputImage: OutputImage


class ImageToImageRequest(Request):
    inputs: Optional[ImageToImageInputs]
    configs: ImageToImageConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class ImageToImageResponse(Response):
    outputs: ImageToImageOutputs


class ImageToImageExecutor(Config):
    name: Literal["ImageToImageExecutor"] = "ImageToImageExecutor"
    value: Union[ImageToImageRequest, ImageToImageResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Image to Image"
        json_schema_extra = {"target": {"value": 0}}


class InpaintingConfigs(Configs):
    inputPrompt: InputPrompt
    negativePrompt: NegativePrompt
    inputPreset: InputPreset
    invertSegmentationMask: InvertMask
    seed: Seed
    inputApiKey: InputApiKey


class InpaintingInputs(Inputs):
    inputImage: InputImage
    segmentationMask: SegmentationMask


class InpaintingOutputs(Outputs):
    outputImage: OutputImage


class InpaintingRequest(Request):
    inputs: Optional[InpaintingInputs]
    configs: InpaintingConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class InpaintingResponse(Response):
    outputs: InpaintingOutputs


class InpaintingExecutor(Config):
    name: Literal["InpaintingExecutor"] = "InpaintingExecutor"
    value: Union[InpaintingRequest, InpaintingResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Inpainting"
        json_schema_extra = {"target": {"value": 0}}


class OutpaintingConfigs(Configs):
    outpaintingPrompt: OutpaintingPrompt
    creativity: Creativity
    paddingLeft: PaddingLeft
    paddingRight: PaddingRight
    paddingUp: PaddingUp
    paddingDown: PaddingDown
    inputPreset: InputPreset
    seed: Seed
    inputApiKey: InputApiKey


class OutpaintingInputs(Inputs):
    inputImage: InputImage


class OutpaintingOutputs(Outputs):
    outputImage: OutputImage


class OutpaintingRequest(Request):
    inputs: Optional[OutpaintingInputs]
    configs: OutpaintingConfigs

    class Config:
        json_schema_extra = {"target": "configs"}


class OutpaintingResponse(Response):
    outputs: OutpaintingOutputs


class OutpaintingExecutor(Config):
    name: Literal["OutpaintingExecutor"] = "OutpaintingExecutor"
    value: Union[OutpaintingRequest, OutpaintingResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Outpainting"
        json_schema_extra = {"target": {"value": 0}}


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[TextToImageExecutor, ImageToImageExecutor, InpaintingExecutor, OutpaintingExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {"shortDescription": "Generation Mode"}


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    name: Literal["StabilityAI"] = "StabilityAI"
    configs: PackageConfigs
    type: Literal["capsule"] = "capsule"