console.log("I'm running");
console.log("I'm running");
console.log("I'm running");
console.log("I'm running");
console.log("I'm running");
console.log("I'm running");
console.log("I'm running");

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
  setTimeout(() => {
    const summary = "This is the summary of the article";
    setSummary(summary);
  }, 2000);
} else {
  console.log("body is null");
}