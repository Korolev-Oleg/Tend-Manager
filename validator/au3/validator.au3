#Region ;**** Directives created by AutoIt3Wrapper_GUI ****
  #AutoIt3Wrapper_Icon=..\..\..\..\Pictures\icons\gear-1077550_1280.ico
  #AutoIt3Wrapper_Res_Fileversion=2.1.1.12
  #AutoIt3Wrapper_Res_Fileversion_AutoIncrement=y
  #AutoIt3Wrapper_Run_After=start ../../upload.exe
#EndRegion ;**** Directives created by AutoIt3Wrapper_GUI ****
;~ #includes
  #include <word.au3>
  #include <Array.au3>
  #include <ButtonConstants.au3>
  #include <GUIConstantsEx.au3>
  #include <WindowsConstants.au3>
  #include <ProgressConstants.au3>
  #include <StaticConstants.au3>
;~ 

If ($cmdLine[1]) Then
  Global $CHOSE_FOLDER_PATH = $cmdLine[1]
Else
  Global $CHOSE_FOLDER_PATH = @ScriptDir
EndIf


$words_path = 'C:\Users\Huston\Documents\GitHub\Tend-Manager\validator\au3\words'

#Region ### START Koda GUI section ### Form=
  $Form1 = GUICreate("Валидатор", 207, 160, @DesktopWidth/2-207/2, @DesktopHeight/2-113)
  $Checkbox1 = GUICtrlCreateCheckbox("автозамена словосочетаний", 16, 16, 185, 17)
  GUICtrlSetState(-1, $GUI_CHECKED)
  $Checkbox2 = GUICtrlCreateCheckbox("Подсветить символы и знаки", 16, 40, 177, 17)
  GUICtrlSetState(-1, $GUI_CHECKED)
  $Checkbox3 = GUICtrlCreateCheckbox("Подсветить запрещенные слова", 16, 64, 197, 17)
  GUICtrlSetState(-1, $GUI_CHECKED)
  $Checkbox4 = GUICtrlCreateCheckbox("Заменять диапазоны", 16, 88, 197, 17)
  $Button1 = GUICtrlCreateButton("Проверить", 64, 120, 75, 25)
  GUISetState(@SW_SHOW)
#EndRegion ### END Koda GUI section ###

;~ считывание надстроек
While 1
  $nMsg = GUIGetMsg()
  Switch $nMsg
    Case $Button1
      $c = GUICtrlRead($Checkbox1)
      $s = GUICtrlRead($Checkbox2)
      $w = GUICtrlRead($Checkbox3)
      $r = GUICtrlRead($Checkbox4)
      ;~ $l = 0
      GUIDelete($Form1)
      prefs($c, $s, $w, $r)
      ExitLoop
  	Case $GUI_EVENT_CLOSE
  	Exit
  EndSwitch
WEnd

;~ применение надстроек, loader()
Func prefs($c, $s, $w, $r)
  #Region ### START Koda GUI section ### Form=
    Opt("GUIOnEventMode", 1)
    $n = "Валидация"
    global $ProgressForm = GUICreate($n, 365, 90, -1, -1, -1, $WS_EX_TOPMOST)
    global $Progress = GUICtrlCreateProgress(16, 16, 329, 17)
    global $progressLabel = GUICtrlCreateLabel("Label", 16, 40, 355, 17)
  #EndRegion ### END Koda GUI section ###
  Const $document = FileOpenDialog( "Выберите документ для проверки", $CHOSE_FOLDER_PATH, "Документ Word (*.doc;*.docx)" )
  If (not $document) Then
    Exit
  EndIf

  GUISetState(@SW_SHOW)
  $file = FileOpen( $words_path )
  Const $DATA = StringSplit( FileRead( $file ), "|" )
  Const $words = StringSplit( $DATA[2], @LF )
  Const $symbols = StringSplit( $DATA[1], @LF )
  Const $ranges = StringSplit( $DATA[3], @LF )
  Const $replaces = StringSplit( $DATA[4], @LF )

  global const $VISIBLE = true


  If $document Then
    $app = settings( $document, $VISIBLE )
    $errors = 0
    if ($w == 1) then global $errors = validate( $app[0], $words , 0x0000FF, 0, "Подсветка недопустимых значений: " )
    if ($s == 1) then validate( $app[0], $symbols , 0xFFC000, 1, "Выделение символов и знаков: " )
    if ($c == 1) then findReplace( $app, $replaces )
    ;~ if ($r == 1) then findReplace( $app, $ranges )
    settings( "", 0 )
      
    progress(99, "Готово")
    Sleep(500)
    Exit
  EndIf
    Return True
EndFunc

;~ ?
;~ Func clear($clear)
;~   For $i = 2 To $clear[0] Step +1
;~     _Word_DocFindReplace( $doc[1], $clear[$i], "" )
;~     validate($doc[0], $word, 0x005aFF, 0)
;~     Next
;~   Return True
;~ EndFunc

;~ преднастройка объекта Word
Func settings($doc, $switch)
  If $switch Then
    $app =  _Word_Create( 1 )
    $doc = _Word_DocOpen( $app, $doc )
    dim $apl[2] = [$app, $doc]
  Else
    If not($VISIBLE) then $app.Aplication.Quit
    $apl = 0 
  EndIf

  Return $apl
EndFunc

;~ подсветка текста
Func validate($app, $str, $color, $bold, $action)
  $app.selection.find.ClearFormatting()
  $ii = 0

  For $i = 1 To $str[0] step +1
    $app.Selection.GoTo (1, 1, 1, "1")
    $str[$i] = StringStripWS($str[$i], 2)

    while $app.selection.find.execute($str[$i], 0, 1)
      if Not($app.selection.Font.Color == $color) Then $ii+=1
      ;~ if $replace then $app.selection.find.execute($str[$i], $replace, 1)
      $app.selection.Font.Bold = $bold
      $app.selection.Font.Color = $color
      $app.Selection.Find.Execute
      $app.selection.Font.Bold = $bold
      $app.selection.Font.Color = $color
      progress($ii, $action & $str[$i])
    wend
  Next
  
  Return $ii
EndFunc

;~ замена текста
Func findReplace($doc, $replaces)

  For $i = 2 To UBound($replaces)-1 Step +1
    $word = StringSplit($replaces[$i], "-")
    If (UBound($word) == 3) Then
      $replaceWord = StringReplace($word[2], @CR, "")
      $replaced = _Word_DocFindReplace( $doc[1], $word[1], $replaceWord )
      ;~ validate($doc[0], $word, 0x005aFF, 0, $replaceWord)
      if $replaced == 1 then validate($doc[0], $word, 0x3A9D03, 0, "Замена текста: ")
    EndIf
  Next

  Return True
EndFunc

;~ изменяет progressbar
Func progress($value, $params)
  GUICtrlSetData($Progress, $value)
  GUICtrlSetData($progressLabel, $params)
  Return True
EndFunc

Func stop()
  Exit
EndFunc