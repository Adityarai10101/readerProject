const body = document.querySelector("body");

async function getSummary(text) {
  let link = "https://adityarai10101--reader-project-summarize.modal.run/?text=\""+text+"\"";
  console.log(link);
  link = link.replace("\n", "");
  link = link.replace("#", "");
  link = link.replace(" ", "");
  console.log(link);
  console.log(encodeURI(link))
  const response = await fetch(encodeURI(link));
  let a = await response.text();
  return a;
}
async function storeVecs(text) {
  let link = "https://adityarai10101--reader-project-pushtovec.modal.run/?text=\"" + text + "\"";
  console.log(link);
  link = link.replace("\n", "");
  link = link.replace("#", "");
  link = link.replace(" ", "");
  console.log(link);
  console.log(encodeURI(link));
  const response = await fetch(encodeURI(link));
  let a = await response.text();
  return a
}


if (body) {
  console.log(body.textContent);
  // 1. make api call to embedder, and summarizer, in parallel
  getSummary(body.textContent).then((data) => console.log(data));
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