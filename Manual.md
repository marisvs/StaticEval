### Static Evaluation

#### Background
The program CreateStaticEvalGraphs.py executes the following steps:
1. start up a stockfish engine
2. open a pgn file
3. reads a game from the pgn file
4. executes the uci command ‘eval’ after every ply (move of each player, so 1 move = 2 plies)
  a. this gives a static evaluation so without any tree search.
  b. it gives scores for a number of categories e.g. ‘material’, ‘king safety’, ‘knight’, etc
5. it creates a html file with plots for every category showing how it developed at each ply
6. it repeats this for every game in the pgn file

*Example game*
`[Event "DDR-POL"]`
`[Site "DDR"]`
`[Date "1977.??.??"]`
`[Round "?"]`
`[White "Vogt, Lothar"]`
`[Black "Bielczyk, Jacek"]`
`[Result "1-0"]`
`[ECO "B67"]`
`[Annotator "Van Voorthuijsen,Peewee"]`
`[PlyCount "83"]`
`[EventDate "1977.??.??"]`
`[EventType "team-match"]`
`[EventRounds "2"]`
`[EventCountry "DDR"]`
`[SourceTitle "EXT 2010"]`
`[Source "ChessBase"]`
`[SourceDate "2009.11.30"]`

1. e4 c5 2. Nf3 Nc6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 d6 6. Bg5 e6 7. Qd2 a6 8.
O-O-O Bd7 9. f4 b5 10. Bxf6 gxf6 11. Kb1 Qb6 12. Nxc6 Bxc6 13. Bd3 Qc5 14. Rhf1
O-O-O 15. f5 d5 16. exd5 exd5 17. Be4 Bd6 18. Nxd5 Bxd5 19. Bxd5 {Diagram [#]}
Bxh2 20. Rf3 Be5 21. Rd3 Rd6 22. Bxf7 Rhd8 23. Bd5 Kb8 24. g4 h6 25. Bh1 Ka7
26. Qg2 Qc7 27. Rc1 Rd4 28. Rxd4 Rxd4 29. c3 Rd8 30. Qe4 Qb6 31. Bf3 a5 32. Rh1
b4 33. c4 b3 34. a3 a4 35. g5 Bxb2 36. c5 Qb5 37. Kxb2 Re8 38. Qd4 Re2+ 39. Kb1
Re5 40. c6+ Ka6 41. c7 Re8 42. Qxf6+ 1-0

#### Legend
There are several plots, depending on which score category is plotted.
In general the following remarks apply:
*	Horizontal axis is ply, so odd plies are for white, even for black
*	Vertical axis displays the score in pawns. Beware that the y-axis scales automatically and scales differ.
*	Tools are available at the right hand side. Activate the one that might be useful for you (eg zoom in)
*	Positioning the mouse at a marker shows both the played move and the score after the move in a small pop up window.

*White and black aggregation plots*
![alt-text] (results/Total_score.png)
*	Dots are in darkblue
*	Quantity that is already a sum of white and black positions
  *	Example 1: Material. the plot displays the material difference for white and black.
  *	Example 2: Total score: addition of all categories together
  *	Positive values are in favor for white, negative for black 
  *	Example plot is the first plot in a file which shows the Total score.
  *	Title of the plot shows the players and the game result

*	Most categories have separate values for middlegame and for endgame.
  *	This is shown in chart by the line that connects the markers. A solid line refers to middlegame scores and a dotted line refers to endgame scores.

*Plots with separate markers for white and black*
All other plots show both values for white and black at the same time
*	White circles are scores for the white player, black circles for the black player.
*	The scores are seen from the perspective of each player (so a positive score is good for them).
![alt-text] (results/Bishops.png) 
*	The endgames scores are indicated by the dotted lines between markers)
*	Stockfish determines a final value based on the middle game score, end game score and game phase (which is a function of the total material present on the board). It does this only for the final Total score but not for the different categories.
