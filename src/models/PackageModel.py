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


class ModelCore(Config):
    """Balanced speed and quality. Recommended for most use cases."""
    name: Literal["core"] = "core"
    value: Literal["core"] = "core"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Core"
        json_schema_extra = {"shortDescription": "Balanced speed and quality"}


class ModelUltra(Config):
    """Highest quality output. Slower than Core. Best for final renders and high-resolution outputs."""
    name: Literal["ultra"] = "ultra"
    value: Literal["ultra"] = "ultra"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Ultra"
        json_schema_extra = {"shortDescription": "Highest quality output"}


class ModelSD3(Config):
    """Stable Diffusion 3. More artistic and creative style. Best for illustrations and stylized outputs."""
    name: Literal["sd3"] = "sd3"
    value: Literal["sd3"] = "sd3"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "SD3"
        json_schema_extra = {"shortDescription": "Artistic and creative style"}


class InputModel(Config):
    """
    Select the Stability AI generation model.
    Core is recommended for most use cases. Ultra gives the highest quality but is slower.
    SD3 is best for artistic and illustrated outputs.
    """
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
    """Renders output with a 3D model aesthetic."""
    name: Literal["3d-model"] = "3d-model"
    value: Literal["3d-model"] = "3d-model"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "3D Model"
        json_schema_extra = {"shortDescription": "3D rendered aesthetic"}


class PresetAnalogFilm(Config):
    """Film grain and warm tones reminiscent of analog photography."""
    name: Literal["analog-film"] = "analog-film"
    value: Literal["analog-film"] = "analog-film"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Analog Film"
        json_schema_extra = {"shortDescription": "Film grain and warm tones"}


class PresetAnime(Config):
    """Japanese animation style with clean lines and vivid colors."""
    name: Literal["anime"] = "anime"
    value: Literal["anime"] = "anime"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Anime"
        json_schema_extra = {"shortDescription": "Japanese animation style"}


class PresetCinematic(Config):
    """Dramatic film-like lighting and composition."""
    name: Literal["cinematic"] = "cinematic"
    value: Literal["cinematic"] = "cinematic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Cinematic"
        json_schema_extra = {"shortDescription": "Dramatic film-like lighting"}


class PresetComicBook(Config):
    """Bold lines and flat colors typical of comic book illustration."""
    name: Literal["comic-book"] = "comic-book"
    value: Literal["comic-book"] = "comic-book"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Comic Book"
        json_schema_extra = {"shortDescription": "Bold lines and flat colors"}


class PresetDigitalArt(Config):
    """Clean, vibrant digital illustration style."""
    name: Literal["digital-art"] = "digital-art"
    value: Literal["digital-art"] = "digital-art"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Digital Art"
        json_schema_extra = {"shortDescription": "Clean digital illustration"}


class PresetEnhance(Config):
    """Enhances details and overall sharpness of the output."""
    name: Literal["enhance"] = "enhance"
    value: Literal["enhance"] = "enhance"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Enhance"
        json_schema_extra = {"shortDescription": "Enhance detail and sharpness"}


class PresetFantasyArt(Config):
    """Magical and fantastical illustration style."""
    name: Literal["fantasy-art"] = "fantasy-art"
    value: Literal["fantasy-art"] = "fantasy-art"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Fantasy Art"
        json_schema_extra = {"shortDescription": "Magical fantasy illustration"}


class PresetIsometric(Config):
    """Isometric perspective rendering with a game-like aesthetic."""
    name: Literal["isometric"] = "isometric"
    value: Literal["isometric"] = "isometric"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Isometric"
        json_schema_extra = {"shortDescription": "Isometric game-like perspective"}


class PresetLineArt(Config):
    """Clean line drawing style with minimal shading."""
    name: Literal["line-art"] = "line-art"
    value: Literal["line-art"] = "line-art"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Line Art"
        json_schema_extra = {"shortDescription": "Clean line drawing style"}


class PresetLowPoly(Config):
    """Geometric low-polygon art style."""
    name: Literal["low-poly"] = "low-poly"
    value: Literal["low-poly"] = "low-poly"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Low Poly"
        json_schema_extra = {"shortDescription": "Geometric low-polygon style"}


class PresetModelingCompound(Config):
    """Clay-like sculpted aesthetic resembling modeling compound."""
    name: Literal["modeling-compound"] = "modeling-compound"
    value: Literal["modeling-compound"] = "modeling-compound"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Modeling Compound"
        json_schema_extra = {"shortDescription": "Clay-like sculpted aesthetic"}


class PresetNeonPunk(Config):
    """Vibrant neon colors with cyberpunk aesthetics."""
    name: Literal["neon-punk"] = "neon-punk"
    value: Literal["neon-punk"] = "neon-punk"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Neon Punk"
        json_schema_extra = {"shortDescription": "Vibrant neon cyberpunk style"}


class PresetOrigami(Config):
    """Paper folding art style inspired by origami."""
    name: Literal["origami"] = "origami"
    value: Literal["origami"] = "origami"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Origami"
        json_schema_extra = {"shortDescription": "Paper folding art style"}


class PresetPhotographic(Config):
    """Realistic photographic rendering with natural lighting."""
    name: Literal["photographic"] = "photographic"
    value: Literal["photographic"] = "photographic"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Photographic"
        json_schema_extra = {"shortDescription": "Realistic photographic rendering"}


class PresetPixelArt(Config):
    """Retro pixel art style with visible pixels."""
    name: Literal["pixel-art"] = "pixel-art"
    value: Literal["pixel-art"] = "pixel-art"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Pixel Art"
        json_schema_extra = {"shortDescription": "Retro pixel art style"}


class PresetTileTexture(Config):
    """Seamlessly tileable texture pattern."""
    name: Literal["tile-texture"] = "tile-texture"
    value: Literal["tile-texture"] = "tile-texture"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Tile Texture"
        json_schema_extra = {"shortDescription": "Seamlessly tileable texture"}


class InputPresetDisabled(Config):
    """No style preset applied. The model uses its default generation style."""
    name: Literal["presetDisabled"] = "presetDisabled"
    value: Literal["presetDisabled"] = "presetDisabled"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Disabled"
        json_schema_extra = {"shortDescription": "Default generation style"}


class InputPresetEnabled(Config):
    """Apply one of the available style presets to guide the artistic output."""
    name: Literal["presetEnabled"] = "presetEnabled"
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
        json_schema_extra = {"shortDescription": "Apply a style preset"}


class InputPreset(Config):
    """
    Optional style preset to guide the artistic style of the generated content.
    When Enabled, select from 17 available presets such as photographic, cinematic, anime, and more.
    Leave Disabled for default generation style.
    """
    name: Literal["inputPreset"] = "inputPreset"
    value: Union[InputPresetDisabled, InputPresetEnabled]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Style Preset"
        json_schema_extra = {"shortDescription": "Optional style preset"}


class SeedDisabled(Config):
    """Use a random seed for each generation. Results will vary on each run."""
    name: Literal["seedDisabled"] = "seedDisabled"
    value: Literal["seedDisabled"] = "seedDisabled"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Disabled"
        json_schema_extra = {"shortDescription": "Random seed each run"}


class SeedEnabled(Config):
    """
    Use a fixed integer seed for reproducible generation.
    Enter a number between 0 and 4294967294.
    """
    name: Literal["seedEnabled"] = "seedEnabled"
    value: int
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Enabled"
        json_schema_extra = {"shortDescription": "Fixed seed for reproducible results"}


class Seed(Config):
    """
    Optional seed for reproducible generation results.
    When Enabled, enter a number between 0 and 4294967294.
    Using the same seed with the same prompt will produce identical outputs.
    Leave Disabled to use a random seed.
    """
    name: Literal["seed"] = "seed"
    value: Union[SeedDisabled, SeedEnabled]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Seed"
        json_schema_extra = {"shortDescription": "Optional seed for reproducible results"}


class InvertMaskDisabled(Config):
    """Inpaint the detected foreground object using the segmentation mask."""
    name: Literal["invertDisabled"] = "invertDisabled"
    value: Literal["invertDisabled"] = "invertDisabled"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Disabled"
        json_schema_extra = {"shortDescription": "Inpaint foreground object"}


class InvertMaskEnabled(Config):
    """Invert the segmentation mask to inpaint the background instead of the foreground."""
    name: Literal["invertEnabled"] = "invertEnabled"
    value: Literal["invertEnabled"] = "invertEnabled"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Enabled"
        json_schema_extra = {"shortDescription": "Inpaint background instead"}


class InvertMask(Config):
    """
    When Enabled, inverts the segmentation mask so the background
    is inpainted instead of the detected foreground object.
    Leave Disabled to inpaint the detected foreground object.
    """
    name: Literal["invertSegmentationMask"] = "invertSegmentationMask"
    value: Union[InvertMaskDisabled, InvertMaskEnabled]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Invert Mask"
        json_schema_extra = {"shortDescription": "Inpaint background instead of foreground"}


class PromptDisabled(Config):
    """No prompt provided. The model decides what to generate based on the original image context."""
    name: Literal["promptDisabled"] = "promptDisabled"
    value: Literal["promptDisabled"] = "promptDisabled"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Disabled"
        json_schema_extra = {"shortDescription": "Model decides based on context"}


class PromptEnabled(Config):
    """Provide a text prompt to guide what appears in the outpainted regions."""
    name: Literal["promptEnabled"] = "promptEnabled"
    value: str = ""
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Enabled"
        json_schema_extra = {"shortDescription": "Describe the expanded area"}


class OutpaintingPrompt(Config):
    """
    Optional text prompt to guide what appears in the outpainted regions.
    When Enabled, describe what you want to see in the expanded areas.
    Leave Disabled to let the model decide based on the original image context.
    """
    name: Literal["outpaintingPrompt"] = "outpaintingPrompt"
    value: Union[PromptDisabled, PromptEnabled]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Prompt"
        json_schema_extra = {"shortDescription": "Optional generation prompt"}


class Creativity(Config):
    """
    Controls how creative the outpainting is. Range: 0.0 to 1.0.
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
    """Number of pixels to expand on the left side. Maximum value is 2000. Set to 0 to skip this direction."""
    name: Literal["paddingLeft"] = "paddingLeft"
    value: int
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Left"
        json_schema_extra = {"shortDescription": "Pixels to expand left (max 2000)"}


class PaddingRight(Config):
    """Number of pixels to expand on the right side. Maximum value is 2000. Set to 0 to skip this direction."""
    name: Literal["paddingRight"] = "paddingRight"
    value: int
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Right"
        json_schema_extra = {"shortDescription": "Pixels to expand right (max 2000)"}


class PaddingUp(Config):
    """Number of pixels to expand on the top side. Maximum value is 2000. Set to 0 to skip this direction."""
    name: Literal["paddingUp"] = "paddingUp"
    value: int
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Up"
        json_schema_extra = {"shortDescription": "Pixels to expand upward (max 2000)"}


class PaddingDown(Config):
    """Number of pixels to expand on the bottom side. Maximum value is 2000. Set to 0 to skip this direction."""
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


class TextToImage(Config):
    """
    Generate a new image from a text prompt only.
    No input image required.
    """
    name: Literal["TextToImage"] = "TextToImage"
    value: Union[TextToImageRequest, TextToImageResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Text to Image"
        json_schema_extra = {"target": {"value": 0}, "shortDescription": "Generate from text only"}


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


class ImageToImage(Config):
    """
    Generate a new image based on an existing image and a text prompt.
    Use the Strength parameter to control how much the original image is preserved.
    """
    name: Literal["ImageToImage"] = "ImageToImage"
    value: Union[ImageToImageRequest, ImageToImageResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Image to Image"
        json_schema_extra = {"target": {"value": 0}, "shortDescription": "Transform an existing image"}


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


class Inpainting(Config):
    """
    Inpaint regions of an image using an instance segmentation mask.
    Replace detected objects or the background with AI-generated content
    guided by a text prompt.
    """
    name: Literal["Inpainting"] = "Inpainting"
    value: Union[InpaintingRequest, InpaintingResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Inpainting"
        json_schema_extra = {"target": {"value": 0}, "shortDescription": "Replace masked regions"}


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


class Outpainting(Config):
    """
    Expand an image beyond its original borders using AI-generated content.
    At least one direction (left, right, up, down) must be greater than 0.
    Use the Creativity parameter to control how much the output deviates from the original style.
    """
    name: Literal["Outpainting"] = "Outpainting"
    value: Union[OutpaintingRequest, OutpaintingResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Outpainting"
        json_schema_extra = {"target": {"value": 0}, "shortDescription": "Expand image borders"}


class ConfigExecutor(Config):
    """
    Select the generation task to perform.
    Text to Image: generate from prompt only.
    Image to Image: transform an existing image guided by a prompt.
    Inpainting: replace detected objects using a segmentation mask.
    Outpainting: expand the image beyond its original borders.
    """
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[TextToImage, ImageToImage, Inpainting, Outpainting]
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
