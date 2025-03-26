import json
import tkinter as tk
from tkinter import ttk, messagebox
import ipa_lookup

class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("የአማርኛ ቃላት ውሂብ መሰብሰቢያ")
        self.data = {}
        
        self.create_initial_fields()
        
        self.save_button = ttk.Button(root, text="አስቀምጥ", command=self.save_data)
        self.save_button.pack(pady=5)
        
        self.reset_button = ttk.Button(root, text="አጥፋ", command=self.reset_form)
        self.reset_button.pack(pady=5)
    
    def create_initial_fields(self):
        self.words_frame = ttk.Frame(self.root)
        self.words_frame.pack(pady=10)
        
        ttk.Label(self.words_frame, text="ቃል:").pack()
        self.word_entry = ttk.Entry(self.words_frame)
        self.word_entry.pack(fill='x')
        self.word_entry.bind("<Return>", self.update_pronunciation)
        
        self.entries_frame = ttk.Frame(self.words_frame)
        self.entries_frame.pack()
        
        self.entries = []
        self.add_entry()
        
        self.add_entry_button = ttk.Button(self.words_frame, text="+ አዲስ ሥርዎ ቃል", command=self.add_entry)
        self.add_entry_button.pack()
    
    def update_pronunciation(self, event):
        word = self.word_entry.get()
        if word:
            pronunciation = ipa_lookup.get_pronunciation(word)
            if self.entries:
                self.entries[0]["pronunciation_entry"].delete(0, tk.END)
                self.entries[0]["pronunciation_entry"].insert(0, pronunciation)
    
    def add_entry(self):
        entry_frame = ttk.Frame(self.entries_frame, relief="groove", borderwidth=2)
        entry_frame.pack(side="left", padx=10)
        
        ttk.Label(entry_frame, text="ሥርዎ ቃል:").pack()
        root_entry = ttk.Entry(entry_frame)
        root_entry.pack(fill='x')
        
        ttk.Label(entry_frame, text="አነባበብ:").pack()
        pronunciation_entry = ttk.Entry(entry_frame)
        pronunciation_entry.pack(fill='x')
        
        ttk.Label(entry_frame, text="ፍቺዎች", font=("Arial", 10, "bold")).pack(pady=5)
        
        definitions_frame = ttk.Frame(entry_frame)
        definitions_frame.pack(pady=5)
        
        definitions = []
        self.add_definition(definitions_frame, definitions)
        
        add_definition_button = ttk.Button(entry_frame, text="+ ፍቺ ይጨምሩ", command=lambda: self.add_definition(definitions_frame, definitions))
        add_definition_button.pack()
        
        self.entries.append({
            "root_entry": root_entry,
            "pronunciation_entry": pronunciation_entry,
            "definitions": definitions
        })
    
    def add_definition(self, parent_frame, definitions):
        definition_frame = ttk.Frame(parent_frame, relief="groove", borderwidth=2)
        definition_frame.pack(fill='x', pady=5)
        
        pos_entry = ttk.Entry(definition_frame)
        ttk.Label(definition_frame, text="የቃል ዓይነት:").pack()
        pos_entry.pack(fill='x')
        
        meaning_entry = ttk.Entry(definition_frame)
        ttk.Label(definition_frame, text="ፍቺ:").pack()
        meaning_entry.pack(fill='x')
        
        example_entry = ttk.Entry(definition_frame)
        ttk.Label(definition_frame, text="ምሳሌ:").pack()
        example_entry.pack(fill='x')
        
        translation_entry = ttk.Entry(definition_frame)
        ttk.Label(definition_frame, text="ትርጉም:").pack()
        translation_entry.pack(fill='x')
        
        ttk.Label(definition_frame, text="ተመሳሳይ ቃላት (በ ; ይለዩ):").pack()
        synonyms_entry = ttk.Entry(definition_frame)
        synonyms_entry.pack(fill='x')
        
        ttk.Label(definition_frame, text="ተቃራኒ ቃላት (በ ; ይለዩ):").pack()
        antonyms_entry = ttk.Entry(definition_frame)
        antonyms_entry.pack(fill='x')
        
        definitions.append({
            "pos_entry": pos_entry,
            "meaning_entry": meaning_entry,
            "example_entry": example_entry,
            "translation_entry": translation_entry,
            "synonyms_entry": synonyms_entry,
            "antonyms_entry": antonyms_entry
        })
    
    def save_data(self):
        word = self.word_entry.get()
        
        if not word:
            messagebox.showerror("ስህተት", "እባክዎ ቃሉን ያስገቡ!")
            return
        
        if word not in self.data:
            self.data[word] = []
        
        for entry in self.entries:
            root = entry["root_entry"].get()
            pronunciation = entry["pronunciation_entry"].get()
            
            if not root or not pronunciation:
                messagebox.showerror("ስህተት", "እባክዎን ሥርዎ ቃል እና አነባበብ ያስገቡ።")
                return
            
            entry_data = {
                "root": root,
                "pronunciation": pronunciation,
                "definitions": []
            }
            
            for definition in entry["definitions"]:
                pos = definition["pos_entry"].get()
                meaning = definition["meaning_entry"].get()
                
                if not pos or not meaning:
                    messagebox.showerror("ስህተት", "የቃል ዓይነት እና ፍቺ ባዶ መሆን አይችሉም።")
                    return
                
                synonyms = [syn.strip() for syn in definition["synonyms_entry"].get().split(';') if syn.strip()]
                antonyms = [ant.strip() for ant in definition["antonyms_entry"].get().split(';') if ant.strip()]
                
                definition_data = {
                    "partOfSpeech": pos,
                    "meaning": meaning,
                    "example": definition["example_entry"].get(),
                    "translation": definition["translation_entry"].get(),
                    "synonyms": synonyms,
                    "antonyms": antonyms
                }
                entry_data["definitions"].append(definition_data)
            
            self.data[word].append(entry_data)
        
        try:
            with open("words.json", "r", encoding="utf-8") as f:
                words_dict = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            words_dict = {}
        
        words_dict.update(self.data)
        
        with open("words.json", "w", encoding="utf-8") as f:
            json.dump(words_dict, f, ensure_ascii=False, indent=4)
        
        messagebox.showinfo("ስኬት", "ተቀምጧል።")
        self.data.clear()
    
    def reset_form(self):
        self.root.destroy()
        self.__init__(tk.Tk())
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()