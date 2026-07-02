# Smart Grid Manager ☀️🔋

O aplicație consolă dezvoltată în **Python** pentru gestionarea eficientă a unei rețele inteligente de energie (Smart Grid). Proiectul simulează monitorizarea producției panourilor solare în timp real și salvarea istoricului de consum, utilizând structuri de date avansate pentru optimizarea performanței.

---

### 🧠 Structuri de Date Utilizate

Pentru a asigura o eficiență maximă în gestionarea datelor, proiectul implementează de la zero două structuri fundamentale:

1. **Max-Heap (Priority Queue):** 
   * Folosit pentru monitorizarea panourilor solare.
   * Permite identificarea instantanee ($O(1)$) și extragerea/actualizarea rapidă ($O(\log n)$) a panoului cu cea mai mare producție de energie curentă.
2. **Red-Black Tree (RBT):**
   * Un arbore binar de căutare echilibrat, utilizat pentru stocarea și sortarea rapoartelor de consum în funcție de ID.
   * Garantează operații eficiente de căutare, inserare și ștergere în timp logaritmic ($O(\log n)$).

---

### 🛠️ Tehnologii și Funcționalități

* **Language:** Python 3
* **Persistența Datelor:** Salvare automată și încărcare din fișier JSON (`smartgriddata.json`).
* **Meniu Interactiv:** Operare directă din terminal (Adăugare/Ștergere panouri, Jurnal complet sortat, Căutare rapidă rapoarte).

---

### 🚀 Cum se rulează proiectul

1. Asigură-te că ai Python instalat pe sistem.
2. Descarcă sau clonează acest repository.
3. Deschide un terminal în folderul proiectului și rulează:
   ```bash
   python main.py
