; A simple program to cycle through the background colors
; See https://youtu.be/H-n64TxS7MM?si=WSkVgCch3FJas6KI
;
; Expected result (Hex):
; CA 8E 20 D0 20 E4 FF C9 00 F0 F5 60
;
; Expected BASIC code:
; 10 DATA 202         : REM DEX
; 20 DATA 142,32,208  : REM STX $D020
; 30 DATA 32,228,255  : REM JSR $FFE4
; 40 DATA 201,0       : REM CMP #$00
; 50 DATA 240,245     : REM BEQ (START)
; 60 DATA 96          : REM RTS
; 70 DATA -1
; 1000 PC=49152
; 1010 X=0
; 1020 READ A:IF A=-1 THEN END
; 1030 POKE PC+X,A:X=X+1:GOTO 1020

START:
  DEX
  STX $D020
  JSR $FFE4
  CMP #$00
  BEQ START
  RTS

