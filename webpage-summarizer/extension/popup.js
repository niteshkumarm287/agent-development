const BACKEND = "https://backend-319512124676.us-central1.run.app/";
let activeMode = "summary";

document.querySelectorAll(".mode").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".mode").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    activeMode = btn.dataset.mode;
  });
});

document.getElementById("btn").addEventListener("click", async () => {
  const resultEl  = document.getElementById("result");
  const spinnerEl = document.getElementById("spinner");
  const errorEl   = document.getElementById("error");

  resultEl.textContent  = "";
  errorEl.style.display = "none";
  spinnerEl.style.display = "block";

  try {
    // Ask content script for the page text
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const [{ result: pageText }] = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => document.body.innerText,
    });

    const res = await fetch(`${BACKEND}/summarize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: pageText, mode: activeMode }),
    });

    if (!res.ok) throw new Error(`Backend error: ${res.status}`);
    const data = await res.json();
    resultEl.textContent = data.summary;
  } catch (err) {
    errorEl.textContent   = err.message;
    errorEl.style.display = "block";
  } finally {
    spinnerEl.style.display = "none";
  }
});