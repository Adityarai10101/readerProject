// Copyright 2022 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
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
} else {
  console.log("body is null");
}
