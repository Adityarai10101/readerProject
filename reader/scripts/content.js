console.log("I'm running");
console.log("I'm running");
console.log("I'm running");
console.log("I'm running");
console.log("I'm running");
console.log("I'm running");
console.log("I'm running");

const body = document.querySelector("body");

if (body) {
  console.log(body.innerHTML);
  // 1. make api call to embedder, and summarizer, in parallel
  // 2. make api call to langchain agent
  // 3. set the summary in the popup to be the value
  setTimeout(() => {
    const summary = "This is the summary of the article";
    setSummary(summary);
  }, 2000);
} else {
  console.log("body is null");
}