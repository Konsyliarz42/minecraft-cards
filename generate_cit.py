import logging
from datetime import date
from pathlib import Path

ROOT_PATH = "./assets/minecraft/optifine/cit"
JSON_TEMPLATE = """{{
	"parent": "item/card",
	"textures": {{
		"card": "item/card",
		"image": "./{image}"
	}}
}}
"""
PROPERTIES_TEMPLATE = """type=item
matchItems=paper
model={model}
nbt.display.Name=iregex:({name})
"""
LOG_FILE = f"logs/{date.today()}.log"


logging.basicConfig(
    format="%(asctime)s %(levelname)8s | %(message)s",
    filename=LOG_FILE,
    level=logging.INFO,
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    files = Path(ROOT_PATH).glob("**/*")
    
    for file in files:
        if file.is_file() and file.suffix == ".png":
            absolute_path = file.absolute().parent / file.stem.lower()
            regex_name = file.stem.replace("_", " ").lower()
            logger.info("Create card for: `%s`", absolute_path.name)

            logger.debug("- Rename `.png` file to lower case")
            file.rename(absolute_path.with_suffix(".png"))

            logger.debug("- Create model")
            json_path = absolute_path.with_suffix(".json")
            json_path.write_text(JSON_TEMPLATE.format(image=file.stem.lower()))

            logger.debug("- Add properties")
            properties_path = absolute_path.with_suffix(".properties")
            properties_path.write_text(PROPERTIES_TEMPLATE.format(
                model=json_path.stem, name=regex_name
            ))
