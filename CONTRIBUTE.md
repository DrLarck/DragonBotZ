## Contribute
Welcome to this short **contribution** guide. After reading it, you should be ready to contribute to this project !

If you have any other question, please contact [@DrLarck](https://github.com/DrLarck).

## Some requirements
First of all, you need to respect the [PEP 8](https://www.python.org/dev/peps/pep-0008/#introduction) coding convention.
Any code that violates this convention won't be merged.

Once you've read the **PEP 8** convention, you may need to install the required libraries. To do so, type the following command in your **terminal** :
```
$pip install -r requirements.txt
```

## Adding some code
To add your code to the project, use the **branch** feature rather than developing on **master**.

You are free to **fork** the project or directly create a **new branch**.

By the way, respect the **purpose** of your branch, stick to your planed changes and do not spread too much to avoid conflicts.

For example : *If I create a new branch to add some characters ; I will only **ADD** new code and not **EDIT** existing one. If I want to edit existing code, I create a new branch OR I open a new **issue** to ask for changes.*

Do not push **non-tested** code.

## Versioning
The versioning system is a little bit tricky, you're not forced to update the version, when the code is merged with **master**, the owner will update the version for the production.

But let me explain how it works : 
- The versioning break it down as following : **{PHASE}** - v **{MAJOR}**.**{MEDIUM}**.**{MINOR}**.**{CHANGES}**

    - **PHASE** : Represents the current project phase (**Prototype**, **ALPHA**, **BETA**, **Release**, **Stable**).
    - **MAJOR** : Represents a major change which is incompatible with the previous version such as a whole code rework, new gameplay, etc.
    - **MEDIUM** : Represents a medium change, like a new feature, etc.
    - **MINOR** : Represents minor changes such as patches, bug fix, etc.
    - **CHANGEs** : Represents file changes, this value increases each time a file is changed. 