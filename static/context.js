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