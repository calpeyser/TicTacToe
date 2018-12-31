function write(space, value) {
  var id = "square_" + space
  $("#" + id).html(value)
}

function getState() {
  var state = []
  for (var i = 0; i < 9; i++) {
    var value = $("#square_" + i).html()
    state.push(value)
  }
  return state
}

function requestMove(current_state) {
  $.post("/move", {state: JSON.stringify(current_state)}, function(data, status) {
    write(data, "O")
  })
}

function handleClick(el, space) {
  var current_value = $("#square_" + space).html()
  if (current_value == "") {
    write(space, "X")
    var state = getState()
    requestMove(state)    
  }
}
