import sys

from refrapy import Refrainv, Refrapick, __version__


def main():
    default_args = ["pick", "inv"]

    print(f"Refrapy - Seismic Refraction Data Analysis\nversion: {__version__}\n")

    if len(sys.argv) == 1:
        print(
            "Refrapy needs an argument.\n"
            'Call "refrapy pick" or "refrapy inv"\n'
            'for using the "Refrapick" or "inv" apps.\n'
        )
        exit()

    arg = sys.argv[1]

    if arg in default_args:
        if arg == "pick":
            app = Refrapick()
        elif arg == "inv":
            app = Refrainv()

        app.mainloop()

    else:
        print('Wrong usage.\nCall "refrapy pick" or "refrapy inv"\nfor using the "Refrapick" or "Refrainv" apps.\n')
        exit()


if __name__ == "__main__":
    main()
