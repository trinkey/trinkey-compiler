# Set this variable using command line later during production
path = input("Enter file path: ")

count         = 0
indentLevel   = 0
indentText    = "    "
inIfStatement = [False]
output        = '# Compiled from a .trinkey file.\nregister = {"A": 0.0, "B": 0.0, "C": 0.0, "D": 0.0, "E": 0.0, "F": 0.0, "G": 0.0, "H": 0.0, "I": 0.0, "J": 0.0, "K": 0.0, "L": 0.0, "M": 0.0, "N": 0.0, "O": 0.0, "P": 0.0, "Q": 0.0, "R": 0.0, "S": 0.0, "T": 0.0, "U": 0.0, "V": 0.0, "W": 0.0, "X": 0.0, "Y": 0.0, "Z": 0.0, "0": "", "1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": ""}\n\n'

EXCESS_CHARS   = [" ", "|"]
FILE_EXT       = "trinkey"
JUST_COMMAND   = [":__", "end", "!__"]
NEWLINE        = "\n"
VALID_COMMANDS = ["cmd", "add", "sub", "mlt", "div", "str", "cmd", "2st", "2nm", "for", "whl", "?__", "?:_", ":__", "end", "dsp", "in_", "!__"]

def removeStrings(string: str) -> str:
    out = ""
    typeOfQuote = ""
    inside = False
    escaped = False
    for i in string:
        if inside and not escaped and i == typeOfQuote:
            inside = False
        elif not escaped and i == "\\":
            escaped = True
            if not inside:
                out += i
        elif not inside and not escaped and i in ["'", '"']:
            inside = True
            typeOfQuote = i
        elif not inside:
            out += i
            escaped = False
        else:
            escaped = False
    return out

def removeExcessChars(string: str) -> str:
    try:
        while string[0] in EXCESS_CHARS:
            string = string[1::]
        while string[-1] in EXCESS_CHARS:
            string = string[:-1:]
    except:
        pass
    return string

def replaceRegisters(string: str) -> str:
    for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
        string = string.replace(f"${i}", f"register[\"{i}\"]")
    return string

def addVal(string: str, newline: bool = True, indentMod: int = 0) -> None:
    global indentLevel, indentText, output
    output += f"{indentText * (indentLevel + indentMod)}{string}{NEWLINE if newline else ''}"

if path.split(".")[-1] != FILE_EXT:
    err = SyntaxError()
    err.filename = path
    err.msg = f"Loading error: Incorrect file extension. Should be a .{FILE_EXT} file"
    raise err

stack = [
    [[removeExcessChars(i[:3:]), removeExcessChars(i[4::])] if len(i) >= 5 else [removeExcessChars(i[:3:]), None]][0]
    if len(i) >= 4 and i[3] == ":" else None
    for i in open(path, "r").read().split("\n")
    if i[:3:] != "!__"
]

for i in stack:
    count += 1
    if i == None:
        err = SyntaxError()
        err.filename = path
        err.msg = f"Compiler error: Colon missing or in the wrong place at stack {count}"
        raise err
    CMD  = i[0].lower()
    INFO = i[1]

    if CMD not in VALID_COMMANDS:
        err = SyntaxError()
        err.filename = path
        err.msg = f"Compiling error: Invalid command at stack {count} ({CMD}: {INFO})"
        raise err

    elif CMD == "add":
        if len(removeStrings(INFO).split(",")) == 3:
            if len(removeExcessChars(removeStrings(INFO).split(",")[2])) != 2 or \
                removeExcessChars(INFO.split(",")[-1])[0] != "$" or \
                removeExcessChars(INFO.split(",")[-1])[1] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                err = SyntaxError()
                err.filename = path
                err.msg = f"Compiling error: Item '{removeExcessChars(removeStrings(INFO)).split(',')[2]}' not register at stack {count} ({CMD}: {INFO})"
                raise err
            else:
                addVal(f"{replaceRegisters(removeExcessChars(INFO.split(',')[-1]))} = {replaceRegisters(removeExcessChars(INFO.split(',')[0]))} + {replaceRegisters(removeExcessChars(INFO.split(',')[-2]))}")
        else:
            err = SyntaxError()
            err.filename = path
            err.msg = f"Compiling error: Invalid amount of inputs at stack {count}, {len(removeStrings(INFO).split(','))} given, 3 required ({CMD}: {INFO})"
            raise err

    elif CMD == "sub":
        if len(removeStrings(INFO).split(",")) == 3:
            if len(removeExcessChars(removeStrings(INFO).split(",")[2])) != 2 or \
                removeExcessChars(INFO.split(",")[-1])[0] != "$" or \
                removeExcessChars(INFO.split(",")[-1])[1] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                err = SyntaxError()
                err.filename = path
                err.msg = f"Compiling error: Item '{removeExcessChars(removeStrings(INFO)).split(',')[2]}' not register at stack {count} ({CMD}: {INFO})"
                raise err
            else:
                addVal(f"{replaceRegisters(removeExcessChars(INFO.split(',')[-1]))} = {replaceRegisters(removeExcessChars(INFO.split(',')[0]))} - {replaceRegisters(removeExcessChars(INFO.split(',')[-2]))}")
        else:
            err = SyntaxError()
            err.filename = path
            err.msg = f"Compiling error: Invalid amount of inputs at stack {count}, {len(removeStrings(INFO).split(','))} given, 3 required ({CMD}: {INFO})"
            raise err

    elif CMD == "mlt":
        if len(removeStrings(INFO).split(",")) == 3:
            if len(removeExcessChars(removeStrings(INFO).split(",")[2])) != 2 or \
                removeExcessChars(INFO.split(",")[-1])[0] != "$" or \
                removeExcessChars(INFO.split(",")[-1])[1] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                err = SyntaxError()
                err.filename = path
                err.msg = f"Compiling error: Item '{removeExcessChars(removeStrings(INFO)).split(',')[2]}' not register at stack {count} ({CMD}: {INFO})"
                raise err
            else:
                addVal(f"{replaceRegisters(removeExcessChars(INFO.split(',')[-1]))} = {replaceRegisters(removeExcessChars(INFO.split(',')[0]))} * {replaceRegisters(removeExcessChars(INFO.split(',')[-2]))}")
        else:
            err = SyntaxError()
            err.filename = path
            err.msg = f"Compiling error: Invalid amount of inputs at stack {count}, {len(removeStrings(INFO).split(','))} given, 3 required ({CMD}: {INFO})"
            raise err

    elif CMD == "div":
        if len(removeStrings(INFO).split(",")) == 3:
            if len(removeExcessChars(removeStrings(INFO).split(",")[2])) != 2 or \
                removeExcessChars(INFO.split(",")[-1])[0] != "$" or \
                removeExcessChars(INFO.split(",")[-1])[1] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                err = SyntaxError()
                err.filename = path
                err.msg = f"Compiling error: Item '{removeExcessChars(removeStrings(INFO)).split(',')[2]}' not register at stack {count} ({CMD}: {INFO})"
                raise err
            else:
                addVal(f"{replaceRegisters(removeExcessChars(INFO.split(',')[-1]))} = {replaceRegisters(removeExcessChars(INFO.split(',')[0]))} / {replaceRegisters(removeExcessChars(INFO.split(',')[-2]))}")
        else:
            err = SyntaxError()
            err.filename = path
            err.msg = f"Compiling error: Invalid amount of inputs at stack {count}, {len(removeStrings(INFO).split(','))} given, 3 required ({CMD}: {INFO})"
            raise err

    elif CMD == "2st":
        if len(removeStrings(INFO).split(",")) == 2:
            if len(removeExcessChars(removeStrings(INFO).split(",")[1])) != 2 or \
                removeExcessChars(INFO.split(",")[-1])[0] != "$" or \
                removeExcessChars(INFO.split(",")[-1])[1] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                err = SyntaxError()
                err.filename = path
                err.msg = f"Compiling error: Item '{removeExcessChars(removeStrings(INFO)).split(',')[1]}' not register at stack {count} ({CMD}: {INFO})"
                raise err
            else:
                addVal(f"{replaceRegisters(removeExcessChars(INFO.split(',')[-1]))} = str({replaceRegisters(','.join(INFO.split(',')[:-1:]))})")
        else:
            err = SyntaxError()
            err.filename = path
            err.msg = f"Compiling error: Invalid amount of inputs at stack {count}, {len(removeStrings(INFO).split(','))} given, 2 required ({CMD}: {INFO})"
            raise err

    elif CMD == "2nm":
        if len(removeStrings(INFO).split(",")) == 2:
            if len(removeExcessChars(removeStrings(INFO).split(",")[1])) != 2 or \
                removeExcessChars(INFO.split(",")[-1])[0] != "$" or \
                removeExcessChars(INFO.split(",")[-1])[1] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                err = SyntaxError()
                err.filename = path
                err.msg = f"Compiling error: Item '{removeExcessChars(removeStrings(INFO)).split(',')[1]}' not register at stack {count} ({CMD}: {INFO})"
                raise err
            else:
                addVal(f"{replaceRegisters(removeExcessChars(INFO.split(',')[-1]))} = float({replaceRegisters(','.join(INFO.split(',')[:-1:]))})")
        else:
            err = SyntaxError()
            err.filename = path
            err.msg = f"Compiling error: Invalid amount of inputs at stack {count}, {len(removeStrings(INFO).split(','))} given, 2 required ({CMD}: {INFO})"
            raise err

    elif CMD == "str":
        if len(removeStrings(INFO).split(",")) == 2:
            if len(removeExcessChars(removeStrings(INFO).split(",")[1])) != 2 or \
                removeExcessChars(INFO.split(",")[-1])[0] != "$" or \
                removeExcessChars(INFO.split(",")[-1])[1] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                err = SyntaxError()
                err.filename = path
                err.msg = f"Compiling error: Item '{removeExcessChars(removeStrings(INFO)).split(',')[1]}' not register at stack {count} ({CMD}: {INFO})"
                raise err
            else:
                addVal(f"{replaceRegisters(removeExcessChars(INFO.split(',')[-1]))} = {replaceRegisters(removeExcessChars(','.join(INFO.split(',')[:-1:])))}")
        else:
            err = SyntaxError()
            err.filename = path
            err.msg = f"Compiling error: Invalid amount of inputs at stack {count}, {len(removeStrings(INFO).split(','))} given, 2 required ({CMD}: {INFO})"
            raise err

    elif CMD == "in_":
        if len(removeStrings(INFO).split(",")) == 2:
            if len(removeExcessChars(removeStrings(INFO).split(",")[1])) != 2 or \
                removeExcessChars(INFO.split(",")[-1])[0] != "$" or \
                removeExcessChars(INFO.split(",")[-1])[1] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                err = SyntaxError()
                err.filename = path
                err.msg = f"Compiling error: Item '{removeExcessChars(removeStrings(INFO)).split(',')[1]}' not register at stack {count} ({CMD}: {INFO})"
                raise err
            else:
                if removeExcessChars(INFO.split(",")[-1])[1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    addVal(f"{replaceRegisters(removeExcessChars(INFO.split(',')[-1]))} = float(input({replaceRegisters(','.join(INFO.split(',')[:-1:]))}))")
                else:
                    addVal(f"{replaceRegisters(removeExcessChars(INFO.split(',')[-1]))} = input({replaceRegisters(','.join(INFO.split(',')[:-1:]))})")

        else:
            err = SyntaxError()
            err.filename = path
            err.msg = f"Compiling error: Invalid amount of inputs at stack {count}, {len(removeStrings(INFO).split(','))} given, 2 required ({CMD}: {INFO})"
            raise err

    elif CMD == "dsp":
        addVal(f"print({replaceRegisters(INFO)})")

    elif CMD == "?__":
        indentLevel += 1
        inIfStatement.append(True)
        addVal(f"if {replaceRegisters(INFO)}{':' if INFO[-1] != ':' else ''}", indentMod=-1)

    elif CMD in ["?:_", ":__"]:
        if not inIfStatement[indentLevel]:
            err = SyntaxError()
            err.filename = path
            err.msg = f"Compiling error: Elif/else statement outside of if statement at stack {count} ({CMD}: {INFO})"
            raise err

        if CMD == "?:_":
            addVal(f"elif {replaceRegisters(INFO)}{':' if INFO[-1] != ':' else ''}", indentMod=-1)

        if CMD == ":__":
            addVal(f"else:", indentMod=-1)

    elif CMD == "whl":
        indentLevel += 1
        inIfStatement.append(False)
        addVal(f"while {replaceRegisters(INFO)}{':' if INFO[-1] != ':' else ''}", indentMod=-1)

    elif CMD == "for":
        if len(removeExcessChars(INFO.split(",")[0])) != 2 or \
            removeExcessChars(INFO.split(",")[0])[0] != "$" or \
            removeExcessChars(INFO.split(",")[0])[1] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            err = SyntaxError()
            err.filename = path
            err.msg = f"Compiling error: Item '{removeExcessChars(removeStrings(INFO)).split(',')[0]}' not register at stack {count} ({CMD}: {INFO})"
            raise err
        elif len(INFO.split(",")) != 4:
            err = SyntaxError()
            err.filename = path
            err.msg = f"Compiling error: Invalid amount of inputs at stack {count}, {len(INFO.split(','))} given, 4 required ({CMD}: {INFO})"
            raise err
        else:
            indentLevel += 1
            inIfStatement.append(False)
            addVal(f"for {replaceRegisters(INFO.split(',')[0])} in range({replaceRegisters(', '.join(INFO.split(',')[1::]))}){':' if INFO[-1] != ':' else ''}", indentMod=-1)

    elif CMD == "end":
        indentLevel -= 1
        inIfStatement.pop(-1)

if indentLevel > 0:
    err = SyntaxError()
    err.filename = path
    err.msg = f"Compiling error: Not enough ends to close all loops and conditionals ({indentLevel} left)"
    raise err

try:
    saveFile = open(f"{path}.py", "x")
except FileExistsError:
    saveFile = open(f"{path}.py", "w")
saveFile.write(output[:-1:])
saveFile.close()