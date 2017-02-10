### Overview

Imagine that you, as a chess player, can ask the computer about chess: to understand a position, to hear what the refutation is of a particular move, to learn with guided hints, to learn positional and strategic features, to learn about plans. To have a program that can explain why a move was played, in human understandable terms. Why is this not yet possible?

In 1997 Deep Blue settled the question whether computers could play chess strong enough to beat the world champion. Since then the chess battle between men and computer is over and the strongest engines are too strong to leave the world champion any hope for a win.
Continued development on hardware and software has made chess engines unbeatable for humans but less progress has been made in transfering this superior playing skills to human players.

Of course, computers play chess in a different way, but why are they not able to communicate more about a position than just the evaluation: a single numeric value.

Hence the goal of the *Cognitive Chess* project:
*Develop programs that help human players improve their skills, that can communicate in human understandable terms about chess*


### Steps towards the goal

Above goal cannot be reached with just a single program, so it is expected that multiple sub projects are developed to deliver small pieces of functionality and when combined, one day, the goal is reached.

The following sub projects are envisaged:
* Modify and/or expand an existing chess engine in any way that is deemed useful. Use it to better understand how a computer engine differs from a human player, for instance, in evaluating a position. Another option is to output the searchtree and use it.
For this purpose [Stockfish] (https://github.com/official-stockfish/Stockfish) is ideal: the strongest engine and open source.
* Visualize static evaluations during a game, especially of a game with a clear positional element such as a open diagonal.
* Create and visualize searchtrees. Chess engines are capable to calculate a million positions per second so the searchtree explodes very quickly. But how does a tree look like, can we learn anything?
* Search trees contain the raw data about why a move is good or bad. What if we extract information from this tree data, condensing it enormously. What information could be extracted?
* How about we use this information to feed a chatbot? Could a chess chatbot be built that is able to convey this information?
* How about training a neural with positional and strategic features more close to how human players think about chess?


### This project is about Visualization of Static Evaluation

For more details see the [Manual] (Manual.md)


### Terms of use

Stockfish is free, and distributed under the **GNU General Public License**
(GPL). Essentially, this means that you are free to do almost exactly
what you want with the program, including distributing it among your
friends, making it available for download from your web site, selling
it (either by itself or as part of some bigger software package), or
using it as the starting point for a software project of your own.

The only real limitation is that whenever you distribute Stockfish in
some way, you must always include the full source code, or a pointer
to where the source code can be found. If you make any changes to the
source code, these changes must also be made available under the GPL.

