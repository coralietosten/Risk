# Polyrisk

_Playing at Polytech is a risky business!_

---

## I. DIRECTORIES

The Risk project contains several source code files distributed into various directories for clarity:

### A. Directory `model`:  The Core Database

The directory `model` provides the description of the data model, i.e., the static part of the project:

**region**
:  There is defined the `Region` relation as a class, as well as associated data types for its extension.

**territory**
:  There is defined the `Territory` relation, basic part of a region.

**army**
:  There is defined the `Army` relation, including the pre-defined colour set.

**world**
:  There is defined the notion of a `World`.
It groups all the previous entities plus the adjacencies between territories.
This corresponds to the permanent facts.

**state**
:  There is defined a `State` of the game, i.e., any instantaneous situation between actions.
It is split up into:

* unchanging informations, i.e., the board and the fighting armies, a.k.a., the world, and
* evolving ones, i.e., the occupation of the territories by the armies, a.k.a., the actual state.

**state_informations**
:  There one can find a bunch of functions to examine the state of the world.
It would have been ugly to put them all into the interface of the `State` class!

**state_transitions**
:  There are defined the instantiations of the various transitions.
This is *not* to be used due to the exponential, or *only* quadratic, explosion!

_Nota._ The contents of this directory is *not* supposed to be modified in any way.
The only exception would be to add some missing functions in `state_informations`.

### B. Directory `strategy`:  The Extended Model

The directory `strategy` introduces the updating operations on a state, both the actual ones and the preparation steps:

**strategy**
:  There is defined an additional data structure that describes, in a functional way, the behaviour of any kind of player, from human to cyborgs to AIs.
Indeed, it is a mere tuple that groups together five functions and avoids to pass all or some of them individually to the functions that need them.
Their role is to decide in what way to conduct several operations, *not* to actually implement them on a state.

_Nota._ Although it is a class associated to `Army` only, the *signatures* of its functions reference `State` and `Territory` too.
Therefore, they introduce circular references.
These have been removed by using mere strings rather than actual types.
However, `mypy` and `pyright` complain with three errors.
They are not actual errors; the program runs without any issue.

**reinforcements**
:  There are defined several strategies in order to distribute new units over the territories already occupied by an army.
Some random ones are provided.

**attacks**
:  There are defined several strategies for an army to decide an attack from an occupied territory to a bordering territory belonging to another army with a given number of units.
Again a random attacking strategy is provided.

**defenses**
:  There are defined several strategies for the defender to answer to an attack.
A random defense and a maximal one are defined.

**invasions**
:  There are defined several strategies for invading a conquered territory.
Here, a random strategy plus two simple ones have been proposed.

**maneuvers**
:  There are defined several strategies for moving part of an army from an occupied territory to a bordering territory belonging to the same army.
Again, several random strategies are proposed.
As this is an optional step, no maneuvering is also provided.

**state_actions**
:  There are defined the three main operations, i.e., `do_reinforce`, `do_invade`, and `do_maneuver`, that *actually* generate a new state from an original one.
They merely apply the asked operations.
The game engine is to call them on behalf of the AIs, but through the overall game engine, not directly from them.

_Nota._ Should additional techniques be defined for the five main functions, they should preferably be declared respectively in the modules `reinforcements`, `attacks`, `defenses`, `invasions`, and `maneuvers`.
Alternatively, if the new AIs depart totally from this structure, it is advisable to isolate them in their own module.

### C. Directory `boards`:  A Partial Instantiation of the Model

The directory `board` extends the `model` one by providing _instances_ of the board games:

**polytech_board**
:  There is defined a localised, smaller variant of a Risk board for Polytech Nantes.
This is the place to be!

**classic_board**
:  There is defined the classic map of the game, for aficionados.
It can be interchanged in the imports of the main program, `polyrisk`.

**rendering**
:  There is defined a textual way to visualise a map with the colours of the occupying armies over the territories.
Usually this is not used unless one would like to visualise how AIs play a game!

_Nota._ The contents of this directory is *not* expected to be modified, not even red.

### D. Directory `ais`:  A Partial Instantiation of the Extended Model

The directory `ais` (should be names AIs if not for conventional naming) also extends the first one by providing _instances_ of the strategies, i.e., players.
We only consider fully automated players, though it would be possible to add the codes for a human player and even for cyborgs.

**neutrals**
:  There are defined losing AIs.
In the original rules of the game, they have to be used when there are only two active players.

**randoms**
:  There are defined dumb AIs.
They play by the rules of the game but have no strategy, though one is simply trying to distribute evenly its units over its territories.

### E. Directory `utilities`:  Miscellaneous

The directory `utilities` defines general functions that are not dedicated to this library:

**histogram**
:  This contains other utilities, dedicated to computing histograms.

**combinatorics**
:  There are defined a few dangerous functions that should not be used in the final project!

### F. Main Directory

The directory main directory contains some aside computations that have been conducted in order to highlight some aspects of the game.
They are not used during a game.
Currently, it is limited to determining the probabilities associated to battles:

**probabilities_single_battle**
:  This is a simple program that computes, once and for all, the probabilities of all the possible outcomes of the battles.

_Nota._ Looking here provides only a view on the computations that lead to the probability tables found in the description of the project.
However, it can be used in order to determine some other kinds of probabilities:  outcomes of long battles, losses of units, etc.

Of course, the main directory contains the full game itself, namely `polyrisk.py`.

---

## II. GLOSSARY

In the code, the names of the functions are quite explicit, i.e., lengthy and informative.
On the contrary, the names of the variables are kept short for brevity.
The glossary is as follows:

- r: a region
- t: a territory
- a: an army
- a: an attacker army
- d: a defendent army
- n: a number of unit
- n: a number of attacking unit
- m: a number of defending units
- u_a: the reinforcements units of the army a
- u_a: a number of unit for army a
- u_d: a number of unit for defending army d
- p_a: number of lost units for the attacker
- p_d: number of lost units for the defender
- g: a strategy
- s: a state
- t_a: the territory of an attacker
- t_d: the territory of a defender
- t_0: the starting territory of a maneuver
- t_1: the territory of arrival of a maneuver
- w: a world
- c: a colour
- r: a number of rounds
- r_max: the maximal number of rounds
- S: a list of states
- D: the set of adjacents territories
- R, f: a mapping of reinforcements
- A: a list of attacks and conclusions
- A: a list/set of attackers
- A: a set of armies
- T: a list/set of territories
- v: a value for a region
- T_a: the territories occupied by the army a
- R_a: the regions occupied by the army a
- R: a set of regions
- M: a set of maneuvers

Sometimes, a name is used with different meanings, but this is clear from the context.

---

## III. BUILDING AN AI

Looking at all the code is *not* necessary in order to build an AI.
All one needs to do is to add some functions, or files, in the `strategy` directory.
An AI is an instance of the `Strategy` class.
It has to be created by providing five functions, the ones present in the interface of the class.
They correspond to the decisions that an AI must take at each step:

* How an army should use a given number of new units over its territories?
* Should it attack an enemy territory, which one, from where, and with how many units?
* In the opposite way, when under attack, with how many units should it defend?
* In case of a successful battle that leads to victory, how many of its units should invade the newly occupied territory?
* Lastly, should some units from one of its territories move to another bordering one?

Providing decision procedures to these five questions is what constitute the strategy of an AI.
Everything else is ruled by the game engine.
For each of these functions, mostly random choices are provided in the corresponding modules, namely `reinforcements`, `attacks`, `defenses`, `invasions`, and `maneuvers`.
They have to be extended with new proposals!

---

## IV. ADDENDUM

### A. Dependencies

A circular dependency had to be broken.
Its is due to `typing`.
So, `mypy` or `pyright` return three similar ``errors'' where the class `Strategy` is undefined.
This is not an actual error.

_Nota._ Using `future annotations` *does* create a circular dependency error at run-time.

### B. Tests

The game framework has *not* been fully and thouroughly tested.
However, the proposed AIs have been playing together for several games.
Since pre- and post-conditions are spread all over the code, naïve bugs should be absent.

_Nota._ Pre- and post-conditions are often repeated in various places to catch possible errors as soon as possible.
This is especially true for functions that have to be used as models.
This should prove useful to the programmer.

_Nota._ Remember that in order to run the code without checking all these assertions, one has to use the `-O` option.
This is slightly more than twice faster.

---

## V. RUN

Running the program is set to animation mode in the source code.
Simply:

* open an ANSI console, 
* enlarge it in full-screen mode, and
* type in the following command line:
    
    ```shell
    python -O polyrisk.py
    ```

Enjoy the animation! (Not too often...)
