/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */


    // =============================== Listeners =============================== //
    
   
 var lock=0; 

 function showTip(id){ document.getElementById(id).style.visibility = 'visible'; }
 function hideTip(id){ document.getElementById(id).style.visibility= 'hidden';  }

 function makeSelection(idA, idB) {
  if (lock==0){
   document.getElementById(idA).style.opacity=1.0; 
   //document.getElementById(idA).filters.alpha.opacity=100;
   document.getElementById(idB).style.opacity=0.2; 
   //document.getElementById(idB).filters.alpha.opacity=20; 

   lock=1;

}
}

function ShowHide(idS, idH) {  
 document.getElementById(idS).style.display = 'block'; 
 document.getElementById(idH).style.display = 'none'; 
 }


function showTagsALL(id1,id2){  
 document.getElementById(id2).style.display = 'block'; 
 document.getElementById(id1).style.display = 'block'; 
 }
 
