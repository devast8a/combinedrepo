# combinedrepo
Tool to manage a large number of git repositories being merged into a single large repository with git subtree.

# Getting started

Say, you have two repositories. `stuff` and `things`.

```
$ ls -R
.:
stuff/  things/

./stuff:
cool-stuff.txt  hello.txt  not-cool-stuff.txt

./things:
directory_of_things/  list_of_things.md

./things/directory_of_things:
cats  dogs  doors  tables
```

Create a new repository called repo, and give it a new commit

```
$ git init repo
$ cd repo
$ git commit --alow-empty -m "Initial Commit"
$ cd ..
```

Initialize a combined repository

```
$ combinedrepo init repo
```

To add a repository use the add command, it will push the CURRENT
working directory to the combined repository. The parameter is the
path you want the repository to have in the combined repository.

```
$ cd test
$ combinedrepo add everything/only_things
$ cd ../
$ cd stuff
$ combinedrepo add everything/stuff
$ cd ../
```

combinedrepo (using git subtree) has added all our files into our repository for us.
Everything from `things` is copied into `everything/only_things`, `stuff` copied into `everything/stuff`

```
$ cd repo
$ ls -R

.:
everything/

./everything:
only_things/  stuff/

./everything/only_things:
directory_of_things/  list_of_things.md

./everything/only_things/directory_of_things:
cats  dogs  doors  tables

./everything/stuff:
cool-stuff.txt  not-cool-stuff.txt
```

More importantly, our git history has been merged into repo too.

```
$ git log --pretty=oneline --graph --all
*   aa8522904c2417f49a3808a95da0aafde7ad1dbf Add 'everything/stuff/' from commit '8385c3533472e3ee1c7b8e90c68c807cb7454751'
|\
| * 8385c3533472e3ee1c7b8e90c68c807cb7454751 Commit all my stuff
*   0f1315c4608fde45851066550c628bc8d4145a45 Add 'everything/only_things/' from commit '9a109aa395036283e42881cd9e28fcc420ee6595'
|\
| * 9a109aa395036283e42881cd9e28fcc420ee6595 Add furniture to directory of things
| * 31a07a85dac1522dc4881ae54543b0ed7f63e805 Lists of things are nice
| * 83e920576c6556eaf1b4ebf45628677e5e5d15b8 Add some pets to directory of things
* a3229ddf61b42f6a0a569654b0ad1f74a98a9e0f Initial Commit
```

If you make some changes in the `things` repository, you can commit those changes then use combined repo to push those changes.

```
$ cd ../stuff
$ combinedrepo push
```

Better management functions and the ability to pull changes comming soon(tm).

# License
Licensed under the MIT License, refer to LICENSE.md for more information.
