# Makefile
This readme will contain the naming conventions, terminologies and tutorials on how to build a Makefile
___
## About ___make___
___make___ is a tool which can run commands to read files, process these files in some way, and write out the processed files. For example, in software development, Make is used to compile source code into executable programs or libraries. The idea is to make results easier to reproduce. <br>
It is used for automating the execution of files. It makes sure that you don't do repetitive stuff everytime i.e., creating data which was already existing. Make ensures that only the required files are recompiled when you make changes to your source files. It checks what is out of data and builds only those parts.Make handles dependencies which are described in Makefile. Makefile is kind of a ***build.sh*** file for build manager describing rules and dependencies.
<br></br>

## Structure of Makefile
```
rules
targets
dependencies
actions
```
Together targets, dependencies, and actions make rules.
It consists of targets which help to modularize and well as tell which part of your task needs to be executed. You also tell which part of your program depends upon which part. When you update some part of the program, it only rebuilds the parts that depend on that.
<br></br>
It does a topological sort and has a tree-like structure determining what dependency need to be built before what. Make checks the ‘last modification time’ of both the target and its dependencies. If any dependency has been updated since the target, then the actions are re-run to update the target
<br></br>

You can run Makefile for a specific task as well as ignoring other tasks based upon the target set up in the file itself.

```
all: 
    cc -o test test.c
```

> make all

 command will execute only the all target. It first creates an executable test which can be used as executable to run test.c
<br></br>

### Commands
We can rename our Makefile to be something else and it can be executed as follows:

> $ make -f MyOtherMakefile


By default, make command looks for Makeflle and will run it. Also, the first target is the default target in Makefile. For enforcing others, you have to explicitly mention the target

Suppose, we made a change to a file and just want to see which files will be executed by make without actually executing them

> $ make -n dats

<br></br>

### Variables
* **#@** is a Make automatic variable which means target of the current rule. Target filenames can be used for variable names.
* **#^** is a Make automatic variable which means dependency of the current rule. Dependency filenames can be used for variable names. 
* **#<** is a Make automatic variable which means first dependency of the current rule. Dependency filenames can be used for variable names if we just want to mention the first dependency only in the action.
<br></br>
### Pattern rules
Wildcards * can be used for prototyping commands. **$*** can be used for addressing multiple files as well.
<br></br>

### Functions
They can be used for complex operations. For example, *.txt can be used for listing all the files in a directory and save it in a variable.

> TXT_FILES=$(wildcard books/*.txt)
<br></br>

### Documentation
Documentation of Makefile can also be done which can help in giving a brief about Makefile. It is executed as 

> make help


**##** comments should be declared above each rule and defined in help rule
```
.PHONY : help
help : Makefile
        @sed -n 's/^##//p' $<
```

<br></br>

**pathsubst**
> DAT_FILES=$(patsubst books/*.txt, %.dat, $(TXT_FILES))

If you have a hierarchy of folders for several files and they follow fixed pattern, it can be used for generating list of files and save it to a variable name.
<br></br>

***Note:***

* .PHONY is used to mark some targets. If we define a rule in which target name doesn't have a dependency and the target name happens to be a directory, then after invoking make target it won't generate the data as it sees that the directory is already existing and it doesn't have any dependency as well. Therefore, we assign a tag PHONY to the target. 
* Sometimes suffix .mk  is used for Makefile as well
* Make variables are sometimes also called as macro