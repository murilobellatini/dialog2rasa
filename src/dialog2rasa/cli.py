import argparse


from dialog2rasa.converters.core import DialogflowToRasaConverter


def main():
    parser = argparse.ArgumentParser(
        description="Convert Dialogflow agent to Rasa YAML format. Output will be "
    )
    parser.add_argument(
        "--path",
        "-p",
        required=True,
        help="The path to the extracted Dialogflow agent directory",
    )

    args = parser.parse_args()

    converter = DialogflowToRasaConverter(args.path)
    converter.convert_all()


if __name__ == "__main__":
    main()
