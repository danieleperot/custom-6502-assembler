# Danmos assembler

 A simple 6502 assembler to learn how to program with machine code in a Commodore 64.

 Simpy run `python assempler.py [path/to/code.s]` and get a machine code output,
 as well as BASIC instructions to allow you to load your code into your brand
 new Commodore 64!

## Usage
```
usage: Danmos Assembler [-h] [-s START_POSITION] [-b BYTES_PER_LINE] filename

A simple, basic, uncompleted 6502 assembler

positional arguments:
  filename

options:
  -h, --help            show this help message and exit
  -s START_POSITION, --start-position START_POSITION
                        Start position of the program (hexidecimal) [default:
                        0xC000]
  -b BYTES_PER_LINE, --bytes-per-line BYTES_PER_LINE
                        Number of bytes per line in instructions output
                        [default: 8]
```

## Sample output
```shell
python assembly.py samples/cycle_colors.s
```

Output:
```
Labels:
	0xC000: START
	0xC00C: TEST

Instructions:
	C000: A2 01 8E 00 04 4C 0C C0 
	C008: A2 02 8E 01 04 A2 03 8E 
	C010: 02 04 

	Total bytes: 18

BASIC instructions:
	10 DATA 162,1        :REM LDX #$01
	20 DATA 142,0,4      :REM STX $0400
	30 DATA 76,12,192    :REM JMP TEST
	40 DATA 162,2        :REM LDX #$02
	50 DATA 142,1,4      :REM STX $0401
	60 DATA 162,3        :REM LDX #$03
	70 DATA 142,2,4      :REM STX $0402

	3000 DATA -1
	3010 PC=49152
	3020 X=0
	3030 READ A:IF A=-1 THEN END
	3040 POKE PC+X,A:X=X+1:GOTO 3030

	SYS 49152
```

By specifying `--bytes-per-line=1`, you can see the output grouped by assembly
instruction.

```
Labels:
	0xC000: START
	0xC00C: TEST

Instructions:
  LDX #$01
	  C000: A2 
	  C001: 01 
  STX $0400
	  C002: 8E 
	  C003: 00 
	  C004: 04 
  JMP TEST
	  C005: 4C 
	  C006: 0C 
	  C007: C0 
  LDX #$02
	  C008: A2 
	  C009: 02 
  STX $0401
	  C00A: 8E 
	  C00B: 01 
	  C00C: 04 
  LDX #$03
	  C00D: A2 
	  C00E: 03 
  STX $0402
	  C00F: 8E 
	  C010: 02 
	  C011: 04 

	Total bytes: 18

BASIC instructions:
	10 DATA 162,1        :REM LDX #$01
	20 DATA 142,0,4      :REM STX $0400
	30 DATA 76,12,192    :REM JMP TEST
	40 DATA 162,2        :REM LDX #$02
	50 DATA 142,1,4      :REM STX $0401
	60 DATA 162,3        :REM LDX #$03
	70 DATA 142,2,4      :REM STX $0402

	3000 DATA -1
	3010 PC=49152
	3020 X=0
	3030 READ A:IF A=-1 THEN END
	3040 POKE PC+X,A:X=X+1:GOTO 3030

	SYS 49152
```
