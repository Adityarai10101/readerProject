const setSummary = (summary) => {
  const summaryElement = document.getElementById("summary");
  summaryElement.innerHTML = summary;
};

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  console.log("Popup got a message");
  console.log(request);
  setSummary(request.summary);
  sendResponse("Popup set the summary");
});

/**
 * You have to refresh the page, then open the modal. You can't open the modal without
 * refreshing the page.
 */
