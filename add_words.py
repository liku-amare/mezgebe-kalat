import json
import tkinter as tk
from tkinter import ttk, messagebox

class DictionaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("የአማርኛ ቃለመዝ ቃላት መሰብሰቢያ")
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
        
        self.entries_frame = ttk.Frame(self.words_frame)
        self.entries_frame.pack()
        
        self.entries = []
        self.add_entry()
        
        self.add_entry_button = ttk.Button(self.words_frame, text="+ አዲስ ሥርዎ ቃል", command=self.add_entry)
        self.add_entry_button.pack()
    
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
        
        add_definition_button = ttk.Button(entry_frame, text="+ ፍቺ ጨምር ", command=lambda: self.add_definition(definitions_frame, definitions))
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
        ttk.Label(definition_frame, text="የቃል አይነት:").pack()
        pos_entry.pack(fill='x')
        
        meaning_entry = ttk.Entry(definition_frame)
        ttk.Label(definition_frame, text="ፍቺ:").pack()
        meaning_entry.pack(fill='x')
        
        example_entry = ttk.Entry(definition_frame)
        ttk.Label(definition_frame, text="ምሳሌ:").pack()
        example_entry.pack(fill='x')
        
        translation_entry = ttk.Entry(definition_frame)
        ttk.Label(definition_frame, text="ትርጉም (Eng):").pack()
        translation_entry.pack(fill='x')

        ttk.Label(definition_frame, text="ተመሳሳይ ቃላት (በ ; ይለዩ):").pack()
        synonyms_entry = ttk.Entry(definition_frame)
        synonyms_entry.pack(fill='x')
        
        ttk.Label(definition_frame, text="ተቃራኒ ቃላት (በ ; ይለዩ):").pack()
        antonyms_entry = ttk.Entry(definition_frame)
        antonyms_entry.pack(fill='x')
        
        definition_data = {
            "pos_entry": pos_entry,
            "meaning_entry": meaning_entry,
            "example_entry": example_entry,
            "translation_entry": translation_entry,
            "synonyms_entry": synonyms_entry,
            "antonyms_entry": antonyms_entry,
            "definition_frame": definition_frame,
            "toggle_button": None
        }
        
        definitions.append(definition_data)
        
        # Add the collapsible functionality to the definition
        self.add_definition_toggle_button(definition_frame, definition_data)
    
    def add_definition_toggle_button(self, definition_frame, definition_data):
        toggle_button = ttk.Button(definition_frame, text="ፍቺ ይጠቅልሉ", command=lambda: self.toggle_definition(definition_frame, toggle_button, definition_data))
        toggle_button.pack(pady=5)
        definition_data["toggle_button"] = toggle_button
    
    def toggle_definition(self, definition_frame, button, definition_data):
        # Collapse or expand based on the button's text
        if definition_frame.winfo_ismapped():
            # If the definition is visible, hide it
            definition_frame.pack_forget()
            button.config(text="ፍቺ ይዘርጉ")
        else:
            # If the definition is hidden, show it
            definition_frame.pack(fill='x', pady=5)
            button.config(text="ፍቺ ይጠቅልሉ")
    
    def save_data(self):
        word = self.word_entry.get()
        
        if not word:
            messagebox.showerror("ስህተት", "እባክዎን ቃሉን ያስገቡ")
            return
        
        if word not in self.data:
            self.data[word] = []
        
        for entry in self.entries:
            root = entry["root_entry"].get()
            pronunciation = entry["pronunciation_entry"].get()
            
            if not root or not pronunciation:
                messagebox.showerror("ስህተት", "እባክዎን ሥርዎ ቃል እና አነባበብ ያስገቡ.")
                return
            
            entry_data = {
                "root": root,
                "pronunciation": pronunciation,
                "definitions": []
            }
            
            for definition in entry["definitions"]:
                pos = definition["pos_entry"].get()
                meaning = definition["meaning_entry"].get()
                
                # Extracting and cleaning synonyms and antonyms
                synonyms = [syn.strip() for syn in definition["synonyms_entry"].get().split(';') if syn.strip()]
                antonyms = [ant.strip() for ant in definition["antonyms_entry"].get().split(';') if ant.strip()]
                
                # Append the definition with synonyms and antonyms
                entry_data["definitions"].append({
                    "partOfSpeech": pos,
                    "meaning": meaning,
                    "example": definition["example_entry"].get(),
                    "translation": definition["translation_entry"].get(),
                    "synonyms": synonyms,
                    "antonyms": antonyms
                })
            
            self.data[word].append(entry_data)
        
        try:
            with open("words.json", "r", encoding="utf-8") as f:
                words_dict = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            words_dict = {}
        
        words_dict.update(self.data)
        
        with open("words.json", "w", encoding="utf-8") as f:
            json.dump(words_dict, f, ensure_ascii=False, indent=4)
        
        messagebox.showinfo("ተሳክቷል", "ቃሉ በሚገባ ተቀምጧል!")
        self.data.clear()
    
    def reset_form(self):
        self.word_entry.delete(0, tk.END)
        for entry in self.entries:
            entry["root_entry"].delete(0, tk.END)
            entry["pronunciation_entry"].delete(0, tk.END)
            for definition in entry["definitions"]:
                definition["pos_entry"].delete(0, tk.END)
                definition["meaning_entry"].delete(0, tk.END)
                definition["example_entry"].delete(0, tk.END)
                definition["translation_entry"].delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    root.mainloop()
