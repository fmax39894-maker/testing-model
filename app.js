const $ = (selector) => document.querySelector(selector);
const rangeButtons = [...document.querySelectorAll(".range-option")];
let rangeMax = 100;
let scanInfo = {};
let toastTimer;

function browserName(ua) {
  if (/SamsungBrowser/i.test(ua)) return "Samsung Internet";
  if (/EdgA|EdgiOS|Edg\//i.test(ua)) return "Edge";
  if (/OPR|Opera/i.test(ua)) return "Opera";
  if (/Firefox/i.test(ua)) return "Firefox";
  if (/Chrome|CriOS/i.test(ua)) return "Chrome";
  if (/Safari/i.test(ua)) return "Safari";
  return "Unknown";
}
function short(value, fallback = "Not exposed") {
  return value === undefined || value === null || value === "" ? fallback : String(value);
}
async function scanDevice() {
  $("#deviceState").textContent = "SCANNING";
  $("#deviceName").textContent = "Detecting device…";
  const ua = navigator.userAgent || "";
  let model = "", platform = navigator.userAgentData?.platform || navigator.platform || "Unknown";
  let androidVersion = "", architecture = "";
  if (navigator.userAgentData) {
    try {
      const d = await navigator.userAgentData.getHighEntropyValues(["model", "platformVersion", "architecture"]);
      model = d.model || "";
      androidVersion = d.platformVersion || "";
      platform = d.platform || platform;
      architecture = d.architecture || "";
    } catch (_) {}
  }
  const android = /Android/i.test(ua) || /Android/i.test(platform);
  const deviceName = model || (android ? "Android device" : platform || "Unknown device");
  $("#deviceName").textContent = deviceName;
  $("#deviceSub").textContent = android
    ? `${short(androidVersion, "Android version hidden")} · Browser-reported details`
    : "Not identified as Android by this browser";
  $("#screenInfo").textContent = `${screen.width} × ${screen.height}`;
  $("#ramInfo").textContent = typeof navigator.deviceMemory === "number" ? `~${navigator.deviceMemory} GB` : "Unavailable";
  $("#cpuInfo").textContent = Number.isFinite(navigator.hardwareConcurrency) ? `${navigator.hardwareConcurrency} threads` : "Unavailable";
  $("#browserInfo").textContent = browserName(ua);
  $("#platformInfo").textContent = android ? "Android" : short(platform, "Unknown");
  $("#pixelInfo").textContent = `${window.devicePixelRatio || 1}×`;
  $("#deviceState").textContent = android ? "DEVICE READY" : "LIMITED DATA";
  scanInfo = {
    android, model, androidVersion, architecture,
    screen: Math.max(1, screen.width * screen.height),
    ram: navigator.deviceMemory || 0,
    cpu: navigator.hardwareConcurrency || 0,
    pixelRatio: window.devicePixelRatio || 1
  };
}
rangeButtons.forEach(button => button.addEventListener("click", () => {
  rangeButtons.forEach(b => b.classList.toggle("active", b === button));
  rangeMax = Number(button.dataset.max);
  $("#scaleSelect").value = String(rangeMax);
}));
$("#rescan").addEventListener("click", scanDevice);

const styles = {
  "one-tap": {name:"One-tap", base:[96,91,84,76,48,67], factor:[1.02,1.03,1.02,1,0.98,1.02]},
  balanced: {name:"Balanced", base:[92,86,78,70,48,62], factor:[1,1,1,1,1,1]},
  rush: {name:"Rush", base:[98,94,88,79,52,70], factor:[1.03,1.03,1.04,1.02,1,1.03]},
  long: {name:"Long-range", base:[82,75,67,58,42,52], factor:[0.97,0.97,0.96,0.96,0.98,0.96]},
  smooth: {name:"Smooth", base:[88,81,73,64,45,58], factor:[0.98,0.98,0.98,0.98,0.98,0.98]}
};
const labels = ["General", "Red Dot", "2× Scope", "4× Scope", "Sniper Scope", "Free Look"];

function makeSettings() {
  const styleKey = $("#styleSelect").value;
  const style = styles[styleKey] || styles["one-tap"];
  const performance = $("#performanceSelect").value;
  // These are transparent heuristics, not a real FPS or touch-latency benchmark.
  let deviceAdjustment = 0;
  if (scanInfo.ram && scanInfo.ram <= 2) deviceAdjustment -= 4;
  else if (scanInfo.ram >= 8) deviceAdjustment += 2;
  if (scanInfo.cpu && scanInfo.cpu <= 4) deviceAdjustment -= 2;
  if (scanInfo.pixelRatio >= 3) deviceAdjustment -= 1;
  const perfAdjustment = performance === "smooth" ? -5 : performance === "responsive" ? 4 : 0;
  const factor = rangeMax / 100;
  return style.base.map((base, i) => {
    const raw = Math.round((base * style.factor[i] + deviceAdjustment + perfAdjustment) * factor);
    return Math.max(0, Math.min(rangeMax, raw));
  });
}
function showToast(message) {
  const toast = $("#toast");
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2300);
}
function renderResults(values) {
  const styleKey = $("#styleSelect").value;
  const style = styles[styleKey] || styles["one-tap"];
  $("#resultStyle").textContent = style.name;
  $("#resultRange").textContent = `0–${rangeMax}`;
  $("#resultFit").textContent = $("#performanceSelect").selectedOptions[0].textContent.split(" ")[0];
  $("#sensitivityRows").replaceChildren();
  values.forEach((value, i) => {
    const row = document.createElement("div");
    row.className = "sensitivity-row";
    const top = document.createElement("div");
    top.className = "sens-top";
    const name = document.createElement("span");
    name.textContent = labels[i];
    const number = document.createElement("strong");
    number.textContent = value;
    top.append(name, number);
    const track = document.createElement("div");
    track.className = "sens-track";
    const fill = document.createElement("div");
    fill.style.width = `${value / rangeMax * 100}%`;
    track.append(fill);
    row.append(top, track);
    $("#sensitivityRows").append(row);
  });
  $("#results").classList.remove("hidden");
}
let generating = false;
async function generate() {
  if (generating) return;
  generating = true;
  $("#generateBtn").disabled = true;
  $("#generateText").textContent = "ANALYZING PROFILE…";
  $("#progressWrap").classList.remove("hidden");
  $("#results").classList.add("hidden");
  const start = Date.now();
  const duration = 20000;
  const phases = [
    [0, "Reading browser-accessible device hints…"],
    [25, "Checking screen and hardware hints…"],
    [50, "Applying your selected play style…"],
    [75, "Building sensitivity recommendations…"],
    [95, "Finalizing your profile…"]
  ];
  await new Promise(resolve => {
    function tick() {
      const elapsed = Date.now() - start;
      const percent = Math.min(100, Math.floor(elapsed / duration * 100));
      $("#progressBar").style.width = `${percent}%`;
      $("#progressPercent").textContent = `${percent}%`;
      const phase = [...phases].reverse().find(p => percent >= p[0]);
      if (phase) $("#progressLabel").textContent = phase[1];
      if (elapsed >= duration) resolve();
      else requestAnimationFrame(tick);
    }
    tick();
  });
  const values = makeSettings();
  renderResults(values);
  $("#progressLabel").textContent = "Profile generated";
  $("#progressPercent").textContent = "100%";
  $("#generateText").textContent = "GENERATE AGAIN";
  $("#generateBtn").disabled = false;
  generating = false;
  $("#results").scrollIntoView({behavior:"smooth", block:"start"});
}
$("#generateBtn").addEventListener("click", generate);
$("#againBtn").addEventListener("click", () => {
  $("#results").classList.add("hidden");
  $("#generateBtn").scrollIntoView({behavior:"smooth", block:"center"});
});
$("#copyBtn").addEventListener("click", async () => {
  const lines = [
    "Craft X Gamer — Sensitivity Pro",
    `Style: ${$("#resultStyle").textContent}`,
    `Range: ${$("#resultRange").textContent}`,
    ...[...$("#sensitivityRows").children].map(row => `${row.querySelector(".sens-top span").textContent}: ${row.querySelector(".sens-top strong").textContent}`)
  ];
  try {
    await navigator.clipboard.writeText(lines.join("\n"));
    showToast("Settings copied to clipboard");
  } catch (_) {
    const area = document.createElement("textarea");
    area.value = lines.join("\n");
    document.body.append(area); area.select();
    const success = document.execCommand("copy");
    area.remove();
    showToast(success ? "Settings copied to clipboard" : "Copy not available in this browser");
  }
});
scanDevice();
