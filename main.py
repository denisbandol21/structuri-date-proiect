import json
import os

class PanouSolar:
    def __init__(self, id_panou, locatie, productie_curenta):
        self.id_panou = id_panou
        self.locatie = locatie
        self.productie_curenta = productie_curenta

    def to_dict(self):
        return {
            "id_panou": self.id_panou,
            "locatie": self.locatie,
            "productie_curenta": self.productie_curenta
        }

    @staticmethod
    def from_dict(data):
        return PanouSolar(data["id_panou"], data["locatie"], data["productie_curenta"])

    def __repr__(self):
        return f"Panou ID {self.id_panou} Locatie {self.locatie} Productie {self.productie_curenta} kW"

class MaxHeap:
    def __init__(self):
        self.heap = []
        self.id_map = {}

    def get_parent(self, i):
        return (i - 1) // 2

    def get_left(self, i):
        return 2 * i + 1

    def get_right(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.id_map[self.heap[i].id_panou] = j
        self.id_map[self.heap[j].id_panou] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, panou):
        if panou.id_panou in self.id_map:
            self.update_priority(panou.id_panou, panou.productie_curenta)
            return
        self.heap.append(panou)
        index = len(self.heap) - 1
        self.id_map[panou.id_panou] = index
        self.sift_up(index)

    def sift_up(self, index):
        parent = self.get_parent(index)
        while index > 0 and self.heap[parent].productie_curenta < self.heap[index].productie_curenta:
            self.swap(index, parent)
            index = parent
            parent = self.get_parent(index)

    def get_max(self):
        if not self.heap:
            return None
        return self.heap[0]

    def extract_max(self):
        if not self.heap:
            return None
        max_panou = self.heap[0]
        del self.id_map[max_panou.id_panou]
        last_panou = self.heap.pop()
        if self.heap:
            self.heap[0] = last_panou
            self.id_map[last_panou.id_panou] = 0
            self.sift_down(0)
        return max_panou

    def delete(self, id_panou):
        if id_panou not in self.id_map:
            return False
        index = self.id_map[id_panou]
        del self.id_map[id_panou]
        if index == len(self.heap) - 1:
            self.heap.pop()
            return True
        last_panou = self.heap.pop()
        self.heap[index] = last_panou
        self.id_map[last_panou.id_panou] = index
        parent = self.get_parent(index)
        if index > 0 and self.heap[parent].productie_curenta < self.heap[index].productie_curenta:
            self.sift_up(index)
        else:
            self.sift_down(index)
        return True

    def sift_down(self, index):
        max_index = index
        left = self.get_left(index)
        right = self.get_right(index)
        if left < len(self.heap) and self.heap[left].productie_curenta > self.heap[max_index].productie_curenta:
            max_index = left
        if right < len(self.heap) and self.heap[right].productie_curenta > self.heap[max_index].productie_curenta:
            max_index = right
        if index != max_index:
            self.swap(index, max_index)
            self.sift_down(max_index)

    def update_priority(self, id_panou, noua_productie):
        if id_panou not in self.id_map:
            return
        index = self.id_map[id_panou]
        vechea_productie = self.heap[index].productie_curenta
        self.heap[index].productie_curenta = noua_productie
        if noua_productie > vechea_productie:
            self.sift_up(index)
        elif noua_productie < vechea_productie:
            self.sift_down(index)

    def get_total_production(self):
        return sum(panou.productie_curenta for panou in self.heap)

class RaportConsum:
    def __init__(self, id_raport, consum_total, status_retea):
        self.id_raport = id_raport
        self.consum_total = consum_total
        self.status_retea = status_retea

    def to_dict(self):
        return {
            "id_raport": self.id_raport,
            "consum_total": self.consum_total,
            "status_retea": self.status_retea
        }

    @staticmethod
    def from_dict(data):
        id_raport = data.get("id_raport")
        if id_raport is None and "timestamp" in data:
            try:
                id_raport = abs(hash(data["timestamp"])) % 10000
            except:
                id_raport = 0
                
        return RaportConsum(id_raport, data["consum_total"], data["status_retea"])

    def __repr__(self):
        return f"Raport ID {self.id_raport} Consum {self.consum_total} kW Status {self.status_retea}"

class RBTNode:
    def __init__(self, raport):
        self.raport = raport
        self.color = "RED"
        self.parent = None
        self.left = None
        self.right = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = RBTNode(None)
        self.TNULL.color = "BLACK"
        self.root = self.TNULL

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, raport):
        if self.search(raport.id_raport) is not None:
            return False
        node = RBTNode(raport)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "RED"
        y = None
        x = self.root
        while x != self.TNULL:
            y = x
            if node.raport.id_raport < x.raport.id_raport:
                x = x.left
            else:
                x = x.right
        node.parent = y
        if y is None:
            self.root = node
        elif node.raport.id_raport < y.raport.id_raport:
            y.left = node
        else:
            y.right = node
        if node.parent is None:
            node.color = "BLACK"
            return True
        if node.parent.parent is None:
            return True
        self.fix_insert(node)
        return True

    def fix_insert(self, k):
        while k.parent.color == "RED":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == "RED":
                    u.color = "BLACK"
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "BLACK"
                    k.parent.parent.color = "RED"
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "BLACK"

    def search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.raport.id_raport:
            return node
        if key < node.raport.id_raport:
            return self.search_tree_helper(node.left, key)
        return self.search_tree_helper(node.right, key)

    def search(self, key):
        res = self.search_tree_helper(self.root, key)
        if res != self.TNULL:
            return res.raport
        return None

    def delete_node(self, key):
        z = self.TNULL
        node = self.root
        while node != self.TNULL:
            if node.raport.id_raport == key:
                z = node
                break
            if node.raport.id_raport <= key:
                node = node.right
            else:
                node = node.left
        if z == self.TNULL:
            return False
        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "BLACK":
            self.fix_delete(x)
        return True

    def fix_delete(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "RED":
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == "BLACK" and s.right.color == "BLACK":
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.right.color == "BLACK":
                        s.left.color = "BLACK"
                        s.color = "RED"
                        self.right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.right.color = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "RED":
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.right_rotate(x.parent)
                    s = x.parent.left
                if s.left.color == "BLACK" and s.right.color == "BLACK":
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.left.color == "BLACK":
                        s.right.color = "BLACK"
                        s.color = "RED"
                        self.left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.left.color = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "BLACK"

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def inorder_helper(self, node):
        if node != self.TNULL:
            self.inorder_helper(node.left)
            print(f"{node.raport}")
            self.inorder_helper(node.right)

    def inorder_traversal(self):
        if self.root == self.TNULL:
            print("Istoricul este gol")
        else:
            self.inorder_helper(self.root)

    def get_all_reports(self, node=None, reports=None):
        if reports is None:
            reports = []
        if node is None:
            node = self.root
        if node != self.TNULL:
            self.get_all_reports(node.left, reports)
            reports.append(node.raport)
            self.get_all_reports(node.right, reports)
        return reports

class SmartGridManager:
    DATA_FILE = "smartgriddata.json"

    def __init__(self):
        self.max_heap = MaxHeap()
        self.rbt = RedBlackTree()
        self.incarca_date()

    def salveaza_date(self):
        data = {
            "panouri": [panou.to_dict() for panou in self.max_heap.heap],
            "rapoarte": [raport.to_dict() for raport in self.rbt.get_all_reports()]
        }
        with open(self.DATA_FILE, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def incarca_date(self):
        if not os.path.exists(self.DATA_FILE):
            return
        try:
            with open(self.DATA_FILE, "r", encoding="utf8") as f:
                data = json.load(f)
            for p_dict in data.get("panouri", []):
                self.max_heap.insert(PanouSolar.from_dict(p_dict))
            for r_dict in data.get("rapoarte", []):
                self.rbt.insert(RaportConsum.from_dict(r_dict))
        except json.JSONDecodeError:
            print("Eroare citire fisier")

    def inregistreaza_productie_noua(self, id_panou, locatie, productie_curenta):
        panou = PanouSolar(id_panou, locatie, productie_curenta)
        self.max_heap.insert(panou)
        self.salveaza_date()

    def afiseaza_toate_panourile(self):
        if not self.max_heap.heap:
            print("Niciun panou inregistrat")
            return
        for i, panou in enumerate(self.max_heap.heap):
            if i == 0:
                print(f"{panou} (top sursa)")
            else:
                print(f"{panou}")

    def sterge_panou(self, id_panou):
        succes = self.max_heap.delete(id_panou)
        if succes:
            self.salveaza_date()
        return succes

    def sterge_raport_istoric(self, id_raport):
        succes = self.rbt.delete_node(id_raport)
        if succes:
            self.salveaza_date()
        return succes

    def salveaza_istoric_consum(self, id_raport, consum_total):
        status = "Optim" if consum_total < 1000 else "Supraincarcat"
        raport = RaportConsum(id_raport, consum_total, status)
        succes = self.rbt.insert(raport)
        if succes:
            self.salveaza_date()
        return succes

    def cauta_istoric(self, id_raport):
        return self.rbt.search(id_raport)

    def afiseaza_jurnal_complet(self):
        self.rbt.inorder_traversal()

def main():
    manager = SmartGridManager()
    while True:
        print("Meniu")
        print("1 Adauga panou solar")
        print("2 Toate panourile")
        print("3 Adauga istoric consum")
        print("4 Cauta istoric")
        print("5 Jurnal complet")
        print("6 Sterge date")
        print("7 Iesire")
        opt = input("Optiune ").strip()
        if opt == "1":
            id_panou = input("ID panou ")
            locatie = input("Locatie ")
            try:
                prod = float(input("Productie kW "))
                manager.inregistreaza_productie_noua(id_panou, locatie, prod)
                print("Adaugat cu succes")
            except ValueError:
                print("Eroare")
        elif opt == "2":
            manager.afiseaza_toate_panourile()
        elif opt == "3":
            try:
                id_raport = int(input("ID raport numar intreg "))
                consum = float(input("Consum kW "))
                succes = manager.salveaza_istoric_consum(id_raport, consum)
                if succes:
                    print("Raport adaugat")
                else:
                    print("Eroare raport existent")
            except ValueError:
                print("Eroare introduceti numere")
        elif opt == "4":
            try:
                id_raport = int(input("ID raport numar intreg "))
                raport = manager.cauta_istoric(id_raport)
                if raport:
                    print(f"Gasit {raport}")
                else:
                    print("Negasit")
            except ValueError:
                print("Eroare introduceti numere")
        elif opt == "5":
            print("Jurnal istoric")
            manager.afiseaza_jurnal_complet()
        elif opt == "6":
            print("Stergere")
            print("p Panou")
            print("r Raport")
            sub_opt = input("Alegere p sau r ").strip().lower()
            if sub_opt == "p":
                id_panou = input("ID panou ")
                succes = manager.sterge_panou(id_panou)
                if succes:
                    print("Sters")
                else:
                    print("Negasit")
            elif sub_opt == "r":
                try:
                    id_raport = int(input("ID raport numar intreg de sters "))
                    succes = manager.sterge_raport_istoric(id_raport)
                    if succes:
                        print("Sters")
                    else:
                        print("Negasit")
                except ValueError:
                    print("Eroare introduceti numere")
            else:
                print("Anulat")
        elif opt == "7":
            print("La revedere")
            break
        else:
            print("Invalida")

if __name__ == "__main__":
    main()