###############################################################################
###############################################################################
##                                                                           ##
##  THATCHORD BY TOM CONTI-LESLIE                                 errors.py  ##
##                                                                           ##
##  This file should be loaded by most other files and contains all error    ##
##  messages that can be returned by various files.                          ##
##                                                                           ##
##                                                                           ##
##  License: CC BY-SA 4.0                                                    ##
##                                                                           ##
##  Contact: tom (dot) contileslie (at) gmail (dot) com                      ##
##                                                                           ##
###############################################################################
###############################################################################

class ChordError(Exception):
    pass

def err(reason):
    
    # REASON 1: INVALID INPUT
    if reason == "input" or reason == 1:
        out = """Invalid chord structure: try a chord of the form """         \
            + """WXYZ", where:\n- W is a letter A-G possibly followed """     \
            + """by "b"or "#";\n- (optional) X is a chord quality, e.g. """   \
            + """"m", "add9", "dim7", ...\n- (optional) Y is a set of """     \
            + """altered notes in parentheses, e.g. "(b7)" or "(#7b13)";\n""" \
            + """- (optional) Z is a bass note, e.g. "/D#"."""
        raise ChordError(out)
    
    # REASON 2: INVALID ALTERATION NUMBER
    if reason == "alteration" or reason == 2:
        out = """Invalid alteration: you can alter the numbers 1, 2, 3, 4, """\
            + """5, 6, 7, 9, 11, 13 only."""
        raise ChordError(out)
    
    # REASON 3: UNRECOGNISED CHORD QUALITY
    if reason == "quality" or reason == 3:
        import dicts
        out = """Unrecognised chord quality. Currently supported chord """    \
            + """qualities are: """ + str(list(dicts.qualities.keys()))       \
            + """. These  are case-sensitive. You can also put alterations """\
            + """in parentheses."""
        raise ChordError(out)
        
    # REASON 4 (FERMAT'S ERROR): MARGIN TOO SMALL TO PRINT LINE NUMBER
    if reason == "fermat" or reason == 4:
        out = """In attempting to print a chord, one line number to be """    \
            + """displayed was too long compared to the default margin size"""\
            + """. Ensure ThatChord is not printing chords absurdly high """  \
            + """on the fretboard, and that the margin is defined to be """   \
            + """suitably large (ideally 3 or more; at least 1)."""
        raise ChordError(out)
    
    # REASON 5: TOO FEW FRETS FOR ANY POSSIBILITIES
    if reason == "frets" or reason == 5:
        out = """The number of frets is too low for one of your """           \
            + """instrument strings to have any valid positions. Try """      \
            + """changing the number of frets, changing the chord, or """     \
            + """allowing more muted strings."""
        raise ChordError(out)
        
    # REASON 6: NO CHORDS FOUND
    if reason == "nosols" or reason == 6:
        out = """There are no ways of playing the requested chord on this """ \
            + """instrument, though your chord was correctly understood. """  \
            + """Try increasing the number of frets or reducing the number """\
            + """of important notes."""
        raise ChordError(out)
    
    # REASON 7: INVALID INPUT TYPE
    if reason == "input type" or reason == 7:
        out = """Invalid input type: in the settings file, please set the """ \
            + """variable input_type to be DIRECT, TERMINAL or CONSOLE."""
        raise ChordError(out)
    
    # REASON 8: INVALID OUTPUT FORMAT
    if reason == "output format" or reason == 8:
        out = """Invalid output format: in the settings file, please set """  \
            + """the variable output_format to be TEXT or PNG."""
        raise ChordError(out)
    
    # REASON 9: INVALID OUTPUT METHOD
    if reason == "output method" or reason == 9:
        out = """Invalid output method: in the settings file, please set """  \
            + """the variable output_method to be PRINT, SPLASH or NONE."""
        raise ChordError(out)
    
    # REASON 10: INVALID SAVE METHOD
    if reason == "save method" or reason == 10:
        out = """Invalid save method: in the settings file, please set the """\
            + """variable save_method to be SINGLE, LIBRARY or NONE."""
        raise ChordError(out)
    
    # REASON 11: INCOMPATIBLE OUTPUT SETTINGS
    if reason == "incompatible output" or reason == 11:
        out = """You have chosen incompatible values of output_format and """ \
            + """output_method. See settings.py to correct this."""
        raise ChordError(out)
    
    # REASON 12: SAVE DIRECTORY DOESN'T EXIST
    if reason == "file not found" or reason == 12:
        out = """The output location could not be found. If you have not """  \
            + """tweaked the settings too much, this can probably be fixed """\
            + """by creating a new folder inside the ThatChord folder """     \
            + """called 'diagrams' (all lowercase). If you have done some """ \
            + """tweaking, then please check that the output directory """    \
            + """specified in settings.py exists."""
        raise ChordError(out)
    
    # REASON 13: CUSTOM INPUT NOT RECOGNISED
    if reason == "custom" or reason == 13:
        out = """Custom input not recongised. To enter a chord note by note"""\
            + """, type "CUSTOM" followed by a list of notes separated by """ \
            + """spaces or commas. Notes can be entered as e.g. 'C#', 'G', """\
            + """'Bb', or as numbers 0-11 (0=C, 1=C#, ...)"""
        raise ChordError(out)
    
    # REASON 14: TOO MANY COLONS IN INPUT
    if reason == "colons" or reason == 14:
        out = """There are too many colons in your input. Adding a ":" at """ \
            + """the end of your chord request requests a specific index of"""\
            + """ chord in the list of possibilities. There must be at most"""\
            + """ one colon in the input."""
        raise ChordError(out)
    
    # REASON 15: CANNOT UNDERSTAND LIST INDEX REQUESTED
    if reason == "aftercolon" or reason == 15:
        out = """You have requested a specific index of chord in the list """ \
            + """of possibilities by using a colon but I don't understand """ \
            + """what index this is. Please follow a colon simply by a """    \
            + """number, e.g. 'Cmaj7:2' if you want to see the second best """\
            + """match for Cmaj7."""
        raise ChordError(out)
    
    # REASON 16: LIST INDEX REQUESTED TOO HIGH
    if reason == "fewoptions" or reason == 16:
        out = """You have requested a solution number which is greater than"""\
            + """ the number of solutions found. Please request a lower """   \
            + """index after the colon."""
        raise ChordError(out)
    
    # REASON 17: LISTS IN SETTINGS NOT OF SAME LENGTH
    if reason == "lenlists" or reason == 17:
        out = """In the settings file, please ensure that the variables """   \
            + """"tuning" and "order" have the same length."""
        raise ChordError(out)
    
    # REASON 18: STRINGSTARTS IS TOO SHORT
    if reason == "stringstarts" or reason == 18:
        out = """In the settings file, please ensure that the variable """    \
            + """"stringstarts" is at least as long as the number of frets."""
        raise ChordError(out)
    
    raise ChordError(str(reason))
