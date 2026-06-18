function getCookie(name) {
  const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return match ? decodeURIComponent(match[2]) : "";
}

function bufferToBase64url(buffer) {
  const bytes = new Uint8Array(buffer);
  let binary = "";
  bytes.forEach((b) => (binary += String.fromCharCode(b)));
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function base64urlToBuffer(base64url) {
  const padding = "=".repeat((4 - (base64url.length % 4)) % 4);
  const base64 = (base64url + padding).replace(/-/g, "+").replace(/_/g, "/");
  const raw = atob(base64);
  const buffer = new ArrayBuffer(raw.length);
  const view = new Uint8Array(buffer);
  for (let i = 0; i < raw.length; i++) view[i] = raw.charCodeAt(i);
  return buffer;
}

function prepareCreationOptions(options) {
  options.challenge = base64urlToBuffer(options.challenge);
  options.user.id = base64urlToBuffer(options.user.id);
  if (options.excludeCredentials) {
    options.excludeCredentials = options.excludeCredentials.map((c) => ({
      ...c,
      id: base64urlToBuffer(c.id),
    }));
  }
  return options;
}

function prepareRequestOptions(options) {
  options.challenge = base64urlToBuffer(options.challenge);
  if (options.allowCredentials) {
    options.allowCredentials = options.allowCredentials.map((c) => ({
      ...c,
      id: base64urlToBuffer(c.id),
    }));
  }
  return options;
}

function credentialToJSON(credential) {
  const response = credential.response;
  const json = {
    id: credential.id,
    rawId: bufferToBase64url(credential.rawId),
    type: credential.type,
    response: {
      clientDataJSON: bufferToBase64url(response.clientDataJSON),
    },
  };
  if (response.attestationObject) {
    json.response.attestationObject = bufferToBase64url(response.attestationObject);
  }
  if (response.authenticatorData) {
    json.response.authenticatorData = bufferToBase64url(response.authenticatorData);
  }
  if (response.signature) {
    json.response.signature = bufferToBase64url(response.signature);
  }
  if (response.userHandle) {
    json.response.userHandle = bufferToBase64url(response.userHandle);
  }
  return json;
}

async function postJSON(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    credentials: "same-origin",
    body: JSON.stringify(data),
  });
  const payload = await res.json();
  if (!res.ok) throw new Error(payload.error || "Request failed");
  return payload;
}

async function registerWindowsHello(registerUrl, completeUrl) {
  const res = await fetch(registerUrl, { credentials: "same-origin" });
  const options = await res.json();
  if (!res.ok) throw new Error(options.error || "Could not start registration");

  const publicKey = prepareCreationOptions(options);
  const credential = await navigator.credentials.create({ publicKey });
  if (!credential) throw new Error("Registration cancelled");

  return postJSON(completeUrl, credentialToJSON(credential));
}

async function loginWindowsHello(matric, optionsUrl, completeUrl) {
  const res = await fetch(
    optionsUrl + "?matric_no=" + encodeURIComponent(matric),
    { credentials: "same-origin" }
  );
  const options = await res.json();
  if (!res.ok) throw new Error(options.error || "Could not start login");

  const publicKey = prepareRequestOptions(options);
  const credential = await navigator.credentials.get({ publicKey });
  if (!credential) throw new Error("Login cancelled");

  return postJSON(completeUrl, credentialToJSON(credential));
}

function unlockEnrollStep2() {
  const stepNose = document.getElementById("step-nose");
  if (stepNose) stepNose.classList.remove("enroll-step-locked");

  const pending = document.getElementById("step-hello-pending");
  const helloDone = document.getElementById("step-hello-done");
  if (pending) pending.style.display = "none";
  if (helloDone) helloDone.style.display = "";

  const locked = document.getElementById("step-nose-locked");
  const formWrap = document.getElementById("step-nose-form-wrap");
  if (locked) locked.style.display = "none";
  if (formWrap) formWrap.style.display = "";

  const stepHello = document.getElementById("step-hello");
  if (stepHello) stepHello.classList.add("enroll-step-done");

  if (stepNose) {
    stepNose.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

window.unlockEnrollStep2 = unlockEnrollStep2;

function bindButton(btn) {
  if (!btn) return;
  btn.addEventListener("click", async () => {
    const status = document.getElementById("hello-status");
    try {
      if (!window.PublicKeyCredential) {
        throw new Error("WebAuthn is not supported in this browser.");
      }
      status.textContent = "Waiting for Windows Hello…";
      status.className = "";

      if (btn.dataset.mode === "register") {
        await registerWindowsHello(
          btn.dataset.registerOptions,
          btn.dataset.registerComplete
        );
        if (document.getElementById("step-nose-form-wrap")) {
          unlockEnrollStep2();
          const statusEl = document.getElementById("hello-status");
          if (statusEl) {
            statusEl.textContent = "Step 1 done! Complete Step 2 below.";
            statusEl.className = "success";
          }
        } else {
          window.location.href = "/biometrics/enroll/?step=2";
        }
      } else if (btn.dataset.mode === "login") {
        const matric = document.getElementById("matric_no")?.value?.trim();
        if (!matric) throw new Error("Enter your Staff/Student ID first.");
        const result = await loginWindowsHello(
          matric.toUpperCase(),
          btn.dataset.authOptions,
          btn.dataset.authComplete
        );
        window.location.href = result.redirect || "/accounts/dashboard/";
      } else if (btn.dataset.mode === "verify") {
        const matric = btn.dataset.matric;
        await loginWindowsHello(
          matric,
          btn.dataset.authOptions,
          btn.dataset.authComplete
        );
        status.textContent = "Windows Hello verified!";
        status.className = "success";
      }
    } catch (err) {
      status.textContent = err.message || String(err);
      status.className = "error";
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  bindButton(document.getElementById("btn-windows-hello"));
});
