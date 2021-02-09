
function deleteMusic(musicId) {
  fetch("/delete-music", {
    method: "POST",
    body: JSON.stringify({ musicId: musicId }),
  }).then((_res) => {
    window.location.href = "/music_player";
  });
}

function deleteUser(userId) {
  fetch("/delete-user", {
    method: "POST",
    body: JSON.stringify({ userId: userId }),
  }).then((_res) => {
    window.location.href = "/user_list";
  });
}

function deleteNoteAdmin(noteId) {
  fetch("/delete-note-admin", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/user_list";
  });
}

function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


