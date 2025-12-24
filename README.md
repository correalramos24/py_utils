# py_utils
Python utils collection, on my own style.

For sure most of the utils here exists as standalone-packages, but is fun to
have something self-build :).

## Utilites

* bashCMD: Launch & manage Bash commands.
* bashScript: Set and Launch bash scripts. Sits on the top of bashCMD.
* gitProject: Gather Git information of a Path.
* logger: My simply logger.
* meta: MetaClass to compend all the utilites for all the object definitions.
* controllers: 3-layers controllers definitions, using logger and other stuff.
* utils_py: Collection of methods to shortcut stuff. 


## Environment

The env.bash file contains all the required functions to work with
the virutal environment and the testing. All the dependencies are in the *requirements.txt* file

### Testing

Unit testing for the utilites is built using **unittest**. You can run the tests using ``python -m unittest discover -s tests`` or the bash function ``launch_tests``.
