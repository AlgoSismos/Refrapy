import sys

from refrapy.refrainv import Refrainv
from refrapy.refrapick import Refrapick


def main():
    default_args = ["pick", "inv"]

    if len(sys.argv) == 1:
        print(
            "Refrapy - Seismic Refraction Data Analysis\n"
            'Refrapy needs an argument. \nCall "refrapy pick" or "refrapy inv"\n'
            'for using the "pick" or "inv" apps.\n'
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
        print(
            "Refrapy - Seismic Refraction Data Analysis\n"
            'Wrong usage. Call "refrapy pick" or "refrapy inv"\n'
            'for using the "pick" or "inv" apps.\n'
        )
        exit()


if __name__ == "__main__":
    main()
