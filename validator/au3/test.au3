#include <Array.au3>

$words_path = 'C:\Users\Huston\Documents\GitHub\Tend-Manager\validator\au3\words'
$file = FileOpen( $words_path )
$DATA = StringSplit( FileRead( $file ), "|" )


Const $replaces = StringSplit( $DATA[4], @LF )

findReplace($replaces)

Func msg($msg)
  MsgBox(0, 'writer', $msg)
EndFunc

Func findReplace($replaces)

  For $i = 2 To UBound($replaces)-1 Step +1
    $word = StringSplit($replaces[$i], "-")
    If (UBound($word) = 3) Then
      msg(UBound($replaces) & UBound($word))
      $replaceWord = StringReplace($word[2], @CR, "")
    EndIf
  Next

  Return True
EndFunc

FileClose($file)
