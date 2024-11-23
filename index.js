import { io } from "socket.io-client";
import { Converter } from "showdown";

const socket = io("ws://localhost:5000");
const converter = new Converter({
  tables: true,
  strikethrough: true,
});

const root = document.getElementById("main");

const parseMarkdownHTML = (text) => {
  const html = converter.makeHtml(text);
  console.log(html);
  return html;
};

socket.on("file_changed", (data) => {
  const html = parseMarkdownHTML(data);
  root.innerHTML = html;
});
