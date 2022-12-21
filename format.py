import argparse

parser = argparse.ArgumentParser()

parser.add_argument("text")
parser.add_argument("--style", nargs="+")

args = parser.parse_args()

prefix = ""
if args.style:
    for i in args.style:
        match i:
            case "bold" | "b":
                prefix += "**"
            case "italics" | "i":
                prefix += "*"
            case "underline" | "u":
                prefix += "__"
            case "strikethrough" | "s":
                prefix += "~~"
            case "code" | "c":
                prefix += "`"

suffix = prefix[::-1]

print(f"{prefix}{args.text}{suffix}")