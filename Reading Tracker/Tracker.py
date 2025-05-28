import tkinter as tk
from tkinter import messagebox, simpledialog
import os

FILENAME = "reading_log.txt"

# Load books from file
def load_books():
    books = []
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            for line in f:
                title, author, status, pages = line.strip().split("|")
                books.append({
                    "title": title,
                    "author": author,
                    "status": status,
                    "pages": pages
                })
    return books

# Save books to file
def save_books():
    with open(FILENAME, "w") as f:
        for book in books:
            f.write(f"{book['title']}|{book['author']}|{book['status']}|{book['pages']}\n")

# Refresh book listbox
def refresh_listbox(filtered_books=None):
    listbox.delete(0, tk.END)
    for i, book in enumerate(filtered_books or books):
        listbox.insert(tk.END, f"{i+1}. {book['title']} by {book['author']} - [{book['status']}, Page {book['pages']}]")

# Add a new book
def add_book():
    title = simpledialog.askstring("Book Title", "Enter book title:")
    if not title:
        return
    author = simpledialog.askstring("Author", "Enter author name:")
    if not author:
        return
    page = simpledialog.askstring("Pages Read", "How many pages have you read?")
    if not page or not page.isdigit():
        page = "0"
    books.append({"title": title, "author": author, "status": "Not Read", "pages": page})
    refresh_listbox()
    save_books()

# Mark selected book as read
def mark_read():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Please select a book.")
        return
    index = selection[0]
    books[index]["status"] = "Read"
    refresh_listbox()
    save_books()

# Mark selected book as unread
def mark_unread():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Please select a book.")
        return
    index = selection[0]
    books[index]["status"] = "Not Read"
    refresh_listbox()
    save_books()

# Update page number
def update_pages():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("No selection", "Please select a book.")
        return
    index = selection[0]
    page = simpledialog.askstring("Update Pages", "Enter page number you've read up to:")
    if page and page.isdigit():
        books[index]["pages"] = page
        refresh_listbox()
        save_books()

# Search books
def search_books():
    query = search_entry.get().lower()
    if not query:
        refresh_listbox()
        return
    filtered = [book for book in books if query in book["title"].lower() or query in book["author"].lower()]
    refresh_listbox(filtered)

# Show unread books
def show_unread():
    unread_books = [book for book in books if book["status"] != "Read"]
    refresh_listbox(unread_books)

# --- GUI Setup ---
books = load_books()

root = tk.Tk()
root.title("📚 BookBuddy")

# Search bar
search_frame = tk.Frame(root)
search_frame.pack(pady=5)

tk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Search", command=search_books).pack(side=tk.LEFT)
tk.Button(search_frame, text="📖 Show Unread", command=show_unread).pack(side=tk.LEFT, padx=5)

# Listbox
listbox = tk.Listbox(root, width=60, height=12)
listbox.pack(pady=10)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="➕ Add Book", command=add_book).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="✅ Mark as Read", command=mark_read).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="❎ Mark as Unread", command=mark_unread).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="📝 Update Page", command=update_pages).grid(row=0, column=3, padx=5)

refresh_listbox()

root.mainloop()
