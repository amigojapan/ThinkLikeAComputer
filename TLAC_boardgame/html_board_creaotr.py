#!/usr/bin/python3
import sys
def main(level):
    header = """
<html>
    <head>
        <title>HTML output</title>
    </head>
    <style>
    body {
            font-family: "Courier New", Courier, monospace;
        }
    .cell-div {
      font-family: Courier;
      display: inline;
      width: 300px;
    }
    </style>
    <body>
"""
    width_and_height="32"
    body=""
    level=level.replace("[#]", "<div class='cell-div'><img src='https://raw.githubusercontent.com/amigojapan/ThinkLikeAComputer/refs/heads/main/TLAC_boardgame/img/wall.png' width="+width_and_height+" height="+width_and_height+"></div>")
    level=level.replace("[^]", "<div class='cell-div'><img src='https://raw.githubusercontent.com/amigojapan/ThinkLikeAComputer/refs/heads/main/TLAC_boardgame/img/turtule_up.png' width="+width_and_height+" height="+width_and_height+"></div>")
    level=level.replace("[V]", "<div class='cell-div'><img src='https://raw.githubusercontent.com/amigojapan/ThinkLikeAComputer/refs/heads/main/TLAC_boardgame/img/turtule_down.png' width="+width_and_height+" height="+width_and_height+"></div>")
    level=level.replace("[<]", "<div class='cell-div'><img src='https://raw.githubusercontent.com/amigojapan/ThinkLikeAComputer/refs/heads/main/TLAC_boardgame/img/turtule_left.png' width="+width_and_height+" height="+width_and_height+"></div>")
    level=level.replace("[>]", "<div class='cell-div'><img src='https://raw.githubusercontent.com/amigojapan/ThinkLikeAComputer/refs/heads/main/TLAC_boardgame/img/turtule_right.png' width="+width_and_height+" height="+width_and_height+"></div>")
    level=level.replace("[ ]", "<div class='cell-div'><img src='https://raw.githubusercontent.com/amigojapan/ThinkLikeAComputer/refs/heads/main/TLAC_boardgame/img/board_empty_slot.png'  width="+width_and_height+" height="+width_and_height+"></div>")
    level=level.replace("[G]", "<div class='cell-div'><img src='https://raw.githubusercontent.com/amigojapan/ThinkLikeAComputer/refs/heads/main/TLAC_boardgame/img/goal.png' width="+width_and_height+" height="+width_and_height+"></div>")
    level=level.replace("[*]", "<div class='cell-div'><img src='https://raw.githubusercontent.com/amigojapan/ThinkLikeAComputer/refs/heads/main/TLAC_boardgame/img/star.png' width="+width_and_height+" height="+width_and_height+"></div>")
    level=level.replace("[o]", "<div class='cell-div'><img src='https://raw.githubusercontent.com/amigojapan/ThinkLikeAComputer/refs/heads/main/TLAC_boardgame/img/egg.png' width="+width_and_height+" height="+width_and_height+"></div>")
    level=level.replace("\n", "<BR>\n")
    #make spaces into HTML spaces
    level=level.replace(" ", "&nbsp")    
    #set HTML elements back to normal
    level=level.replace("<div&nbspclass='cell-div'>", "<div class='cell-div'>")    
    level=level.replace("<img&nbspsrc=", "<img src=")    
    level=level.replace("'&nbsp&nbspwidth=", "'  width=")    
    level=level.replace("&nbspheight=", " height=")    
    body=level
    footer = """
    </body>
</html>"""
    print(header, level, footer)

if '__main__' == __name__:
    #example how to call this program:
    #cat ../problem7-output.txt | python3 html_board_creaotr.py  > problem7test.html
    separator = ""#empty separator
    result_string = separator.join(sys.stdin)
    main(result_string)

#(done, changed all the backrounds of every piece) maybe change backround color of turtle to same as groud