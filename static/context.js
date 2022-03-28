/**
 * Credit go's to:
 * https://dev.to/stackfindover/how-to-create-a-custom-right-click-menu-54h2
 */

document.onclick = hideMenu; 
       document.oncontextmenu = rightClick; 

        function hideMenu() { 
            document.getElementById("contextMenu") 
                    .style.display = "none" 
        } 

        function rightClick(e) { 
            e.preventDefault(); 

            if (document.getElementById("contextMenu") .style.display == "block"){ 
                hideMenu(); 
            }else{ 
                var menu = document.getElementById("contextMenu")      
                menu.style.display = 'block'; 
                menu.style.left = e.pageX + "px"; 
                menu.style.top = e.pageY + "px"; 
            } 
        } 




//https://eloquentjavascript.net/15_event.html
//
// what about "Focus Events" when a data cell is being manipulated??
//
// to change an elements contents
//document.getElementById("demo").innerHTML = "I have changed!";
//
// to get the contents of an element
//let html = document.getElementById("myP").innerHTML;