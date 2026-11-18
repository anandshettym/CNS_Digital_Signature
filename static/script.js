
let generatedSignature = "";

// Generate Digital Signature
document.getElementById("signForm").addEventListener(
    "submit", async function(event) {

    event.preventDefault();

    const file = document.getElementById("signFile").files[0];

    if (!file) {
        alert("Please select a file");
        return;
    }

    const button = this.querySelector("button");

    button.disabled = true;
    button.textContent = "Generating...";

    try {

        const formData = new FormData();

        formData.append("file", file);

        const response = await fetch("/sign", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Signing failed");
        }

        generatedSignature = data.signature;

        document.getElementById("fileName").textContent =
            data.filename;

        document.getElementById("hashValue").textContent =
            data.hash;

        document.getElementById("signResult").classList.remove("hidden");

    } catch (error) {

        alert(error.message);

    } finally {

        button.disabled = false;
        button.textContent = "Generate Signature";

    }
});


// Download Digital Signature
document.getElementById("downloadBtn").addEventListener(
    "click", function() {

    if (!generatedSignature) {
        alert("Generate a signature first");
        return;
    }

    const blob = new Blob(
        [generatedSignature],
        { type: "text/plain" }
    );

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");

    link.href = url;
    link.download = "digital_signature.sig";

    document.body.appendChild(link);

    link.click();

    link.remove();

    URL.revokeObjectURL(url);

});


// Verify Digital Signature
document.getElementById("verifyForm").addEventListener(
    "submit", async function(event) {

    event.preventDefault();

    const file = document.getElementById("verifyFile").files[0];

    const signatureFile =
        document.getElementById("signatureFile").files[0];

    if (!file || !signatureFile) {
        alert("Select both file and signature");
        return;
    }

    const button = this.querySelector("button");

    button.disabled = true;
    button.textContent = "Verifying...";

    try {

        const formData = new FormData();

        formData.append("file", file);
        formData.append("signature", signatureFile);

        const response = await fetch("/verify", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        const result = document.getElementById("verifyResult");

        const status = document.getElementById("verifyStatus");

        result.classList.remove("hidden", "success", "failure");

        status.textContent = data.status || "Error";

        document.getElementById("verifyMessage").textContent =
            data.message || data.error || "Verification failed";

        document.getElementById("verifyHash").textContent =
            data.hash || "Not available";

        if (data.status === "Verified") {
            result.classList.add("success");
        } else {
            result.classList.add("failure");
        }

    } catch (error) {

        alert(error.message);

    } finally {

        button.disabled = false;
        button.textContent = "Verify Signature";

    }
});
