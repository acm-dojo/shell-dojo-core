Linux is a multi-user system, meaning it has built-in rules to protect files from being accessed or modified by the wrong people. This lesson gives you the keys to understand and control those rules.

---

## Users and Groups

In Linux, everything is owned by a user. Every file and every process (running program) is associated with a specific user account. This is how the system keeps track of who is doing what.

User: An individual account. When you log in, you are acting as a specific user. The most powerful user is called root (or the superuser), which has unlimited access to the entire system.

Group: A collection of users. Groups make it easy to manage permissions for multiple users at once. The most practical example is the `www-data` group for web servers, you do not want every user to have access to the webpages; also, you do not want web servers like Nginx or Caddy to have access to your personal files. [This post explain it well](https://askubuntu.com/questions/873839/what-is-the-www-data-user).

You can see who you are with the whoami command.

```bash
whoami
```

---

## The `rwx` Permissions

You have already learned about the `ls -la` command in previous lessons, the `-l` flag shows detailed information about files, including their permissions. Here is what you might see:

```bash
total 96
drwxr-x---+ 119 theunknownthing  staff   3.7K Sep 15 16:09 ..
drwxr-xr-x@   8 theunknownthing  staff   256B Sep 15 16:00 contents
drwxr-xr-x@  15 theunknownthing  staff   480B Sep 15 15:59 .git
-rw-r--r--@   1 theunknownthing  staff   1.1K Sep  9 20:58 README.md
...
```

See the `drwxr-xr-x` part? This is where the permissions are shown.

---

Let me first explain the characters for you. There are three basic permissions:

- Read (r): The ability to **view** the contents of a file or **list** the contents of a directory.

- Write (w): The ability to **change** or **delete** a file, or **create/delete** files within a directory.

- Execute (x): The ability to **run** a file (if it's a program or script) or **enter** a directory (`cd` into it).

The first character indicates the type of file: `d` for directory, `-` for a regular file, `l` for a symbolic link, and other characters for special file types.

So, in `drwxr-xr-x@  15 theunknownthing  staff   480B Sep 15 15:59 .git`:

- `d` indicates it's a directory.
- Then you can see exactly 9 characters, divided into three groups of three.

  The first 3 characters (`rwx`) is the **owner**'s permissions. Here, `rwx` means the **owner** can read, write, and execute. Owner of this file is `theunknownthing`.

  The second 3 characters (`r-x`) is the **group**'s permissions. Here, `r-x` means the **group** can read and execute, but not write. Group of this file is `staff`.

  The third 3 characters (`r-x`) is the permissions for others (everyone else). Again, `r-x` means they can read and execute, but not write.

---

To strengthen your understanding, let's take another example: `-rw-r--r--@   1 theunknownthing  staff   1.1K Sep  9 20:58 README.md`

You could interpret it yourself before you turn to the next page for the answer. Think:

- What type of file is it?
- What are the permissions for the owner? Why owner do not have execute permission?
- What are the permissions for the group?
- What are the permissions for others?

---

The first character is `-`, indicating it's a regular file.

The owner has `rw-` permissions, meaning they can read and write the file but cannot execute it (which is obvious, because it is a text file, you cannot run it).

The group has `r--` permissions, meaning the users in the `staff` group can view the contents of the file but cannot modify or execute it.

Others also have `r--` permissions, meaning they can only read the file as well.

---

## Changing Permissions with `chmod`

The chmod (change mode) command is used to change a file's permissions. You can do this in two common ways: **symbolic** or **octal notation**.

We would first learn the symbolic way, which is more intuitive.

This method uses letters (`u` for user (owner), `g` for group, `o` for others, `a` for all) and symbols (+ to add, - to remove, = to set) to modify permissions.

```bash
# Add execute permission for the owner
chmod u+x script.sh

# Set the permissions for others to be read-only
chmod o=r README.md

# Remove read permission for everyone except the owner, here `go` means `g` and `o`
chmod go-r README.md

# Remove ALL permissions for the group
chmod g= script.sh
```

---

## Octal Notation

This method uses numbers to represent the permissions for each category. It's a bit like binary! `r = 4, w = 2, x = 1`. And you add the numbers together for the permissions you want.

| Number | Permission | Meaning                         |
| ------ | ---------- | ------------------------------- |
| 7      | rwx        | Read, Write, and Execute, 4+2+1 |
| 6      | rw-        | Read and Write, 2+4             |
| 5      | r-x        | Read and Execute, 4+1           |
| 4      | r--        | Read only, 4                    |
| 0      | ---        | No permissions, 0               |

A `chmod` command with octal notation uses a 3-digit number representing the permissions for user, group, and others, in that order. To set permissions to rwxr-xr-x (user can do everything; group and others can read and execute), you would use the number 755.

```bash
chmod 755 script.sh
```

This would set 7 to the owner (rwx), 5 to the group (r-x), and 5 to others (r-x).

---

## Superuser Privileges with `sudo`

What happens when you need to do something that your normal user account isn't allowed to do, like install software or edit a system configuration file?

```bash
apt update
```

And you get the error:

```bash
Reading package lists... Done
E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)
E: Unable to lock directory /var/lib/apt/lists/
W: Problem unlinking the file /var/cache/apt/pkgcache.bin - RemoveCaches (13: Permission denied)
W: Problem unlinking the file /var/cache/apt/srcpkgcache.bin - RemoveCaches (13: Permission denied)
```

For that, you need administrator privileges. The sudo command lets you execute a **single command** as the superuser (root).

```bash
sudo apt update
```

> 🈲 The root user can do anything, including accidentally deleting your entire system. Double-check any command before you run it with sudo. You probably have seen some evil person to tell you execute `sudo rm -rf /*`. Don't do it!

---

If you want to login the root user yourself, you can use the `su` command (substitute user). It will ask for your password.

```bash
sudo su
```

It is basically doing the `su` command with `sudo`, and when there are no arguments given to `su`, it defaults to root user.

Of course, `su` is not limited to switching to root. You can switch to any user if you know their password.

```bash
su some_username
```

This will switch to `some_username` if you know their password or if your current user has higher permission then that user. So switching from root to any user does not require that user's password.
