class Pazer:
    pages_names = []
    pages_ids = []
    items_on_page = 5
    current_page = 0
    current_select = 0
    select_tuple = ("> ", "")

    def __init__(self, items, items_on_page=5, select_str="> ", unselect_str=""):
        self.load_items(items)
        self.items_on_page = items_on_page
        self.select_tuple = (select_str, unselect_str)

    def load_items(self, items):
        pages_ids = [list(items.keys())[r:r + self.items_on_page] for r in
                     range(0, len(list(items.keys())), self.items_on_page)]
        pages_names = [list(items.values())[r:r + self.items_on_page] for r in
                       range(0, len(list(items.values())), self.items_on_page)]
        self.pages_names = pages_names
        self.pages_ids = pages_ids

    def change_page(self, i):
        if 0 <= self.current_page + i < len(self.pages_names):
            self.current_page += i
            self.current_select = 0

    def change_select(self, i):
        if 0 <= self.current_select + i < len(self.pages_names[self.current_page]):
            self.current_select += i

    def render(self):
        strout = []
        for i, name in enumerate(self.pages_names[self.current_page]):
            strout.append(f"""{i}) {self.select_tuple[0 if i == self.current_select else 1]}{name}""")
        strout.append(f"\nPage {self.current_page+1}/{len(self.pages_names)}\n")
        return "\n".join(strout)


if __name__ == "__main__":
    a = {
        "0": "Foo",
        "1": "Bar",
        "2": "Tar",
        "3": "Evar",
        "4": "Itor",
        "5": "Vior",
        "6": "Foo444",
        "7": "Bar1234",
        "8": "Tar907",
        "9": "Evar712",
        "10": "Itor98761",
        "11": "13Vior978",
        "12": "234Foo56789",
        "13": "11123Bar989898",
        "14": "7653Tar37",
        "15": "1Evar1",
        "16": "845Itor321",
        "17": "567Vior43",
    }
    pzr = Pazer(a, select_str=">>> ", unselect_str="")
    strin = None
    while strin != ["e"]:
        print(pzr.render())
        strin = input("input >>> ").split()
        if len(strin) == 2:
            if strin[0] == "p":
                pzr.change_page(int(strin[1]))

            if strin[0] == "s":
                pzr.change_select(int(strin[1]))

        elif len(strin) == 1:
            if strin[0] == "g":
                print(f"\n{pzr.pages_names[pzr.current_page][pzr.current_select]} = {pzr.pages_ids[pzr.current_page][pzr.current_select]}\n")

