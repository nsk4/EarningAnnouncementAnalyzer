^a::
Loop, 50 ; run 50 iterations
{
	Send, {F12} ; open dev tools
	sleep, 2000
	click, 300, 900 ; click on dev tools
	Send, ^V ; paste script
	Send, {Enter} ; run script
	sleep, 120000 ; wait until script is done processing (6 years -> 120 seconds)

	click, 20, 20 ; select first tab
	Send, {MButton} ; close first tab
	
	sleep, 60000 ; general wait between requests
}
return