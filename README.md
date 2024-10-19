# DUmmy

This is the repo where all my practice files are going to be kept. I usually write some helpful functions/modules when practicing and they get removed or stays in 1 hard drive which gets annoying. This is to save those helpful functions.


## Folder Structure.

This is an example structure. It is not mandatory or recommended to follow the exact name, but it is mandatory to follow this structure.

```
DUmmy/
│
├── Language/
│   ├── env/
│   ├── main.*
│   ├── run.*
│   ├── projects/
│   │   ├── main.*
│   ├── modules/
│   │   ├── module
│   │   │   ├── main.*
│
├── tests/
```

### Difference between main and run 
`main.*` is the entry point for our project. This is mainly for writing some quick code to test. But you might forget to remove this before doing commit. As such, if there is any possibility of commit, use `run.*` instead as this is in the `.gitignore` file. At the same time, as `run.*` is in the `.gitignore` file you have to create it yourself if this is a new clone of the project/
