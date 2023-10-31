function insertVideo(search,videoId,uniqueId) {

  const instructions = document.getElementById('instructions');

  //finds occurrences
  const occurrence = instructions.innerText.match(search);
  instructions.innerHTML = instructions.innerHTML.replace(occurrence, `<span class="highlight" style="color: #2596be; text-decoration: underline;" class="btn btn-danger btn-sm m-1" data-toggle="modal" data-target="#tipModal${uniqueId}">${occurrence}</span>`);
  if(occurrence == null) {
    const lowercaseInstructions = instructions.innerText.toLowerCase();
    const lowercaseOccurrence = lowercaseInstructions.match(search.toLowerCase());
    instructions.innerHTML = instructions.innerHTML.replace(lowercaseOccurrence, `<span class="highlight" style="color: #2596be; text-decoration: underline;" class="btn btn-danger btn-sm m-1" data-toggle="modal" data-target="#tipModal${uniqueId}">${lowercaseOccurrence}</span>`);
  }


  const modalDiv = document.createElement("div");
  modalDiv.innerHTML = `
    <div class="modal fade" id="tipModal${uniqueId}" role="dialog" tabindex="-1" aria-labelledby="tipModalLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="tipModalLabel">Tip Video</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="ratio ratio-4x3">
              <iframe src="https://www.youtube.com/embed/${videoId}"></iframe>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  `;

  // Add the modal to the document body.
  document.body.appendChild(modalDiv);
}