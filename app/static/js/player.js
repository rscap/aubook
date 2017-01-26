current_playing_id = null;
// recordCurrentTime = true;

// stuff that happens when the page loads
// console.log('start!')
var aud = document.getElementById('audio')
var aud2 = document.getElementById('audio2')
// Attach a "timeupdate" event to the video
// aud.addEventListener("timeupdate", reportCurTime);
//aud2.addEventListener("timeupdate", reportCurTime);


// Display the current playback position of the video in a p element with id="time"
function reportCurTime() {
  console.log('aud.currentTime in reportCurTime = '+aud.currentTime)
document.getElementById("time").innerHTML = "The current playback position is " + aud.currentTime + " seconds.";
}

// console.log('aud.paused state: '+aud.paused);

// aud.addEventListener('pause', printTime)

// function printTime (){
//   console.log('current time = '+aud.currentTime)
// }


// Assigns the active element to the var activeElement (used to stop spacebar control while notating bookmarks)
document.body.onclick=function() {
  activeElement = document.activeElement.id;
  if (activeElement !='') {
    console.log('activeElement = '+activeElement);
  } else {
    console.log('no element selected');
  }
}


// enables spacebar pause/play action
document.body.onkeypress = function(e){
  if (activeElement != 'desc') {
    if(e.keyCode == 32){
      console.log('space bar pressed')
      if (aud.paused) {
        console.log('status is paused')
        console.log('playing')
        aud.play()
      } else {
        console.log('pausing')
        aud.pause()
      }
    }
  }
}

// // controls the bookmark UI
function enableBookmarkUI() {
  if (current_playing_id == null) {
    $('#currentPlaying').html("<h3 class=\'w3-text-red\'>  No book slected. Select book before creating bookmark.<h3>");
  } else {
    $('#createBookmark').toggle();
  }
}

// jQuery for timed events
$(document).ready(function(){
   console.log('ready!');
//  setInterval(saveTime,10000);
});

// operates the fastforward and rewind buttons
function changeTime(op, time) {
  if (op == '+') {
    aud.currentTime = aud.currentTime + time;
  }
  else {
      aud.currentTime = aud.currentTime - time;
  };
}

//saves bookmarks to db
function saveBookmark() {
  console.log('saveBookmark button pushed!');
  var form = new FormData(document.getElementById('bookmarkForm'));
  var desc = form.get('desc');
  console.log(desc)
  if (current_playing_id != null) {
  $.ajax({
    type: 'POST',
    url: '/saveBookmark',
    data: JSON.stringify({'book_id':current_playing_id,'time':aud.currentTime,'desc':desc}, null, '\t'),
    contentType:'application/json;charset=UTF-8',
    success: function(){
      retrieveBookmarks();
      console.log('time saved')
    },
    error: function() {
        console.log('bookmark not saved')
      }
  });
  $('#createBookmark').toggle();
  }
 }



 // retrieves times time from db
 function retrieveTime() {
   console.log('retrieveTime start')
    $.ajax({
      type: 'POST',
      url: '/retrieveTime',
      data: JSON.stringify({'book_id':current_playing_id}, null, '\t'),
      contentType: 'application/json;charset=UTF-8',
      success: function(currentBookTime) {
          console.log('in retrieveTime, aud.currentTime = '+aud.currentTime)
          console.log('currentBookTime = '+currentBookTime.currentBookTime)
          // console.log('Bookmarks = '+bookmarks)
          aud.currentTime = currentBookTime.currentBookTime
          // $('#audio').bind('canplaythrough',function(){
          //   console.log('before = '+aud.currentTime);
          //  aud.currentTime = currentBookTime.currentBookTime
          //   console.log('after = '+aud.currentTime);
          //
          // });
          // recordCurrentTime = true;
          console.log('aud.currentTime last in success = '+aud.currentTime)
          // $('#resumeTimeline').prop('disabled',true);
          $(loading).hide();
          $(player).show();
        //  console.log('retrieveTime function done ran');
      },
      error: function() {
          console.log('time not retrieved')
      }
    });
 }


// saves currentTime for book being played to db
//  function saveTime() {
//     if (current_playing_id != null && recordCurrentTime==true )  {
//         console.log('recordCurrentTime in saveTime = '+recordCurrentTime);
//       $.ajax({
//         type: 'POST',
//         url: '/saveTime',
//         data: JSON.stringify({'book_id':current_playing_id,'currentTime':aud.currentTime}, null, '\t'),
//         contentType:'application/json;charset=UTF-8',
//         success: function(){
//           console.log('time saved')
//         },
//         error: function() {
//           console.log('currentTime not saved')
//         }
//        })
//      }
//  }


 // retrieve Bookmark for selected book from db
 function retrieveBookmarks() {
  //  if (current_playing_id !='null') {
    $.ajax({
      type: 'POST',
      url: '/retrieveBookmark',
      data: JSON.stringify({'book_id':current_playing_id}, null, '\t'),
      contentType: 'application/json;charset=UTF-8',
      success: function(data) {
        console.log('type of = '+typeof data);
        console.log('number of bookmarks = '+data.length);
        $.each(data, function(i,bookmark) {
          console.log('type of = '+typeof data);
          console.log('bookmark.desc = '+bookmark.desc)
          // console.log('data[i] = '+data[i])
          console.log('i = '+i)
        }
      )

       }
      //   if (data.bookmark.length != '0') {
      //       console.log('there are bookmarks');
      //       container = $('#bookmarks');
      //       container.empty();
      //       container.html('<h3>Bookmarks</h3>');
      //       // $('#bookmark_list').append('<tr><th></th><th>Description</th><th>Time</th>')
      //       $.each(data.bookmark, function(i,bookmark){
      //         console.log('data = '+data);
      //         console.log('bookmark = '+bookmark);
      //         console.log('data.bookmark.id = '+data.bookmark.id);
      //         // create the DOM
      //            link = $('<a>'),
      //            trshcn = $('<img>'),
      //            cell = $('<td>'),
      //            row = $('<tr>');
      //            p = $('<p>');
      //         trshcn.attr({'src':'static/img/trash-can.png','width':'15','height':'15'});
      //         // trshcn.click(book,removeBookmark);
      //         trshcn.appendTo(cell);
      //         trshcn.appendTo(row);
      //         link.attr('href','javascript:void(0)').text(data.bookmark.desc).appendTo(cell);
      //         // link.click(book,setBook);
      //         cell.appendTo(row);
      //         row.appendTo(container);
      //       })
      //       // for (i=0; i<data.bookmark.length; i++){
      //       //   $('#bookmark_list').append('<img type="image" src="{{ url_for('static', filename='img/trash-can.png') }}" width="15" height="15"><li id=bookmark'+data.bookmark[i]['id']+'><a href="avascript:void(0);" onclick=goToTime('+data.bookmark[i]['time']+');>'+data.bookmark[i]['desc']+'</a></li>');
      //       //   console.log('id = bookmark'+data.bookmark[i]['id'])
      //         // $('#bookmark_list').append(
      //         //   '<tr><td><input type="image" src="{{ url_for('static', filename='img/trash-can.png') }}" width="15" height="15" onclick=removeBookmark('+data.bookmark[i]['id']+')></td><td id=bookmark'+data.bookmark[i]['id']+'><a href="avascript:void(0);"onclick=goToTime('+data.bookmark[i]['time']+');>'+data.bookmark[i]['desc']+'</a></td></tr>');
      //
      //   } else {
      //     console.log('there are no bookmarks.')
      //   }
      // },
      // error: function() {
      //   console.log('didn\'t get bookmarks')
      // }
     })
    }



// // sets play position for selected bookmark
// function goToTime(time){
//   recordCurrentTime = false;
//   console.log('recordCurrentTime = '+recordCurrentTime);
//   aud.currentTime=time;
//   $('#resumeTimeline').prop('disabled',false);
// }

function removeBook(book){
  console.log('removeBook start');
  $.ajax({type:'POST',url:'removeBook',data: JSON.stringify({'book_id':book.data.id}, null, '\t'),contentType: 'application/json;charset=UTF-8',success:loadBooks,error:lose});
}

function removeBookmark(bookmarkId){
  console.log('desc = '+desc);
  $.ajax({
    type: 'POST',
    url: '/removeBookmark',
    data: JSON.stringify({'id':bookmarkId}, null, '\t'),
    contentType: 'application/json;charset=UTF-8',
    success: function() {
      console.log('bookmark removed');
      retrieveBookmarks();
    },
    error: function() {
      console.log('bookmark not removed.')
    }
  })
}


// function loadBooks(url,success,error) {
//   console.log('loadBooks start')
//   // var obj = {
//   //   url: '/getBooks',
//   //   success: loadBooksSuccess,
//   //   error: lose
//   // };
//   // $.ajax(obj);
//   $.ajax({url:url,success:success,error:error})
// }



function win() {
  console.log('win ran')
}

function loadBooksSuccess(data) {
  console.log('loadBooksSuccess wran')
  // console.log('type of = '+typeof data);
  // console.log(data);
  // console.log(data[0]);
  // console.log(data[0]['id']);
  // console.log('number of book(s) = '+data.length);
  if (data.length == '0') {
      // console.log('there are no books');
      // $('#checkedout_Books').html('You have no Books in the checked out<br/> Head over to the <a href="{{ url_for('library')}}">Library<a>');
      // $('#checkedout_Books').empty();
      // $('#bookmark_list').html('<h3>Bookmarks</h3>')
  } else {
    $('#checkedout_Books').empty();
    $('#checkedout_Books').html('<h3>Your Books</h3>')
    container = $('#checkedout_Books');
    $.each(data, function(i,book){
      // console.log('book id in each loop = '+book.id);
      // create the DOM
         link = $('<a>'),
         trshcn = $('<img>'),
         cell = $('<td>'),
         row = $('<tr>');
         p = $('<p>');
      trshcn.attr({'src':'static/img/trash-can.png','width':'15','height':'15'});
      trshcn.click(book,removeBook);
      trshcn.appendTo(cell);
      trshcn.appendTo(row);
      link.attr('href','javascript:void(0)').text(book.title).appendTo(cell);
      link.click(book,setBook);
      cell.appendTo(row);
      row.appendTo(container);
    });
      }
    // $('#checkedout_Books').append('</table>')
    retrieveBookmarks();
    }



function lose() {
  console.log('lose ran')
}

function loadBooks() {
  $.ajax({url:'/getBooks',success:loadBooksSuccess,error:lose})
}

function setBook(book) {
  console.log('clicked '+book.data.title);
  var continut = '/'+book.data.id+'/'+this.textContent+'.mp3'; // gets the content
  current_playing_id = book.data.id
  document.getElementById('audio').setAttribute('src', '/audio'+continut);
  document.getElementById('currentPlaying').innerHTML = this.textContent;
  //var t = timeInfo('currentTime=none&book_id='+current_playing_id);
  retrieveBookmarks();
}

window.addEventListener('load', loadBooks); //loadBooks('/getBooks',loadBooksSuccess,lose));
// window.addEventListener('load',$.ajax({url:'/getBooks',success:loadBooksSuccess,error:lose}));
