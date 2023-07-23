const body = document.querySelector("body");

async function getSummary(url) {
  console.log(url);

  let endpoint = `https://adityarai10101--reader-project-summarize.modal.run/?link=${url}`;
  console.log(endpoint);
  console.log(encodeURI(endpoint));
  const response = await fetch(encodeURI(endpoint));
  let a = await response.text();
  return a;
}
async function storeVecs(text) {
  let link =
    'https://adityarai10101--reader-project-pushtovec.modal.run/?text="' +
    text +
    '"';
  console.log(link);
  link = link.replace("\n", "");
  link = link.replace("#", "");
  link = link.replace(" ", "");
  console.log(link);
  console.log(encodeURI(link));
  const response = await fetch(encodeURI(link));
  let a = await response.text();
  return a;
}

if (body) {
  const url = window.location.href;
  console.log(url);
  // 1. make api call to embedder, and summarizer, in parallel
  getSummary(url).then((summary) => {
    console.log(summary);
    chrome.runtime.sendMessage({ summary }, function (response) {
      console.log("content script sending message to popup");
      console.log(response);
    });
  });

  storeVecs(body.textContent);
  // 2. make api call to langchain agent
  // 3. set the summary in the popup to be the value
  const summary = body.innerHTML;
  setTimeout(() => {
    chrome.runtime.sendMessage({ summary }, function (response) {
      console.log("content script sending message to popup");
      console.log(response);
    });
  }, 2000);
} else {
  console.log("body is null");
}
