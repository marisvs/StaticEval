import subprocess
import time
import chess.pgn
import json
from bokeh.io import output_file, show, save
from bokeh.layouts import column
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool, Span

engine = subprocess.Popen(
    '../engine/stockfish 7 x64.exe',
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    bufsize=1
)

trace = False

def get_column(matrix, i):
    '''
    Extract column i from matrix
    Input: matrix is a 2D list, i is an integer
    Output: list
    Comment: perhaps to be replace by a more solid routine from numpy
    '''
    return [row[i] for row in matrix]

def put(command):
    if trace == True:
        print('\nPut: '+command)
    engine.stdin.write(command+'\n')

def get():
    # using the 'isready' command (engine has to answer 'readyok')
    # to indicate current last line of stdout
    output = []
    engine.stdin.write('isready\n')
    if trace == True:
        print('\nGet: ')
    while True:
        text = engine.stdout.readline().rstrip()
        #print(text)
        if text == 'readyok':
            break
        if text !='':
            if trace == True:
                print(text)
        output += [text]
    return output

def exec_engine(command):
    put(command)
    return get()

def init_engine():
    output = get()
    put('uci')
    output += get()
    # possibly some additional options:
    # put('setoption name Hash value 128')
    # get()
    return output

EvalHeader = [
    'Move', 'Material Total MG', 'Material Total EG',
    'Imbalance Total MG', 'Imbalance Total MG',
    'Pawns Total MG', 'Pawns Total MG',
    'Knights White MG', 'Knights White EG', 'Knights Black MG', 'Knights Black EG',  'Knights Total MG', 'Knights Total EG',
    'Bishops White MG', 'Bishops White EG', 'Bishops Black MG', 'Bishops Black EG',  'Bishops Total MG', 'Bishops Total EG',
    'Rooks White MG', 'Rooks White EG', 'Rooks Black MG', 'Rooks Black EG',  'Rooks Total MG', 'Rooks Total EG',
    'Queens White MG', 'Queens White EG', 'Queens Black MG', 'Queens Black EG',  'Queens Total MG', 'Queens Total EG',
    'Mobility White MG', 'Mobility White EG', 'Mobility Black MG', 'Mobility Black EG',  'Mobility Total MG', 'Mobility Total EG',
    'King Safety White MG', 'King Safety White EG', 'King Safety Black MG', 'King Safety Black EG',  'King Safety Total MG', 'King Safety Total EG',
    'Threats White MG', 'Threats White EG', 'Threats Black MG', 'Threats Black EG',  'Threats Total MG', 'Threats Total EG',
    'Passed Pawns White MG', 'Passed Pawns White EG', 'Passed Pawns Black MG', 'Passed Pawns Black EG',  'Passed Pawns Total MG', 'Passed Pawns Total EG',
    'Space White MG', 'Space White EG', 'Space Black MG', 'Space Black EG',  'Space Total MG', 'Space Total EG',
    'Total MG', 'Total EG', 'Total'
    ]
    
    
def static_eval(mode, info, phase):
    '''
    Execute an uci.eval command and captures and processes its output.
    The evaluation is a static evaluation so without search.

    Input: mode: FEN   -> info must be a FEN string
                 start -> info contains the list of uci moves from the starting position
           phase: is MG, EG, XG where XG is the mixed value of MG and EG

    Output: list of floats containing all evaluations. Headers are contained in variable EvalHeader

    Details:
    OUTPUT from uci command eval:
     0123456789012345678901234567890123456789012345678901234567890
    0    Eval term |    White    |    Black    |    Total
    1              |   MG    EG  |   MG    EG  |   MG    EG
    2--------------+-------------+-------------+-------------
    3     Material |   ---   --- |   ---   --- |  1.07  1.02
    4    Imbalance |   ---   --- |   ---   --- | -0.36 -0.36
    5        Pawns |   ---   --- |   ---   --- |  0.23  0.39
    6      Knights |  0.16  0.04 |  0.00  0.00 |  0.16  0.04
    7       Bishop | -0.12 -0.19 | -0.10 -0.22 | -0.02  0.03
    8        Rooks |  0.17  0.08 |  0.17  0.08 |  0.00  0.00
    9       Queens |  0.00  0.00 |  0.00  0.00 |  0.00  0.00
    0     Mobility |  0.63  1.60 |  0.59  1.39 |  0.03  0.22
    1  King safety |  0.74 -0.06 | -0.02 -0.12 |  0.77  0.06
    2      Threats |  0.31  0.31 |  0.36  0.40 | -0.05 -0.09
    3 Passed pawns |  0.00  0.00 |  0.00  0.00 |  0.00  0.00
    4        Space |  0.15  0.00 |  0.09  0.00 |  0.06  0.00
    5--------------+-------------+-------------+-------------
    6        Total |   ---   --- |   ---   --- |  1.90  1.28
    7
    8Total Evaluation: 1.70 (white side)
    '''

    def phi (info):
        '''
        phi uses total evaluation values to determine the game phase (=phi)
        input: info : [Total, Total MG, Total EG]
        comment:
        > pay attention to when MG=EG: avoid division by zero
        > assumption is that all scores can be treated this way
        '''
        if info[1] == info[2]:
            return 0
        else:
            return (info[0]-info[1]) / (info[2]-info[1])
    
    def mg_eg (info):
        '''
        phase uses MG and EG values to determine the value for a particular game phase
        input: info : [phi, MG_value, EG_value]
        '''
        return info[1] + info[0]*(info[2]-info[1])
    
    if mode == 'FEN':
        exec_engine('position fen ' + info)
    else:
        #mode == 'start':
        exec_engine('position startpos moves' + info)
    evaluation = exec_engine('eval')
    results = []
    for i in range(3,6):
        results += evaluation[i].split('|')[3].split()
    for i in range(6,15):
        for j in range(1,4):
            results += evaluation[i].split('|')[j].split()
    results += evaluation[16].split('|')[3].split()
    results += [evaluation[18].split()[2]]    # no '|'
    results = [float(x) for x in results]
  
    #print (results, end='==')
    if phase == 'XG':
        # replace all MG and EG values by the mg_eg value
        phi0 = (phi([results[-1], results[-3], results[-2]]))
        results = [mg_eg([phi0, results[i], results[i+1]]) for i in range(0,len(results)-1,2)]
    #print (results)
    
    return results

def open_pgn(file_name):
    '''
    Open a pgn file so that games can be read from it

    Input: file name of pgn file
 
    Output: pgn_file_descriptor
    ''' 
    return open(file_name, 'r', encoding='utf-8-sig', errors='surrogateescape')

def read_pgn(f):
    '''
    Read the next game from an open pgn file

    Input: pgn_file_descriptor

    Output: game which is of class 'chess.pgn.Game'
    ''' 
    return chess.pgn.read_game(f)

def close_pgn(f):
    '''
    Close the pgn file

    Input: pgn_file_descriptor

    Output: None
    '''
    f.close()
    
def static_eval_pgn(game):
    '''
    Perform for every ply a static evaluation of a game

    Input: game as read by read_pgn() is of class 'chess.pgn.Game'

    Output: matrix of evaluation values per ply
    Example for first row (=first ply after starting position):
    ['1. e4', 0.11, -0.0, 0.0, 0.0, -0.02, -0.01, 0.12, 0.0, 0.12, 0.0, 0.0, 0.0,
    -0.12, -0.37, -0.12, -0.37, 0.0, 0.0, -0.27, 0.0, -0.27, 0.0, 0.0, 0.0, 0.0,
    0.0,0.0, 0.0, 0.0, 0.0, -0.19, -0.21, -0.73, -0.84, 0.55, 0.63, 0.93, -0.06,
    0.93, -0.06, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 0.45, 0.0, 0.27, 0.0, 0.18, 0.0, 0.82, 0.65, 0.74]

    Comment: command sent to the engine is built up from the starting position
    including all subsequent moves.
    '''
    output = []
    uci_moves = ''
    node = game
    while not node.is_end():
        next_node = node.variation(0)
        move_notation = str(node.board().fullmove_number) + '. '
        if node.board().turn == chess.BLACK:
            move_notation += '... '
        move_notation += node.board().san(next_node.move)
        uci_moves += ' '+node.board().uci(next_node.move)
        scores = static_eval('start', uci_moves, 'MG EG')
        scores.insert(0, move_notation)
        output.append(scores)
        node = next_node
    return output

def plot_scores(mode, matrix, game):
    '''
    Use bokeh plots to plot a line chart for the selected field
    
    Input:
        mode: save to save the html files, show to show the files in the browser
        matrix: matrix output from static_eval_pgn
        game: all game information read from pgn file
       
    Output:
        html file created with name: "[white player]-[black player] [year].html"
        plot contains multiple subplots for the different score elements
        file is automatically displayed (and saved) in default browser
    '''

    def sub_plot(title_text, fields):
        if title_text=='Total':
            sp_title = game_id+'  '+game.headers['Result']
        else:
            sp_title = title_text
        entries = [EvalHeader.index(i) for i in fields]
        sp = figure(
            #y_range=(-6, 6),
            background_fill_color='#DFDFE5',
            width=1000, plot_height=250,
            title=sp_title,
            x_axis_label='ply', y_axis_label='score',
            tools=tools_to_show)
        sp.ygrid.grid_line_color = 'white'
        sp.title.text_font_size = '20px'
        hline = Span(location=0, dimension='width', line_color='darkgrey', line_width=2)
        sp.add_layout(hline)    # make the level 0 better visible
        e = 0
        for entry in entries:
            source = ColumnDataSource(  # just needed to get the tooltip contents about the move
                data=dict(
                    x=list(range(1, plies+1)),
                    y=get_column(matrix, entry),
                    info=get_column(matrix, 0))
                )
            if 'Black' in EvalHeader[entry]:
                kleur_circle = 'black'
                kleur_line = 'black'
            elif 'White' in EvalHeader[entry]:
                kleur_circle = 'white'
                kleur_line = 'black'
            else:
                kleur_circle = 'darkblue'
                kleur_line = 'darkblue'
            if ('MG' in EvalHeader[entry]) or (title_text=='Total'):
                dash_type='solid'
            else:
                dash_type='dotted'
            sp.line(
                list(range(1, plies+1)),
                get_column(matrix, entry),
                source=source,
                color='darkgrey',
                line_width=1,
                line_dash=dash_type)
            sp.circle(
                list(range(1, plies+1)),
                get_column(matrix, entry),
                source=source,
                size=6,
                fill_color=kleur_circle,
                line_color=kleur_line)
            e += 1
        hover = sp.select(dict(type=HoverTool))
        hover.tooltips = {"score":"@y{1.11}", "move":"@info"}
        hover.line_policy='nearest'
        #hover.mode = 'mouse'    # doesn't seem to do anything
        return sp

    plies = len(matrix)
    game_id = game.headers['White']+'-'+game.headers['Black']+' ('+game.headers['Date'][0:4]+')'
    output_file(
        '../results/'+game_id+'.html',
        title=game_id)
    tools_to_show = 'hover, box_zoom, pan, reset, wheel_zoom'
    p = []
    p += [sub_plot('Total', ['Total'])]
    p += [sub_plot('Material', ['Material Total MG', 'Material Total EG'])]
    p += [sub_plot('Imbalance', ['Imbalance Total MG', 'Imbalance Total MG'])]
    p += [sub_plot('Pawns', ['Pawns Total MG', 'Pawns Total MG'])]
    p += [sub_plot('Knights', ['Knights White MG', 'Knights White EG', 'Knights Black MG', 'Knights Black EG'])]
    p += [sub_plot('Bishops', ['Bishops White MG', 'Bishops White EG', 'Bishops Black MG','Bishops Black EG'])]
    p += [sub_plot('Rooks', ['Rooks White MG', 'Rooks White EG', 'Rooks Black MG', 'Rooks Black EG'])]
    p += [sub_plot('Queens', ['Queens White MG', 'Queens White EG', 'Queens Black MG', 'Queens Black EG'])]
    p += [sub_plot('King Safety', ['King Safety White MG', 'King Safety White EG', 'King Safety Black MG','King Safety Black EG'])]
    p += [sub_plot('Space', ['Space White MG', 'Space White EG', 'Space Black MG', 'Space Black EG'])]
    p += [sub_plot('Mobility', ['Mobility White MG', 'Mobility White EG', 'Mobility Black MG', 'Mobility Black EG'])]
    p += [sub_plot('Threats', ['Threats White MG', 'Threats White EG', 'Threats Black MG', 'Threats Black EG'])]
    p += [sub_plot('Passed Pawns', ['Passed Pawns White MG', 'Passed Pawns White EG', 'Passed Pawns Black MG', 'Passed Pawns Black EG'])]
    if mode=='show':
        show(column(*p))
    elif mode=='save':
        save(column(*p))
    else:
        print ('unknown plot mode', mode)
    
def print_scores(field_name, data, game):
    '''
    Print moves and scores in a long list for the selected field
    Input:
       field_name: list of selected fields,
       data: matrix output from static_eval_pgn
       game: all game information read from pgn file
    
    Output: list of moves and scores on stdout
    '''
    print (game.headers)
    header = 'Move'
    for name in field_name:
        header += ' '+name
    print (header)
    entries = [EvalHeader.index(i) for i in field_name]
    for eval in evaluations:
        print (eval[0].ljust(15), end=' ')
        for entry in entries:
            print (eval[entry], end=' ')
        print ()
    print (evaluations[-1][0])

def plot_pgn (mode, pgn_file):
    exec_engine('ucinewgame')
    f = open_pgn(pgn_file)
    game = read_pgn(f)
    while game:
        print(game.headers['White']+'-'+game.headers['Black']+' ('+game.headers['Date'][0:4]+')')
        evaluations = static_eval_pgn(game)
        plot_scores(mode, evaluations, game)
        game = read_pgn(f)
    close_pgn(f)
    
init_engine()
plot_pgn('save', '../games/Diagonal.pgn')
put('quit') # don't wait for output

