import argparse
import readData

def main(args):
	readData.readTrainingData()


if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="HomeWork Five")
        parser.add_argument("--input", type=str)
        args = parser.parse_args()
        main(args)


