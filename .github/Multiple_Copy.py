import shutil
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class FileCopyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi Copy Tool")
        self.root.geometry("400x400")  # Adjusted for progress bar
        
        self.files = []  # List to store selected files
        self.dest_folder = ""  # Destination folder

        # Create buttons
        self.choose_files_btn = tk.Button(root, text="Choose Files", command=self.select_files, width=20)
        self.choose_files_btn.pack(pady=10)

        self.select_target_btn = tk.Button(root, text="Select Target Folder", command=self.select_destination, width=20)
        self.select_target_btn.pack(pady=10)

        self.paste_now_btn = tk.Button(root, text="Paste Now", command=self.copy_files, width=20, state=tk.DISABLED)
        self.paste_now_btn.pack(pady=10)

        self.how_to_use_btn = tk.Button(root, text="How to Use", command=self.show_instructions, width=20)
        self.how_to_use_btn.pack(pady=10)

        self.status_label = tk.Label(root, text="Select files and target folder", fg="blue")
        self.status_label.pack(pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(root, length=300, mode='determinate')
        self.progress.pack(pady=10)

        # New button for contacting you
        self.contact_btn = tk.Button(root, text="More Tools! Contact Me", command=self.show_contact_info, width=20)
        self.contact_btn.pack(pady=10)

    def select_files(self):
        new_files = filedialog.askopenfilenames(title="Choose Files to Copy")
        if new_files:
            self.files.extend(new_files)
            self.status_label.config(text=f"{len(self.files)} files selected", fg="green")
            self.paste_now_btn.config(state=tk.NORMAL)

    def select_destination(self):
        self.dest_folder = filedialog.askdirectory(title="Select Target Folder")
        if self.dest_folder:
            self.status_label.config(text="Target folder selected", fg="green")

    def copy_files(self):
        if not self.files:
            messagebox.showerror("Error", "No files selected!")
            return
        if not self.dest_folder:
            messagebox.showerror("Error", "No target folder selected!")
            return

        existing_files = []  # List to store files that already exist in the target folder
        copied_files = 0  # Counter for successful copies
        self.progress['value'] = 0
        self.progress['maximum'] = len(self.files)

        try:
            for i, file in enumerate(self.files, start=1):
                dest_path = os.path.join(self.dest_folder, os.path.basename(file))
                if os.path.exists(dest_path):
                    existing_files.append(os.path.basename(file))  # Add to list of existing files
                else:
                    shutil.copy(file, self.dest_folder)
                    copied_files += 1  # Increment the count for successful copies
                    print(f"Copied: {file} → {self.dest_folder}")
                
                # Update progress bar
                self.progress['value'] = i
                self.root.update_idletasks()

            # Check if there were any existing files and show appropriate message
            if existing_files:
                messagebox.showerror("Error", f"Some file you are trying to paste already exists but others have been pasted. Existing files: {', '.join(existing_files)}")

            # Show success message
            if copied_files > 0:
                messagebox.showinfo("Success", f"{copied_files} files copied successfully!")
                self.status_label.config(text="Copy complete!", fg="red")  # Set the status color to red for success
            else:
                self.status_label.config(text="No new files were pasted.", fg="red")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_label.config(text="An error occurred during copy", fg="red")
        
        self.progress['value'] = 0  # Reset progress bar

    def show_instructions(self):
        instructions = (
            "Multi Copy Tool - How to Use:\n\n"
            "1. Click 'Choose File' to select the files from different folders you want to copy.\n"
            "2. Click 'Select Target Folder' to choose the folder where you want to paste the files.\n"
            "3. If you select the same file again, you will see an error message indicating that the file already exists.\n"
            "4. Click 'Paste Now' to copy the selected files to the target folder.\n"
            "5. You will be notified of any errors or successful file copies.\n\n"
            "Enjoy using Multi Copy!"
        )

        # Create a new window for instructions
        instructions_window = tk.Toplevel(self.root)
        instructions_window.title("How to Use")

        # Add a label to display instructions with a larger font
        instructions_label = tk.Label(instructions_window, text=instructions, justify=tk.LEFT, font=("Arial", 12), padx=10, pady=10)
        instructions_label.pack(expand=True, fill=tk.BOTH)

        # Add a button to close the instructions window
        close_btn = tk.Button(instructions_window, text="Close", command=instructions_window.destroy)
        close_btn.pack(pady=10)

    def show_contact_info(self):
        # Create a new window for contact info with selectable email
        contact_window = tk.Toplevel(self.root)
        contact_window.title("Contact Me")

        # Create a Text widget that will display the email, making it selectable
        email_text = tk.Text(contact_window, height=1, width=40, wrap=tk.WORD)
        email_text.insert(tk.END, "hajianhosein@yahoo.com")
        email_text.config(state=tk.DISABLED)  # Make the text non-editable but selectable
        email_text.pack(padx=10, pady=10)

        # Add a button to close the contact window
        close_btn = tk.Button(contact_window, text="Close", command=contact_window.destroy)
        close_btn.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCopyApp(root)
    root.mainloop()
