```ahk name=swipe.ahk
; swipe.ahk
; Aceita parâmetros de linha de comando: startX, startY, endX, endY, steps
; Exemplo de chamada: AutoHotkey.exe swipe.ahk 1100 400 900 100 10

#NoTrayIcon

; Verifica se os parâmetros foram passados
if (A_Args.Length() < 5) {
    MsgBox, 16, Erro, Uso: AutoHotkey.exe swipe.ahk startX startY endX endY steps
    ExitApp
}

; Lê os parâmetros da linha de comando
startX := A_Args[1]
startY := A_Args[2]
endX := A_Args[3]
endY := A_Args[4]
steps := A_Args[5]

; Desativa modo de tiro (pressiona "x")
Send, {x down}

; Calcula os incrementos de cada passo
deltaX := (endX - startX) / steps
deltaY := (endY - startY) / steps

; Pressiona o botão esquerdo do mouse
MouseClick, left, %startX%, %startY%, 1, 0, D

; Faz o movimento em etapas suaves
Loop, %steps%
{
    newX := Round(startX + (A_Index * deltaX))
    newY := Round(startY + (A_Index * deltaY))
    MouseMove, %newX%, %newY%, 0
    Sleep, 10
}

; Solta o botão do mouse
MouseClick, left, , , , , U
Sleep, 150

; Reativa modo de tiro (solta "x")
Send, {x up}

ExitApp
```