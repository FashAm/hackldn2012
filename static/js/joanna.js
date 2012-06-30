/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */


    // =============================== Listeners =============================== //
    
    
   
 function showTip(id){ document.getElementById(id).style.visibility = 'visible'; }
 function hideTip(id){ document.getElementById(id).style.visibility= 'hidden'; console.log('CHECKARISMA') }

 var lock=0; 
 function makeSelection(idA, idB) {
  if (lock==0){
	document.getElementById(idB).style.opacity=0.2; 
	document.getElementById(idB).filters.alpha.opacity=20; 
	document.getElementById(idA).style.opacity=1.0; 
	document.getElementById(idA).filters.alpha.opacity=100; 

	lock=1;
   }
 } 
 
