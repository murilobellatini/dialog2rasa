import argparse
from pathlib import Path

from dialog2rasa.converters.core import DialogflowToRasaConverter
from dialog2rasa.utils.general import setup_logger


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Transforms a Dialogflow agent into Rasa format. "
        "The result is saved in /output/[LANGUAGE_CODE], where [LANGUAGE_CODE] "
        "is replaced with the actual language code (e.g., 'en', 'de'), inside "
        "the Dialogflow agent's directory."
    )
    parser.add_argument(
        "--path",
        "-p",
        required=True,
        help="Path to the Dialogflow agent's extracted/unzipped folder.",
    )
    parser.add_argument(
        "--language",
        "-l",
        default="de",
        help="Language code (e.g., 'en' for English) of the Dialogflow agent. "
        "Defaults to 'de' (German).",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Increase output verbosity for debugging purposes.",
    )

    args = parser.parse_args()

    logger = setup_logger(verbose=args.verbose)

    converter = DialogflowToRasaConverter(
        agent_dir=Path(args.path), language=args.language, logger=logger
    )
    converter.convert_all()


if __name__ == "__main__":
    main()
