; first, support just one small set of commands:
; L: load a block of memory and print it to screen
; ... more coming soon ...
; 
; If the operation is not recognized, print to screen "?"
; When the operation is loaded, store it somewhere in memory (maybe zero page).
; Continue push characters to stack until ENTER is pressed.


;-----------------------------------------
; MEMORY ADDRESSES:
;   0002: Current operation
;-----------------------------------------


START:
RESET_PROMPT:
  ; clear current operation
  ; start waiting for command

READ_OPERATION:
  JSR $FFE4;                 ; Get a character (GETIN)
  CMP #$0;
  BEQ READ_OPERATION;        ; Wait unti a char is provided
  ;---- L ----
  CMP #$4                    ; Is the instruction ASCII "L"?
  BEQ VALID_INSTRUCTION

  ;---- Not found ----
  ; TODO: Somehow print error
  JMP RESET_PROMPT           ; Let's try again

VALID_INSTRUCTION:
  STA $02                    ; Store the operation in memory register

READ_PARAMETERS:
  TSX                        ; Make a note of where we are with the stack

READ_SINGLE_CHAR:
  JSR $FFE4                  ; Get a character (Kernal GETIN)
  CMP #$00
  BEQ READ_SINGLE_CHAR       ; What until a char is provided
  CMP #$0D                   ; Is the character RETURN (ENTER)?
  BEQ RUN_INSTRUCTION        ; User said we are done!
  CMP #$20                   ; Is the character a space?
  BEQ READ_SINGLE_CHAR       ; Ignore spaces
  PHA                        ; Add the character to the stack...
  JMP READ_SINGLE_CHAR       ; ... and fetch the next character

RUN_INSTRUCTION:
  ; TODO: what do we do here?

