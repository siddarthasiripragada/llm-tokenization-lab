const examples = {
  english: "Tokenization happens before reasoning.",
  sql: "SELECT user_id, COUNT(*) FROM events WHERE status = 'failed';",
  json: "{\"user_id\":\"acct_123\",\"plan\":\"enterprise\",\"active\":true}",
  log: "2026-07-09T21:03:44Z ERROR payment_worker retry_count=3 account_id=acct_9f3a",
  identifier: "customerBillingExportJob_v2_failed_count",
  code: "def chunk_text(text, max_tokens=200): return text[:max_tokens]",
  unicode: "Tokenization with café, naïve, emoji 😊, and mixed-language text.",
};

const tokenPattern = /[A-Za-z]+|\d+|[^\w\s]|\w/gu;

function tokenize(text) {
  return text.match(tokenPattern) || [];
}

function wordCount(text) {
  const words = text.trim().match(/\S+/g);
  return words ? words.length : 0;
}

function numberValue(id) {
  const value = Number(document.getElementById(id).value);
  return Number.isFinite(value) ? value : 0;
}

function tokenType(token) {
  if (/^\d+$/u.test(token)) return "number";
  if (/^[A-Za-z]+$/u.test(token)) return "word";
  if (/^[^\w\s]$/u.test(token)) return "punctuation";
  return "symbol";
}

function currentTokenSummary() {
  const text = document.getElementById("tokenInput").value;
  const tokens = tokenize(text);
  return {
    text,
    tokens,
    words: wordCount(text),
    characters: text.length,
  };
}

function renderTokens() {
  const summary = currentTokenSummary();
  const { text, tokens } = summary;
  document.getElementById("tokenCount").textContent = String(tokens.length);
  document.getElementById("wordCount").textContent = String(summary.words);
  document.getElementById("charCount").textContent = String(summary.characters);

  const tokenList = document.getElementById("tokenList");
  tokenList.replaceChildren(
    ...tokens.map((token) => {
      const item = document.createElement("span");
      item.className = `token token-${tokenType(token)}`;
      item.textContent = token;
      return item;
    }),
  );
}

function renderBudget() {
  const maxContext = Math.max(numberValue("maxContext"), 1);
  const used =
    numberValue("systemPrompt") +
    numberValue("userQuery") +
    numberValue("expectedOutput") +
    numberValue("safetyMargin") +
    numberValue("chatHistory") +
    numberValue("toolOutput");
  const retrieval = Math.max(maxContext - used, 0);
  const utilization = used / maxContext;

  document.getElementById("usedTokens").textContent = String(used);
  document.getElementById("retrievalTokens").textContent = String(retrieval);
  document.getElementById("utilization").textContent = `${(utilization * 100).toFixed(1)}%`;
  document.getElementById("budgetBar").style.width = `${Math.min(utilization * 100, 100)}%`;
}

function renderCost() {
  const inputText = document.getElementById("costInput").value;
  const inputTokens = tokenize(inputText).length;
  const outputTokens = Math.max(numberValue("costOutputTokens"), 0);
  const inputCost = Math.max(numberValue("inputCost"), 0);
  const outputCost = Math.max(numberValue("outputCost"), 0);
  const estimatedCost = (inputTokens / 1000) * inputCost + (outputTokens / 1000) * outputCost;

  document.getElementById("costInputTokens").textContent = String(inputTokens);
  document.getElementById("costTotalTokens").textContent = String(inputTokens + outputTokens);
  document.getElementById("estimatedCost").textContent = `$${estimatedCost.toFixed(6)}`;
}

function renderChunks() {
  const text = document.getElementById("chunkInput").value;
  const tokens = tokenize(text);
  const maxTokens = Math.max(numberValue("chunkMax"), 1);
  const overlap = Math.max(numberValue("chunkOverlap"), 0);
  const chunks = document.getElementById("chunks");

  if (overlap >= maxTokens) {
    chunks.textContent = "Overlap must be less than max tokens.";
    return;
  }

  const step = maxTokens - overlap;
  const nodes = [];
  for (let start = 0; start < tokens.length; start += step) {
    const chunkTokens = tokens.slice(start, start + maxTokens);
    if (chunkTokens.length === 0) break;

    const chunk = document.createElement("div");
    chunk.className = "chunk";

    const title = document.createElement("div");
    title.className = "chunk-title";
    title.textContent = `Chunk ${nodes.length + 1} (${chunkTokens.length} tokens)`;

    const tokenWrap = document.createElement("div");
    tokenWrap.className = "chunk-tokens";
    chunkTokens.forEach((token, index) => {
      const item = document.createElement("span");
      item.className = index < overlap && start > 0 ? "chunk-token overlap" : "chunk-token";
      item.textContent = token;
      tokenWrap.append(item);
    });

    chunk.append(title, tokenWrap);
    nodes.push(chunk);

    if (start + maxTokens >= tokens.length) break;
  }

  chunks.replaceChildren(...nodes);
}

function renderAll() {
  renderTokens();
  renderBudget();
  renderCost();
  renderChunks();
}

document.getElementById("exampleSelect").addEventListener("change", (event) => {
  document.getElementById("tokenInput").value = examples[event.target.value];
  renderTokens();
});

async function copyText(text, message) {
  const status = document.getElementById("copyStatus");
  try {
    await navigator.clipboard.writeText(text);
    status.textContent = message;
  } catch {
    status.textContent = "Copy failed";
  }
  window.setTimeout(() => {
    status.textContent = "";
  }, 1800);
}

document.getElementById("copyTokens").addEventListener("click", () => {
  const { tokens } = currentTokenSummary();
  copyText(JSON.stringify(tokens, null, 2), "Tokens copied");
});

document.getElementById("copySummary").addEventListener("click", () => {
  const summary = currentTokenSummary();
  const markdown = [
    "## Tokenization summary",
    "",
    `Input: \`${summary.text}\``,
    "",
    `- Tokens: ${summary.tokens.length}`,
    `- Words: ${summary.words}`,
    `- Characters: ${summary.characters}`,
    "",
    "```text",
    JSON.stringify(summary.tokens),
    "```",
  ].join("\n");
  copyText(markdown, "Summary copied");
});

[
  "tokenInput",
  "maxContext",
  "systemPrompt",
  "userQuery",
  "expectedOutput",
  "safetyMargin",
  "chatHistory",
  "toolOutput",
  "costInput",
  "costOutputTokens",
  "inputCost",
  "outputCost",
  "chunkInput",
  "chunkMax",
  "chunkOverlap",
].forEach((id) => {
  document.getElementById(id).addEventListener("input", renderAll);
});

document.getElementById("tokenInput").value = examples.sql;
renderAll();
