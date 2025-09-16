### **Course Structure and Philosophy**

The course is structured as a series of challenges. A key principle is to **merge related topics into broader challenges** rather than splitting them into many small ones. This is intended to create a better user experience, preventing students from having to constantly exit one challenge and start another. The goal is for each major challenge to feel substantial.

---

### ## M1P0: Navigating the File System (Read-Only)

This initial challenge focuses on viewing and moving around the file system without changing anything. It combines basic navigation commands.

* **Core Commands:**
    * `ls`: To list directory contents.
    * `cd`: To change directories.
    * `pwd`: To print the working directory.
* **Key Concepts:**
    * **Special Directories:** The meaning and usage of `~` (home directory), `.` (current directory), and `..` (parent directory) will be taught within the context of the `cd` command.
* **Challenge Idea:** Create a hidden directory. The student will first have to use the correct `ls` command to **see the hidden directory**, then `cd` into it to perform an action and find a flag.

---

### ## M1P1: Manipulating Files & Directories (Write)

This challenge introduces commands that create, modify, and delete files and directories. It represents the "write" part of file system interaction.

* **Core Commands:**
    * `mkdir`: To create new directories.
    * `cp`: To copy files and directories.
    * `mv`: To move or rename files and directories.
    * `rm`: To remove files and directories.

---

### ## M2P0: Understanding Commands

This module shifts focus from file operations to the nature of commands themselves. The goal is for students to understand what happens when they type a command.

* **What is a Command?**
    * Distinguishing between the **command** and its **arguments**.
    * Understanding that most commands are executable files.
* **Finding Commands:**
    * Using the `whereis` command to locate the file corresponding to a command.
    * Mentioning that some commands are **shell built-ins** and don't exist as separate files.
* **Getting Help:** This is a crucial skill.
    * **Man Pages:** `man`.
    * **Help Flags:** Using the common conventions of `-h` and `--help`.
    * **TLDR:** Introducing `tldr` as a user-friendly alternative for getting quick summaries of commands.

---

### ## M2P1: The Shell Environment

This challenge covers the shell itself, including customization, configuration, and environment variables.

* **Different Shells:**
    * Introduce the concept that there are different shells, such as `bash`, `zsh`, and `fish`.
* **Shell Customization:**
    * Show students that the shell can be customized to be more powerful and visually appealing.
    * Mention tools like **Oh My Zsh** to spark interest.
* **Configuration Files:**
    * Explain the role of `.bashrc` and `.zshrc`.
* **Aliases:**
    * Teach how to create command aliases for shortcuts.
* **Environment Variables:**
    * Explain what environment variables are.
    * Show how to view them (`env`) and how to read a specific variable's value (e.g., `echo $SHELL`). This will be linked back to the concept of different shells.

---

### ## M3P0: Pipes and I/O Redirection

This challenge focuses on the concept of I/O streams and how to manipulate them to chain commands together.

* **Core Concepts:**
    * Standard Input, Standard Output, and Standard Error.
    * **I/O Redirection:** Using `>` (redirect output) and `<` (redirect input).
    * **Piping:** Using the pipe `|` operator to send the output of one command to the input of another.
* **Core Commands:**
    * `echo`: To print text.
    * `cat`: To display file contents.
    * `grep`: To search for patterns in text.
* **Note:** The command `less` was explicitly **excluded** to keep the scope concise.

---

### ## M4P0: Users and Permissions

This challenge covers the multi-user nature of Linux systems, focusing on file permissions and administrative privileges.

* **Users and Groups:** The basic concept of user accounts.
* **Permissions:** Understanding the read, write, and execute permissions.
* **Commands:**
    * `chmod`: To change a file's permissions.
    * `sudo`: To execute commands with superuser (administrator) privileges.

---

### ## M5P0: Package Management (Skills for Power Users)

The final challenge introduces how to install and manage software on a Linux system.

* **Package Managers:** Explain the role of a package manager, using `apt` as the primary example.
* **Installing Software:** `apt install`.
* **Mirrors:**
    * Explain what a software mirror is and why choosing a geographically close one is important for download speed.
    * Generalize this concept, mentioning that other tools like **`pip`**, **Docker**, and **Hugging Face** also use mirrors.

---

### ### Topics Explicitly Excluded from Core Challenges

The following topics were discussed but ultimately decided against for the main curriculum to avoid overwhelming beginners. They could be mentioned as avenues for further exploration.

* **Text Editors (`vim`, `nano`):** Instead of a full tutorial, the plan is to simply **introduce them as options**. You will highlight that `nano` is simple, while `vim` (and especially a modern version like `neovim`) is highly powerful and customizable, which might encourage students to learn it on their own.
* **Terminal Multiplexers (`tmux`, `screen`):** Deemed less essential in an era where tools like VS Code Remote can manage sessions automatically.
* **Shebang (`#!`):** Considered too advanced, as most beginners will consume scripts rather than write them from scratch.
* **Advanced Shell Scripting:**
    * **Shell Expansion (backticks ``):** Deemed too advanced.
    * **Subshells & `export`:** The complexities of parent and child shells were considered out of scope.
* **WSL-Specific Features:** While tools like `wslpath` are useful, they are too platform-specific for a general course.
* **A "Boring Stuff" Appendix:** The course will conclude with a non-interactive section listing other useful commands. Students will simply need to view this page to get the final flag, without a practical exercise.