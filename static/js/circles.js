/**
* This module contains all the JS code needed for the circles functionality
* Author: George Eracleous  
*/


// =============================== Drag and drop functions =============================== //

  $('div.friend-info-container').draggable( {
    revert: "invalid",
    helper: draggableHelper,
    stop: stopEventHandler,
    appendTo: 'body',
    scroll: false
  } );

  function draggableHelper(event){
     $copy = $(this).clone();
     $(this).addClass("friend-info-container-dragged");
     return $copy;
  }

  function stopEventHandler(event, ui){
     $(this).removeClass("friend-info-container-dragged");
     $(this).addClass("friend-info-container");
  }
    

